#!/usr/bin/env python3
"""Optional Google Scholar discovery search via SerpApi, for lit-review-compiler.

Only runs if lit-review-compiler/settings.json defines a non-empty serpapi_key
(see serpapi_config.py). If no key is configured, this prints
{"available": false} and exits 0 -- callers should treat that as a silent
no-op and continue with their existing discovery method (e.g. web search),
not as an error.

When a key is available, this hits SerpApi's engine=google_scholar and
returns normalized organic results, including each result's "cited by" count
(SerpApi's stand-in for forward citation chaining) and link, so the model can
follow it to see who has cited the source since.

Usage:
    python3 search_scholar.py --query "..." [--year-lo YYYY] [--year-hi YYYY]

Prints a JSON object to stdout:
    {
        "available": true | false,
        "query": {...},
        "results": [
            {"title": ..., "authors": [...], "year": ..., "snippet": ...,
             "link": ..., "cited_by_count": ..., "cited_by_link": ...},
            ...
        ]
    }
"""

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request

from serpapi_config import get_serpapi_key

TIMEOUT_SECONDS = 12
YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")


def _extract_year(summary):
    match = YEAR_PATTERN.search(summary or "")
    return int(match.group(0)) if match else None


def _extract_authors(summary):
    # SerpApi's publication_info.summary is typically shaped like
    # "AB Author, CD Other - Journal Name, Year - Publisher", so authors are
    # whatever precedes the first " - " separator.
    if not summary:
        return []
    head = summary.split(" - ")[0]
    return [name.strip() for name in head.split(",") if name.strip()]


def search_google_scholar(api_key, query, year_lo=None, year_hi=None):
    params = {"engine": "google_scholar", "q": query, "api_key": api_key}
    if year_lo:
        params["as_ylo"] = year_lo
    if year_hi:
        params["as_yhi"] = year_hi
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        data = json.loads(response.read().decode("utf-8"))

    results = []
    for item in data.get("organic_results", []) or []:
        summary = (item.get("publication_info") or {}).get("summary", "")
        cited_by = (item.get("inline_links") or {}).get("cited_by") or {}
        results.append(
            {
                "title": item.get("title") or "",
                "authors": _extract_authors(summary),
                "year": _extract_year(summary),
                "snippet": item.get("snippet") or "",
                "link": item.get("link"),
                "cited_by_count": cited_by.get("total"),
                "cited_by_link": cited_by.get("link"),
            }
        )
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--year-lo", type=int, default=None, help="Earliest publication year")
    parser.add_argument("--year-hi", type=int, default=None, help="Latest publication year")
    args = parser.parse_args()

    api_key = get_serpapi_key()
    if not api_key:
        print(json.dumps({"available": False}))
        return

    query_record = {"query": args.query, "year_lo": args.year_lo, "year_hi": args.year_hi}
    try:
        results = search_google_scholar(api_key, args.query, args.year_lo, args.year_hi)
    except (urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"available": True, "query": query_record, "results": [], "error": str(exc)}))
        return

    print(json.dumps({"available": True, "query": query_record, "results": results}, indent=2))


if __name__ == "__main__":
    main()
