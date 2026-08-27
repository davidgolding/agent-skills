#!/usr/bin/env python3
"""Tiered existence verification for a candidate bibliographic citation.

If lit-review-compiler/settings.json defines a serpapi_key (see
serpapi_config.py), checks Google Scholar first as Tier 0. Otherwise, or if
Tier 0 doesn't confirm, checks free scholarly APIs (Crossref, OpenAlex,
Semantic Scholar) and, if none confirm it, against free catalog APIs (Open
Library, Google Books) as a secondary tier. This is the mechanical guardrail
lit-review-compiler uses to make sure no citation is included on the model's
recollection or inference alone.

Usage:
    python3 verify_citation.py --title "..." [--author "..."] [--year YYYY]

Prints a JSON object to stdout:
    {
        "tier": "scholar_confirmed" | "api_confirmed" | "secondary_confirmed" | "unverified",
        "query": {"title": ..., "author": ..., "year": ...},
        "matched": {...} | null,
        "checked": ["googlescholar", "crossref", "openalex", ...],
        "errors": [{"source": "...", "error": "..."}],
        "scholar_available": true | false
    }

Exit code is always 0 on a completed run; the "tier" field communicates the
result. A non-empty "errors" list for a source that never matched means that
source's check was inconclusive (network/rate-limit failure), not a
confirmed absence -- see references/sharp_edges.md, "Verification API
Unavailable Mid-Run". "scholar_available" reflects whether a serpapi_key was
configured for this run at all, independent of whether Tier 0 matched.
"""

import argparse
import difflib
import json
import re
import socket
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

from serpapi_config import get_serpapi_key

USER_AGENT = "lit-review-compiler-verify-citation/1.0 (mailto:research@example.invalid)"
TIMEOUT_SECONDS = 12
TITLE_SIMILARITY_THRESHOLD = 0.78
YEAR_TOLERANCE_TIER0 = 1
YEAR_TOLERANCE_TIER1 = 1
YEAR_TOLERANCE_TIER2 = 15

TIER0_SOURCES = ("googlescholar",)
TIER1_SOURCES = ("crossref", "openalex", "semanticscholar")
TIER2_SOURCES = ("openlibrary", "googlebooks")


# Letters that carry a stroke or ligature rather than a combining diacritical
# mark are not decomposed by NFKD (e.g. "ø" is its own code point, not "o" +
# a combining stroke), so unicodedata.normalize alone misses them.
_MANUAL_TRANSLITERATIONS = {
    "ø": "o", "Ø": "O",  # ø Ø
    "ł": "l", "Ł": "L",  # ł Ł
    "đ": "d", "Đ": "D",  # đ Đ
    "ß": "ss",  # ß
    "æ": "ae", "Æ": "AE",  # æ Æ
    "œ": "oe", "Œ": "OE",  # œ Œ
}


def strip_diacritics(text):
    text = "".join(_MANUAL_TRANSLITERATIONS.get(ch, ch) for ch in (text or ""))
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def normalize_title(title):
    text = strip_diacritics(title).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_name(name):
    return strip_diacritics(name or "").lower()


def title_similarity(a, b):
    return difflib.SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def author_matches(query_author, candidate_authors):
    if not query_author:
        return True
    if not candidate_authors:
        return False
    query_surname = normalize_name(query_author).strip().split()[-1]
    return any(query_surname in normalize_name(candidate) for candidate in candidate_authors)


def year_matches(query_year, candidate_year, tolerance):
    if query_year is None:
        return True
    if candidate_year is None:
        return False
    try:
        return abs(int(candidate_year) - int(query_year)) <= tolerance
    except (TypeError, ValueError):
        return False


def fetch_json(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def query_crossref(title, author, year):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": title, "rows": 5}
    )
    data = fetch_json(url)
    candidates = []
    for item in data.get("message", {}).get("items", []):
        titles = item.get("title") or []
        if not titles:
            continue
        subtitles = item.get("subtitle") or []
        authors = [
            " ".join(filter(None, [a.get("given"), a.get("family")]))
            for a in item.get("author", []) or []
        ]
        date_parts = (
            (item.get("published-print") or {}).get("date-parts")
            or (item.get("published-online") or {}).get("date-parts")
            or (item.get("issued") or {}).get("date-parts")
            or [[None]]
        )
        candidate_year = date_parts[0][0] if date_parts and date_parts[0] else None
        # Crossref sometimes truncates a bibliographic query's subtitle, and
        # sometimes returns the full subtitle where the query only had a
        # fragment of it -- keep both the bare title and title+subtitle as
        # separate candidates so best_match can take whichever scores higher.
        title_variants = {titles[0]}
        if subtitles:
            title_variants.add(": ".join([titles[0], subtitles[0]]))
        for title_variant in title_variants:
            candidates.append(
                {
                    "title": title_variant,
                    "authors": authors,
                    "year": candidate_year,
                    "id": item.get("DOI"),
                    "source": "crossref",
                }
            )
    return candidates


def query_openalex(title, author, year):
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": title, "per-page": 5}
    )
    data = fetch_json(url)
    candidates = []
    for item in data.get("results", []) or []:
        authors = [
            (a.get("author") or {}).get("display_name", "")
            for a in item.get("authorships", []) or []
        ]
        candidates.append(
            {
                "title": item.get("display_name") or item.get("title") or "",
                "authors": authors,
                "year": item.get("publication_year"),
                "id": item.get("doi") or item.get("id"),
                "source": "openalex",
            }
        )
    return candidates


def query_semanticscholar(title, author, year):
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
        {"query": title, "fields": "title,year,authors", "limit": 5}
    )
    data = fetch_json(url)
    candidates = []
    for item in data.get("data", []) or []:
        authors = [a.get("name", "") for a in item.get("authors", []) or []]
        candidates.append(
            {
                "title": item.get("title") or "",
                "authors": authors,
                "year": item.get("year"),
                "id": item.get("paperId"),
                "source": "semanticscholar",
            }
        )
    return candidates


def query_openlibrary(title, author, year):
    params = {"title": title, "limit": 5}
    if author:
        params["author"] = author
    url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    candidates = []
    for item in data.get("docs", []) or []:
        candidates.append(
            {
                "title": item.get("title") or "",
                "authors": item.get("author_name") or [],
                "year": item.get("first_publish_year"),
                "id": item.get("key"),
                "source": "openlibrary",
            }
        )
    return candidates


def query_googlebooks(title, author, year):
    query = f"intitle:{title}"
    if author:
        query += f" inauthor:{author}"
    url = "https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode(
        {"q": query, "maxResults": 5}
    )
    data = fetch_json(url)
    candidates = []
    for item in data.get("items", []) or []:
        info = item.get("volumeInfo", {})
        published = info.get("publishedDate", "") or ""
        year_prefix = re.match(r"(\d{4})", published)
        candidates.append(
            {
                "title": info.get("title") or "",
                "authors": info.get("authors") or [],
                "year": int(year_prefix.group(1)) if year_prefix else None,
                "id": item.get("id"),
                "source": "googlebooks",
            }
        )
    return candidates


def query_googlescholar(title, author, year):
    api_key = get_serpapi_key()
    if not api_key:
        return []
    query = title
    if author:
        query += f" {author}"
    params = {"engine": "google_scholar", "q": query, "api_key": api_key}
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    candidates = []
    for item in data.get("organic_results", []) or []:
        summary = (item.get("publication_info") or {}).get("summary", "")
        year_match = re.search(r"\b(19|20)\d{2}\b", summary)
        authors_head = summary.split(" - ")[0] if summary else ""
        candidates.append(
            {
                "title": item.get("title") or "",
                "authors": [name.strip() for name in authors_head.split(",") if name.strip()],
                "year": int(year_match.group(0)) if year_match else None,
                "id": item.get("result_id"),
                "source": "googlescholar",
            }
        )
    return candidates


QUERY_FUNCTIONS = {
    "googlescholar": query_googlescholar,
    "crossref": query_crossref,
    "openalex": query_openalex,
    "semanticscholar": query_semanticscholar,
    "openlibrary": query_openlibrary,
    "googlebooks": query_googlebooks,
}


def best_match(candidates, title, author, year, tolerance):
    best = None
    best_score = 0.0
    for candidate in candidates:
        similarity = title_similarity(title, candidate.get("title"))
        if similarity < TITLE_SIMILARITY_THRESHOLD:
            continue
        if not author_matches(author, candidate.get("authors") or []):
            continue
        if not year_matches(year, candidate.get("year"), tolerance):
            continue
        if similarity > best_score:
            best = candidate
            best_score = similarity
    if best:
        best = dict(best)
        best["match_score"] = round(best_score, 3)
    return best


def verify(title, author, year):
    checked = []
    errors = []
    scholar_available = get_serpapi_key() is not None

    tiers = [
        ("api_confirmed", TIER1_SOURCES, YEAR_TOLERANCE_TIER1),
        ("secondary_confirmed", TIER2_SOURCES, YEAR_TOLERANCE_TIER2),
    ]
    # Only attempt Google Scholar when a serpapi_key is configured -- with no
    # key, skip it entirely (not even listed in "checked") so behavior is an
    # exact no-op match for a run with no settings.json at all.
    if scholar_available:
        tiers.insert(0, ("scholar_confirmed", TIER0_SOURCES, YEAR_TOLERANCE_TIER0))

    for tier_name, sources, tolerance in tiers:
        for source in sources:
            checked.append(source)
            try:
                candidates = QUERY_FUNCTIONS[source](title, author, year)
            except (urllib.error.URLError, socket.timeout, ValueError, json.JSONDecodeError) as exc:
                errors.append({"source": source, "error": str(exc)})
                continue
            match = best_match(candidates, title, author, year, tolerance)
            if match:
                return {
                    "tier": tier_name,
                    "query": {"title": title, "author": author, "year": year},
                    "matched": match,
                    "checked": checked,
                    "errors": errors,
                    "scholar_available": scholar_available,
                }

    return {
        "tier": "unverified",
        "query": {"title": title, "author": author, "year": year},
        "matched": None,
        "checked": checked,
        "errors": errors,
        "scholar_available": scholar_available,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Candidate source title")
    parser.add_argument("--author", default=None, help="A candidate author's surname or full name")
    parser.add_argument("--year", type=int, default=None, help="Candidate publication year")
    args = parser.parse_args()

    result = verify(args.title, args.author, args.year)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
