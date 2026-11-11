#!/usr/bin/env python3
"""Convert TEI XML transcriptions into Markdown Source Corpus drafts for corpus-curator.

Usage:
    python3 tei_convert.py convert INPUT WORKDIR [--corpus CORPUS] [--pilot N]
                           [--profile auto|generic|jsp] [--collection NAME]
                           [--formfill rendition|addition] [--default-author NAME]
                           [--edition-year VOL=YYYY ...] [--editorial-date YYYY]
    python3 tei_convert.py write WORKDIR CORPUS [--skip-cause CAUSE ...]
                           [--skip-file TEI_ID ...] [--replace TEI_ID ...]
    python3 tei_convert.py audit WORKDIR CORPUS

convert  reads one TEI file or a folder tree of them and writes, per document,
         WORKDIR/drafts/<slot>/witness.md (the transcription), editorial.md (the
         edition's apparatus, when it has any) and baseline.txt (the transcription's
         text drawn independently from the XML, for the fidelity check). A document
         that is wholly the edition's writing (JSP case introductions and calendars)
         gets editorial.md alone. Keys and
         suffixes are assigned over every input, so a pilot's keys match the later
         bulk run. WORKDIR/manifest.json lists every input; WORKDIR/causes.json
         groups every uncertainty by cause with counts and example files.
         --pilot N keeps drafts only for N inputs chosen to cover the constructs
         present (elements, note kinds, modes, causes).
write    copies ready drafts into their collections, creating CONVENTIONS.md from
         templates/CONVENTIONS.md when absent, never overwriting an existing file
         (unless --replace names its TEI id), and lists written files in
         WORKDIR/written.txt.
audit    runs validate_corpus.py on the written files and fidelity_check on every
         written witness against its baseline, printing only failures and a summary.

Profiles: "generic" handles standard TEI P5 (pb opens a page). "jsp" handles the
Joseph Smith Papers backend XML (undeclared pm:/lds: prefixes, pb closing a page,
docfront apparatus, JSP note types, header metadata). auto picks jsp when the root
TEI element carries pm: or lds: attributes.

Exit status: 0 on success, 1 when audit finds failures, 2 on usage error.
Standard library only.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today()
MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_NUM = {"january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
             "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
             "august": 8, "aug": 8, "september": 9, "sept": 9, "sep": 9, "october": 10,
             "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12}
MON = (r"(?:January|February|March|April|May|June|July|August|September|October|"
       r"November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.?")
SEASON = {"spring": 21, "summer": 22, "fall": 23, "autumn": 23, "winter": 24}
SUFFIXES = [chr(c) for c in range(ord("b"), ord("z") + 1)] + \
           [a + b for a in "abcdefghijklmnopqrstuvwxyz" for b in "abcdefghijklmnopqrstuvwxyz"]
NAME_SUFFIX = {"Jr.", "Sr.", "Jr", "Sr", "II", "III", "IV"}
TITLE_JOINERS = {"to", "of", "and", "for", "the", "in", "at", "by", "with", "from", "on", "a", "an"}
MAX_TITLE_WORDS = 7
LONG_FILE_LINES = 2000

# Causes: "review" causes go to the grouped review; "info" causes go to the report only.
REVIEW, INFO = "review", "info"


def local(name):
    return name.rsplit("}", 1)[-1] if isinstance(name, str) else ""


def attr(el, name, default=None):
    for k, v in el.attrib.items():
        if local(k) == name:
            return v
    return default


def children(el, name):
    return [c for c in el if local(c.tag) == name]


def descendants(el, name):
    return [c for c in el.iter() if local(c.tag) == name]


def first(el, name):
    for c in el.iter():
        if local(c.tag) == name:
            return c
    return None


def flat(el):
    """All text of an element, whitespace collapsed (for header values)."""
    if el is None:
        return ""
    return " ".join("".join(el.itertext()).split())


def nfc(s):
    return unicodedata.normalize("NFC", s)


def escape_text(s):
    """Backslash-escape characters that are syntax in a corpus file (M5, E4)."""
    s = s.replace("\\", "\\\\")
    for ch in "[]{}|*<":
        s = s.replace(ch, "\\" + ch)
    return s


def yaml_value(v):
    v = " ".join(v.split())
    if (": " in v or " #" in v or v.endswith(":") or v[:1] in "[{>|&*!%@`\"'"
            or v.startswith("- ")):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return v


# ---------------------------------------------------------------- parsing

def parse_xml(raw):
    """Parse XML, declaring any namespace prefix the file uses without declaring."""
    live = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    prefixes = set()
    for tag in re.findall(r"<[A-Za-z_][^>]*>", live):
        for m in re.finditer(r"(?:^<|\s)([A-Za-z_][\w.\-]*):[A-Za-z_][\w.\-]*", tag):
            prefixes.add(m.group(1))
    blanked = re.sub(r"<\?.*?\?>|<!--.*?-->|<!DOCTYPE[^>]*>", lambda x: " " * len(x.group(0)), raw, flags=re.S)
    m = re.search(r"<([A-Za-z_][\w.\-:]*)", blanked)
    root_tag = re.match(r"<[^>]*>", blanked[m.start():]).group(0) if m else ""
    # Only declarations on the root cover the whole document.
    declared = set(re.findall(r"xmlns:([\w.\-]+)\s*=", root_tag))
    missing = sorted(prefixes - declared - {"xml", "xmlns"})
    if missing and m:
        decl = " ".join(f'xmlns:{p}="urn:x-undeclared:{p}"' for p in missing)
        raw = raw[:m.end()] + " " + decl + raw[m.end():]
    return ET.fromstring(raw.encode("utf-8")), missing


# ---------------------------------------------------------------- dates

def valid_date(y, m=None, d=None):
    try:
        datetime.date(y, m or 1, d or 1)
        return True
    except ValueError:
        return False


def edtf(y, m=None, d=None, approx=False):
    s = f"{y:04d}"
    if m:
        s += f"-{m:02d}"
        if d:
            s += f"-{d:02d}"
    return s + ("~" if approx else "")


def month(name):
    return MONTH_NUM.get(name.lower().rstrip("."), None) if name else None


def title_date(title):
    """Find the date phrase in a title. Return (edtf, start, end) or None."""
    t = title
    pats = [
        (r"between (?:(\d{1,2}) )?(" + MON + r")?(?: (\d{4}))? and (?:(\d{1,2}) )?(" + MON + r") (\d{4})", "between"),
        (r"\b(\d{1,2})\s?[–-]\s?(\d{1,2}) (" + MON + r") (\d{4})\b", "dayrange"),
        (r"(?:\b(\d{1,2}) )?(" + MON + r")(?: (\d{4}))?\s?[–-]\s?(?:(\d{1,2}) )?(" + MON + r") (\d{4})\b", "range"),
        (r"\b(\d{4})\s?[–-]\s?(\d{4})\b", "years"),
        (r"(ca\. |circa |about )?(?:(Early|Late|Mid-?|Middle) ?)?(?:(Spring|Summer|Fall|Autumn|Winter) )?"
         r"(?:\b(\d{1,2}) )?(?:(" + MON + r") )?\b(\d{4})\b", "single"),
    ]
    for pat, kind in pats:
        m = re.search(pat, t, re.I if kind != "single" else 0)
        if not m:
            continue
        g = m.groups()
        try:
            if kind == "between":
                y2, m2, d2 = int(g[5]), month(g[4]), int(g[3]) if g[3] else None
                y1 = int(g[2]) if g[2] else y2
                m1 = month(g[1]) if g[1] else m2
                d1 = int(g[0]) if g[0] else None
                a, b = edtf(y1, m1, d1), edtf(y2, m2, d2)
                if not (valid_date(y1, m1, d1) and valid_date(y2, m2, d2)):
                    continue
                return f"{a}/{b}", m.start(), m.end()
            if kind == "dayrange":
                y, mo = int(g[3]), month(g[2])
                d1, d2 = int(g[0]), int(g[1])
                if not (valid_date(y, mo, d1) and valid_date(y, mo, d2)) or d1 >= d2:
                    continue
                return f"{edtf(y, mo, d1)}/{edtf(y, mo, d2)}", m.start(), m.end()
            if kind == "range":
                y2, m2 = int(g[5]), month(g[4])
                d2 = int(g[3]) if g[3] else None
                y1 = int(g[2]) if g[2] else y2
                m1, d1 = month(g[1]), int(g[0]) if g[0] else None
                if not (valid_date(y1, m1, d1) and valid_date(y2, m2, d2)):
                    continue
                return f"{edtf(y1, m1, d1)}/{edtf(y2, m2, d2)}", m.start(), m.end()
            if kind == "years":
                y1, y2 = int(g[0]), int(g[1])
                if not 1000 <= y1 < y2 <= 2999:
                    continue
                return f"{y1}/{y2}", m.start(), m.end()
            approx = bool(g[0]) or bool(g[1])
            y = int(g[5])
            if not 1000 <= y <= 2999:
                continue
            if g[2]:
                return f"{y:04d}-{SEASON[g[2].lower()]}" + ("~" if approx else ""), m.start(), m.end()
            mo = month(g[4]) if g[4] else None
            d = int(g[3]) if g[3] and mo else None
            if not valid_date(y, mo, d):
                continue
            return edtf(y, mo, d, approx), m.start(), m.end()
        except (TypeError, ValueError, KeyError):
            continue
    return None


def split_edtf(value):
    core = value.rstrip("~?%")
    bits = core.split("-")
    y = int(bits[0].replace("X", "0"))
    mo = int(bits[1]) if len(bits) > 1 and int(bits[1]) <= 12 else None
    d = int(bits[2]) if len(bits) > 2 else None
    return y, mo, d


def key_date(value):
    """The filename date (N5) for an EDTF value: as much as tells the date, truncating the start."""
    if "/" in value:
        a, b = value.split("/")
        (y1, m1, _), (y2, m2, _) = split_edtf(a), split_edtf(b)
        if y1 != y2:
            return f"{y1}–{y2}"
        if m1 and m1 == m2:
            return f"{y1} {MONTH_ABBR[m1 - 1]}"
        return f"{y1}"
    y, mo, d = split_edtf(value)
    if mo and "-2" in value[4:7] and int(value[5:7]) > 12:
        mo = None
    out = f"{y}"
    if mo:
        out += f" {MONTH_ABBR[mo - 1]}"
        if d:
            out += f" {d}"
    return out


# ---------------------------------------------------------------- names and keys

def allowed_name_char(ch):
    if ch in "',.&-" or ch in "0123456789":
        return True
    cat = unicodedata.category(ch)
    if cat.startswith("M"):
        return True
    return cat.startswith("L") and unicodedata.name(ch, "").startswith("LATIN")


def key_part(s):
    s = nfc(s).replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    s = re.sub(r"[\[\](){}:;\"“”!?/\\|*#@<>_=+~`^$%]", " ", s)
    s = "".join(ch if (ch == " " or allowed_name_char(ch)) else "" for ch in s)
    words = [w.lstrip("-") for w in s.split()]
    words = [w for w in words if w and w not in {",", "."}]
    out = " ".join(words).strip(" ,")
    return out


def invert_name(name):
    """Natural-order personal name to 'Surname, Forename[, Jr.]'."""
    name = " ".join(name.split())
    if name in ("JS", "Joseph Smith", "Joseph Smith Jr.", "Joseph Smith Jr"):
        return "Smith, Joseph, Jr."
    if "," in name:
        return name
    toks = name.split()
    suffix = toks.pop() if len(toks) > 2 and toks[-1] in NAME_SUFFIX else None
    if len(toks) < 2:
        return name
    out = f"{toks[-1]}, {' '.join(toks[:-1])}"
    return out + (f", {suffix}" if suffix else "")


def looks_like_person(s):
    toks = s.split()
    if not 2 <= len(toks) <= 5 or "," in s:
        return False
    return all(t[0].isupper() or t in NAME_SUFFIX for t in toks)


def author_key(authors):
    surnames = [key_part(a.split(",")[0]) for a in authors]
    surnames = [s for s in surnames if s]
    if not surnames:
        return ""
    if len(surnames) == 1:
        return surnames[0]
    if len(surnames) == 2:
        return f"{surnames[0]} and {surnames[1]}"
    return f"{surnames[0]}, et al."


def short_title(head):
    """Short title (N3, N4): key words of the main title, initial article dropped."""
    words = key_part(head).split()
    if len(words) > 1 and words[0].lower() in ("a", "an", "the"):
        words = words[1:]
    shortened = False
    if len(words) > MAX_TITLE_WORDS:
        words = words[:MAX_TITLE_WORDS]
        while words and words[-1].lower().strip(",") in TITLE_JOINERS:
            words.pop()
        shortened = True
    out = " ".join(words).strip(" ,")
    if out and not out[0].isupper() and not out[0].isdigit():
        out = out[0].upper() + out[1:]
    return out, shortened


def fold(s):
    return nfc(s).casefold()


# ---------------------------------------------------------------- emitter

class Emitter:
    """Builds corpus lines from a TEI walk, keeping every mark closed on its own line (M4)."""

    def __init__(self, inline=False):
        self.lines = []
        self.cur = []
        self.stack = []
        self.inline = inline
        self.causes = []

    # -- line state
    def _content(self):
        opens = {id(e["tok"]) for e in self._live()}
        return any(t.strip() and id(t) not in opens for t in self.cur)

    def _mark_has(self):
        for e in self._live():
            e["has"] = True

    def raw(self, token):
        self.cur.append(token)
        self._mark_has()

    def text(self, s):
        if not s:
            return
        s = re.sub(r"\s+", " ", s)
        if s == " ":
            if self.cur and not self.cur[-1].endswith(" "):
                self.cur.append(" ")
            return
        lead = s.startswith(" ")
        body = escape_text(s.strip())
        # "word(abc)" would read as an expansion mark (M2); "](" as a link (M5).
        body = re.sub(r"(^|(?<=[^\W\d_]))\((?=(?:[^\W\d_]+|---)\))", r"\1\\(", body)
        if body.startswith("(") and not lead and self.cur and str(self.cur[-1]).endswith("]"):
            body = "\\" + body
        if any(e["kind"] == "{" for e in self.stack if not e.get("absorbed")):
            body = body.replace("@", "\\@")
        trail = s.endswith(" ")
        if lead:
            top = next((e for e in reversed(self._live())), None)
            if top is not None and not top["has"] and self.cur and self.cur[-1] is top["tok"]:
                self.cur.insert(len(self.cur) - 1, " ")
            elif self.cur and not self.cur[-1].endswith(" "):
                self.cur.append(" ")
        top = next((e for e in reversed(self._live())), None)
        if (top is not None and not top["has"] and top["open"] in ("[", "{")
                and self.cur and self.cur[-1] is top["tok"] and body[:1] in ".?_+-!=@"):
            body = "\\" + body
        self.cur.append(body)
        self._mark_has()
        if trail:
            self.cur.append(" ")

    def _live(self):
        return [e for e in self.stack if not e["paused"] and not e.get("absorbed")]

    def _blockers(self, kind):
        """Open marks that may not enclose a new mark of this kind (M3)."""
        if kind not in "[{":
            return []
        return [e for e in self._live() if e["kind"] == "[" or (kind == "{" and e["kind"] == "{")]

    def _pause(self, blockers):
        for e in blockers:
            self._close_entry(e)
            e["paused"] = True

    def _resume(self, entries):
        for r in entries:
            r["paused"] = False
            r["tok"] = _Tok(r["open"])
            r["has"] = False
            self.cur.append(r["tok"])

    def open(self, opener, closer, kind):
        # Inside an editorial mark, any further mark is absorbed: its text is the editor's.
        # A hand mark inside a hand mark splits the enclosing mark around it instead:
        # {+a <del>b</del> c} becomes {+a}{-b}{+c}.
        if kind in "[{" and any(e["kind"] == "[" for e in self._live()):
            self.stack.append({"absorbed": True, "paused": False, "kind": kind})
            self.causes.append(("mark inside an editorial mark absorbed into it", INFO))
            return
        resumes = self._blockers(kind)
        if resumes:
            self._pause(resumes)
            self.causes.append(("enclosing mark split around a nested mark", INFO))
        tok = _Tok(opener)
        self.stack.append({"paused": False, "kind": kind, "open": opener, "close": closer,
                           "tok": tok, "has": False, "resumes": resumes})
        self.cur.append(tok)

    def retarget(self, opener):
        """After a substitution's '+', reopen continued lines as an addition."""
        if self.stack[-1].get("absorbed"):
            self.text(" ")
            return
        top = self.stack[-1]
        if not top["has"] and self.cur and self.cur[-1] is top["tok"]:
            # The deletion was split around a nested mark; write the rest as an addition.
            self.cur[-1] = top["tok"] = _Tok(opener)
            if len(self.cur) > 1 and not str(self.cur[-2]).endswith(" "):
                self.cur.insert(len(self.cur) - 1, " ")
        else:
            self.cur.append("+")
        top["open"] = opener

    def close(self):
        e = self.stack.pop()
        if e.get("absorbed"):
            return
        self._close_entry(e)
        self._resume(e.get("resumes", []))

    def isolated(self, token, kind):
        """Emit a standalone mark (gap, hand shift, description), splitting enclosing marks it may not sit in."""
        blockers = self._blockers(kind)
        self._pause(blockers)
        self.raw(token)
        self._resume(blockers)

    def _close_entry(self, e):
        if not e["has"]:
            for i in range(len(self.cur) - 1, -1, -1):
                if self.cur[i] is e["tok"]:
                    del self.cur[i]
                    break
            return
        trailing = False
        while self.cur and self.cur[-1] == " ":
            self.cur.pop()
            trailing = True
        self.cur.append(e["close"])
        if trailing:
            self.cur.append(" ")

    def newline(self):
        if self.inline:
            self.text(" ")
            return
        if not self._content():
            return
        live = self._live()
        for e in reversed(live):
            self._close_entry(e)
        line = "".join(str(t) for t in self.cur).strip()
        line = re.sub(r" {2,}", " ", line)
        if line[:1] in "#@" or re.fullmatch(r"(?:[-=_]\s*){3,}", line):
            line = "\\" + line
        self.lines.append(line)
        self.cur = []
        for e in live:
            e["tok"] = _Tok(e["open"])
            e["has"] = False
            self.cur.append(e["tok"])

    def blank(self):
        self.newline()
        if not self.inline and self.lines and self.lines[-1] != "":
            self.lines.append("")

    def milestone(self, label):
        self.newline()
        if self.inline:
            return
        self.lines.append("@" + label)

    def anchor(self):
        return len(self.lines)

    def finish(self):
        self.newline()
        if self._live():
            self.causes.append(("mark left open at end of transcription", REVIEW))
        return self.lines


class _Tok(str):
    """A mark opener; a distinct object so it can be found and removed by identity."""

    def __new__(cls, s):
        return str.__new__(cls, s)


def tidy(lines):
    """Collapse blank-line runs and trim blank ends. Return (lines, old index -> new index)."""
    out, mapping = [], {}
    for i, line in enumerate(lines):
        if line == "" and (not out or out[-1] == ""):
            mapping[i] = max(len(out) - 1, 0)
            continue
        mapping[i] = len(out)
        out.append(line)
    while out and out[-1] == "":
        out.pop()
    for i in mapping:
        mapping[i] = min(mapping[i], max(len(out) - 1, 0))
    mapping[len(lines)] = max(len(out) - 1, 0)
    return out, mapping


# ---------------------------------------------------------------- profiles

class Generic:
    name = "generic"
    pb_closes_page = False
    skip_dirs = set()
    editorial_note_types = {"editorial", "commentary", "annotation", "gloss", "explanatory"}
    drop_note_types = {"internal", "todo"}
    description_note_types = {"description"}

    def __init__(self, opts):
        self.opts = opts

    def transcription_roots(self, root):
        text = first(root, "text")
        if text is None:
            return []
        bodies = children(text, "body")
        return bodies or [text]

    def note_kind(self, note):
        t = (attr(note, "type") or "").strip()
        if t in self.drop_note_types:
            return "drop"
        if t in self.description_note_types:
            return "description"
        if t in self.editorial_note_types or attr(note, "resp") or attr(note, "place") in ("margin-editorial",):
            return "companion"
        return "source"

    def element_kind(self, el):
        return None

    def editorial_document(self, root, meta):
        """True when the whole document is the edition's own writing, with no witness."""
        return False

    def apparatus(self, root):
        """List of (heading, [elements]) sections for the companion file."""
        text = first(root, "text")
        sections = []
        for part, heading in (("front", "Front Matter"), ("back", "Back Matter")):
            el = children(text, part)[0] if text is not None and children(text, part) else None
            if el is not None and flat(el):
                sections.append((heading, [p for p in el.iter() if local(p.tag) in ("p", "ab", "head")] or [el]))
        return sections

    def ref_names(self, root):
        names = {}
        for el in root.iter():
            target, n = attr(el, "target"), attr(el, "n")
            if target and n and "," in n:
                names.setdefault(target, " ".join(n.split()))
            ident = attr(el, "id")
            if ident and local(el.tag) == "handNote" and flat(el):
                names.setdefault(ident, flat(el))
            if ident and local(el.tag) in ("person", "persName"):
                pn = first(el, "persName") if local(el.tag) == "person" else el
                if pn is not None and flat(pn):
                    names.setdefault(ident, flat(pn))
        return names

    def metadata(self, root, path, causes):
        header = first(root, "teiHeader")
        ts = first(header, "titleStmt") if header is not None else None
        title = flat(first(ts, "title")) if ts is not None else ""
        if not title:
            title = os.path.splitext(os.path.basename(path))[0]
            causes.append(("title not in header; file name used", REVIEW))
        authors = [invert_name(flat(a)) for a in (children(ts, "author") if ts is not None else []) if flat(a)]
        date = None
        sd = first(header, "sourceDesc") if header is not None else None
        for d in (descendants(sd, "date") if sd is not None else []):
            w = attr(d, "when") or attr(d, "when-iso")
            if w and re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", w):
                date = w
                break
            nb, na = attr(d, "notBefore"), attr(d, "notAfter")
            if nb and na:
                date = f"{nb}/{na}"
                break
        if date is None:
            td = title_date(title)
            if td:
                date = td[0]
                causes.append(("date taken from title", REVIEW))
        lang = None
        lu = first(header, "language") if header is not None else None
        if lu is not None and attr(lu, "ident"):
            lang = attr(lu, "ident")
        text = first(root, "text")
        if not lang and text is not None:
            lang = attr(text, "lang")
        if not lang:
            lang = "en"
            causes.append(("language not encoded; en assumed", REVIEW))
        src = flat(first(sd, "bibl")) if sd is not None and first(sd, "bibl") is not None else ""
        msid = first(sd, "msIdentifier") if sd is not None else None
        if not src and msid is not None:
            src = ", ".join(flat(c) for c in msid if flat(c))
        if not src:
            causes.append(("source citation not in header", REVIEW))
        ident = attr(root, "id") or os.path.splitext(os.path.basename(path))[0]
        pub = first(header, "publicationStmt") if header is not None else None
        edition = flat(first(pub, "publisher")) if pub is not None else ""
        source = "; ".join(x for x in (src, f"TEI transcription{', ' + edition if edition else ''}, TEI {ident}") if x)
        bare = re.sub(r"\s*\[[^\]]*\]", "", title).strip()
        td = title_date(bare)
        head = (bare[:td[1]].rstrip(" ,;") or bare[td[2]:].strip(" ,;")) if td else bare
        printed = any(attr(pb, "type") == "print" for pb in descendants(root, "pb"))
        dtype, certain = self.doc_type(None, head, printed)
        if not certain:
            causes.append((f"type inferred as {dtype}", REVIEW))
        return {"title": title, "authors": authors, "date": date, "lang": lang, "source": source,
                "type": dtype, "tei_id": ident, "sortkey": f"{date or '9999'} {path}",
                "head": head, "edition_ref": edition}

    def doc_type(self, series, head, printed):
        h = head.lower()
        if h.startswith(("letter", "letters")):
            return "letter", True
        if h.startswith("minutes"):
            return "minutes", True
        if h.startswith(("journal", "diary")):
            return "diary", True
        if printed:
            return "article", False
        return "manuscript", False

    def collection(self, path, input_root):
        if self.opts.collection:
            return self.opts.collection
        base = os.path.basename(input_root.rstrip(os.sep)) if os.path.isdir(input_root) \
            else os.path.basename(os.path.dirname(input_root))
        return key_part(base) or "TEI Imports"

    def editorial_date(self, root, meta, causes):
        header = first(root, "teiHeader")
        pub = first(header, "publicationStmt") if header is not None else None
        for d in (descendants(pub, "date") if pub is not None else []):
            w = attr(d, "when") or flat(d)
            m = re.search(r"\b(1[5-9]\d\d|20\d\d)\b", w or "")
            if m:
                return m.group(1)
        return None

    def editorial_source(self, meta):
        return f"{meta['edition_ref'] or 'TEI edition'}, apparatus for {meta['title']}, TEI {meta['tei_id']}"

    def resp_source(self):
        return "TEI transcription"

    # `layer` of the witness text (F-table): a generic TEI edition's text is a
    # transcription unless the profile knows the edition verified it
    witness_layer = "transcription"


class JSP(Generic):
    name = "jsp"
    pb_closes_page = True
    skip_dirs = {"collated", "paratext"}
    series_names = ["Administrative Records", "Documents", "Financial Records", "Histories",
                    "Journals", "Legal Records", "Revelations and Translations"]
    companion_types = {"editorial-footnote", "editorial-footnote-scribe", "editorial-footnote-text",
                       "toe-note", "intratextual-note"}
    drop_types = {"internal-note", "formatting-note", "errata", "comment-external", "annotative"}
    description_types = {"editorial-comment"}
    # Print-volume publication years confirmed for The Joseph Smith Papers; others come
    # from --edition-year or the posting date.
    volume_years = {"D1": 2013, "D2": 2013, "D3": 2014, "D4": 2016, "D5": 2017, "D6": 2017,
                    "D7": 2018, "D8": 2019, "D9": 2019, "D10": 2020, "J1": 2008, "J2": 2011,
                    "J3": 2015, "H1": 2012, "H2": 2012, "R1": 2009, "MRB": 2009, "R2": 2011,
                    "A1": 2016, "CFM": 2016}

    def transcription_roots(self, root):
        return [d for d in root.iter() if local(d.tag).startswith("div") and attr(d, "type") == "docbody"]

    def note_kind(self, note):
        t = (attr(note, "type") or "").strip()
        if t == "authorial-footnote":
            return "source"
        if t in self.companion_types:
            return "companion"
        if t in self.drop_types:
            return "drop"
        if t in self.description_types:
            return "description"
        return "unknown"

    def element_kind(self, el):
        if local(el.tag) == "ab" and attr(el, "type") == "journal-entry-divider":
            return "description"
        if local(el.tag) == "EventGroup":
            return "drop"
        return None

    def editorial_document(self, root, meta):
        # Case introductions and calendars: JSP prose in the docbody slot, marked by EventGroup.
        return (first(root, "EventGroup") is not None
                or meta["title"].startswith(("Introduction to ", "Calendar of Documents")))

    def apparatus(self, root):
        sections = []
        for d in root.iter():
            if not local(d.tag).startswith("div"):
                continue
            t = attr(d, "type")
            if t == "sourcenote":
                ps = [p for s in descendants(d, "summary") for p in (children(s, "p") or [s])]
                if any(flat(p) for p in ps):
                    sections.append(("Source Note", ps))
            elif t == "historical-intro":
                ps = children(d, "p")
                if any(flat(p) for p in ps):
                    sections.append(("Historical Introduction", ps))
        return sections

    def series(self, path):
        parts = os.path.abspath(path).split(os.sep)
        for name in self.series_names:
            if name in parts:
                return name
        return None

    def collection(self, path, input_root):
        if self.opts.collection:
            return self.opts.collection
        s = self.series(path)
        return f"JSP {s}" if s else super().collection(path, input_root)

    def metadata(self, root, path, causes):
        names = self.ref_names(root)
        raw_title = attr(root, "docDesc") or flat(first(first(root, "titleStmt"), "title"))
        title = re.sub(r"^LIVE FILE IN [A-Z0-9]+[_,]?\s*", "", raw_title).strip()
        if title != raw_title:
            causes.append(("JSP staff prefix removed from title", INFO))
        if not title:
            title = os.path.splitext(os.path.basename(path))[0]
            causes.append(("title missing; file name used", REVIEW))
        series = self.series(path)

        # Authors: header first, then the title's "Type, A to B" or "X from A".
        authors = []
        lp = first(root, "listPerson")
        for person in (children(lp, "person") if lp is not None else []):
            if attr(person, "role") != "author":
                continue
            ref = first(person, "ref")
            target = attr(ref, "target") if ref is not None else None
            n = attr(ref, "n") if ref is not None else None
            name = names.get(target) or (n if n and "," in n else None) or invert_name(n or flat(person))
            if name and name not in authors:
                authors.append(" ".join(name.split()))

        bare = re.sub(r"\s*\[[^\]]*\]", "", title).strip()
        td = title_date(bare)
        head = bare[:td[1]].rstrip(" ,;") if td else bare
        if td and not head:
            head = bare[td[2]:].strip(" ,;")
        short_head = head
        m = re.match(r"^([^,]+), (.+?) to (.+)$", head)
        if m and looks_like_person(m.group(2)):
            short_head = f"{m.group(1)} to {m.group(3)}"
            if not authors:
                authors = [invert_name(m.group(2))]
                causes.append(("author inferred from title", INFO))
        elif not authors:
            m2 = re.match(r"^(.+?) from (.+)$", head)
            if m2 and looks_like_person(m2.group(2)):
                authors = [invert_name(m2.group(2))]
                causes.append(("author inferred from title", INFO))
        if not authors:
            if self.opts.default_author:
                authors = [self.opts.default_author]
                causes.append((f"default author applied: {self.opts.default_author}", INFO))
            else:
                causes.append(("author not stated (key will omit author)", REVIEW))

        # Date: the title's phrase gives precision; docDate is the fallback.
        doc_date = attr(root, "docDate")
        dmin, dmax = attr(root, "docDateMin"), attr(root, "docDateMax")
        date = td[0] if td else None
        if date is None:
            if dmin and dmax and dmin != dmax:
                a, b = sorted([dmin, dmax])
                date = f"{a}/{b}"
            elif doc_date and re.fullmatch(r"\d{4}-\d{2}-\d{2}", doc_date):
                date = doc_date
            if date:
                causes.append(("date from JSP date fields; precision unverified", REVIEW))
            else:
                causes.append(("no date found", REVIEW))
        elif doc_date and doc_date[:4].isdigit() and split_edtf(date.split("/")[0])[0] != int(doc_date[:4]) \
                and "/" not in date:
            causes.append(("title date and JSP docDate disagree on the year", REVIEW))

        # Source citation.
        msid = first(root, "msIdentifier")
        ms_name = flat(first(msid, "msName")) if msid is not None else ""
        call = ""
        for idno in (descendants(msid, "idno") if msid is not None else []):
            if attr(idno, "type") == "call-number" and flat(idno):
                call = flat(idno)
        repo = flat(first(msid, "repository")) if msid is not None else ""
        repo = "" if repo.lower() in ("unknown", "") else repo
        printref = ""
        for lb in root.iter():
            if local(lb.tag) == "listBibl" and attr(lb, "type") == "print-volume-location":
                printref = flat(lb)
        printref = printref if re.match(r"^JSP,?\s*[A-Z]+\d*", printref) else ""
        loc = ", ".join(x for x in (ms_name, call, repo) if x)
        if not repo:
            causes.append(("source lacks a repository", REVIEW))
        ident = attr(root, "id") or os.path.splitext(os.path.basename(path))[0]
        ed = f"The Joseph Smith Papers{' (' + printref + ')' if printref else ''}"
        source = f"{loc + '; ' if loc else ''}transcription in {ed}, JSP TEI {ident}"

        lang_el = first(root, "textLang")
        lang = attr(lang_el, "mainLang") if lang_el is not None else None
        if not lang:
            lang = "en"
            causes.append(("language not encoded; en assumed", INFO))

        printed = any(attr(pb, "type") == "print" for pb in descendants(root, "pb"))
        dtype, certain = self.doc_type(series, head, printed)
        if not certain:
            causes.append((f"type inferred as {dtype}", REVIEW))

        return {"title": title, "authors": authors, "date": date, "lang": lang, "source": source,
                "type": dtype, "tei_id": ident, "sortkey": attr(root, "sortkey") or f"{date} {path}",
                "head": short_head, "edition_ref": printref, "series": series}

    def doc_type(self, series, head, printed):
        h = head.lower()
        if h.startswith(("letter", "letters")):
            return "letter", True
        if h.startswith("minutes"):
            return "minutes", True
        if series == "Journals" or h.startswith("journal"):
            return "diary", True
        if series == "Legal Records":
            return "legal", True
        if series in ("Financial Records", "Administrative Records"):
            return "record", True
        if printed:
            return "article", False
        return "manuscript", False

    def editorial_date(self, root, meta, causes):
        vol = re.match(r"^JSP,?\s*([A-Z]+\d*)", meta.get("edition_ref") or "")
        if vol:
            v = vol.group(1)
            if v in self.opts.edition_years:
                return self.opts.edition_years[v]
            if v in self.volume_years:
                return str(self.volume_years[v])
            causes.append((f"publication year unknown for JSP volume {v}", REVIEW))
        for ch in descendants(root, "change"):
            label = flat(first(ch, "label"))
            if label.lower().startswith("posted"):
                m = re.search(r"\b(20\d\d)\b", flat(first(ch, "desc")))
                if m:
                    return m.group(1)
        years = [attr(ch, "when")[:4] for ch in descendants(root, "change") if (attr(ch, "when") or "")[:4].isdigit()]
        if years:
            causes.append(("editorial date from revision history", INFO))
            return max(years)
        return None

    def editorial_source(self, meta):
        where = meta["edition_ref"] or "josephsmithpapers.org"
        return f"The Joseph Smith Papers, {where}, source note and annotation for {meta['title']}, JSP TEI {meta['tei_id']}"

    def resp_source(self):
        return "Joseph Smith Papers TEI transcription"

    witness_layer = "edition"


# ---------------------------------------------------------------- conversion

class Draft:
    pass


HI_MAP = {"superscript": "sup", "subscript": "sub", "underscore": "underline", "underline": "underline",
          "small-caps": "sc", "smallcaps": "sc", "shading": "shading", "double-underline": "underline2"}
LAYOUT_RENDS = {"normal", "right", "left", "center", "indent", "noindent", "hangindent",
                "icon-glyph", "icon-email", "no-indent"}


class Converter:
    def __init__(self, profile, root, mode, names=None):
        self.p = profile
        self.root = root
        self.mode = mode
        self.e = Emitter()
        self.causes = []
        self.dropped = {}
        self.companion_notes = []   # (note element, emitter line index)
        self.source_notes = []      # rendered definitions for the witness
        self.hands = {}             # scribe id -> label
        self.hand_names = {}
        self.cur_hand = None
        self.names = names if names is not None else profile.ref_names(root)
        self.pbs = []
        self.pb_index = 0
        self.span_end = None
        self.elements = set()

    def cause(self, text, level=REVIEW):
        self.causes.append((text, level))

    # -- pages
    def page_label(self, pb, ordinal):
        n = re.sub(r"[^A-Za-z0-9.\-]", "", attr(pb, "n") or "")
        if not n or not n[0].isalnum():
            self.cause("page break without a usable label; ordinal used", REVIEW)
            n = str(ordinal)
        return "p" + n

    def hand(self, scribe):
        if scribe not in self.hands:
            taken = set(self.hands.values())
            if re.fullmatch(r"h\d+", scribe) and scribe not in taken:
                label = scribe
            else:
                n = len(self.hands) + 1
                while f"h{n}" in taken:
                    n += 1
                label = f"h{n}"
            self.hands[scribe] = label
            self.hand_names[label] = self.names.get(scribe) or f"unidentified hand ({scribe})"
        return self.hands[scribe]

    # -- walk
    def run(self, roots):
        for r in roots:
            self.pbs.extend(descendants(r, "pb"))
        if self.p.pb_closes_page and self.pbs:
            self.e.milestone(self.page_label(self.pbs[0], 1))
        for r in roots:
            self.walk_children(r)
            self.e.blank()
        lines = self.e.finish()
        self.causes.extend(self.e.causes)
        return lines

    def walk_children(self, el):
        if el.text:
            self.e.text(el.text)
        kids = list(el)
        i = 0
        while i < len(kids):
            c = kids[i]
            nxt = kids[i + 1] if i + 1 < len(kids) else None
            if (local(c.tag) == "del" and nxt is not None and local(nxt.tag) == "add"
                    and not (c.tail or "").strip() and attr(nxt, "type") != "formfill"):
                self.substitution(c, nxt)
                if nxt.tail:
                    self.e.text(nxt.tail)
                i += 2
                continue
            self.walk(c)
            if c.tail:
                self.e.text(c.tail)
            i += 1

    def hand_suffix(self, el, place=True):
        bits = []
        if attr(el, "hand"):
            bits.append(self.hand(attr(el, "hand").lstrip("#")))
        pl = attr(el, "place")
        if place and pl and pl not in ("inline",):
            bits.append(re.sub(r"[^A-Za-z0-9 \-]", "", pl.replace("-", " ")))
        return ("@" + " ".join(bits)) if bits else ""

    def substitution(self, d, a):
        self.elements.update({"del", "add"})
        e = self.e
        e.open("{-", self.hand_suffix(a) + "}", "{")
        self.walk_children(d)
        e.retarget("{+")
        self.walk_children(a)
        e.close()

    def walk(self, el):
        tag = local(el.tag)
        e = self.e
        if not isinstance(el.tag, str):
            return
        self.elements.add(tag)
        kind = self.p.element_kind(el)
        if kind == "drop":
            self.dropped[tag] = self.dropped.get(tag, 0) + 1
            return
        if kind == "description":
            text = " ".join(prose(el, lambda n: "").split())
            if text:
                e.newline()
                self.description("entry", text)
                e.newline()
            return

        if tag == "lb":
            e.newline()
        elif tag == "pb":
            self.pb_index += 1
            if self.p.pb_closes_page:
                if self.pb_index < len(self.pbs):
                    e.milestone(self.page_label(self.pbs[self.pb_index], self.pb_index + 1))
                elif self.text_after(el):
                    e.newline()
                    self.cause("text follows the final page-closing break", REVIEW)
            else:
                e.milestone(self.page_label(el, self.pb_index))
        elif tag in ("p", "ab", "div", "div1", "div2", "div3", "div4", "body", "floatingText", "lg",
                     "list", "head", "closer", "opener", "salute", "signed", "dateline", "postscript"):
            e.blank() if tag in ("p", "ab", "div", "div1", "div2", "div3", "div4", "lg", "list",
                                 "floatingText", "postscript") else e.newline()
            self.walk_children(el)
            e.blank() if tag in ("p", "ab", "lg", "list", "postscript") else e.newline()
        elif tag in ("l", "item", "row"):
            e.newline()
            self.walk_children(el)
            e.newline()
        elif tag == "table":
            self.table(el)
        elif tag == "hi":
            rends = (attr(el, "rend") or "").split()
            marks = [r for r in rends if r not in LAYOUT_RENDS]
            if not marks:
                self.walk_children(el)
            elif marks[0] == "italic":
                self.emphasis(el, "*")
            elif marks[0] == "bold":
                self.emphasis(el, "**")
            elif marks[0] in ("strikethrough", "strike-through"):
                e.open("{-", "}", "{")
                self.walk_children(el)
                e.close()
            else:
                value = HI_MAP.get(marks[0], re.sub(r"[^A-Za-z0-9]", "", marks[0]))
                if marks[0] not in HI_MAP:
                    self.cause(f"rendition '{marks[0]}' written as @{value}", INFO)
                e.open("{", f"@{value}}}", "{")
                self.walk_children(el)
                e.close()
        elif tag == "del":
            dt = attr(el, "type") or ""
            value = "@erasure" if dt in ("wipe-out", "knife-erase", "erasure") else ""
            if dt == "not-crossed-out":
                self.cause("deletion marked 'not-crossed-out' written as a deletion", REVIEW)
            e.open("{-", value + "}", "{")
            self.walk_children(el)
            e.close()
        elif tag == "add":
            if attr(el, "type") == "formfill" and self.p.opts.formfill == "rendition":
                hand = self.hand_suffix(el, place=False)
                closer = "@formfill " + hand[1:] + "}" if hand else "@formfill}"
                e.open("{", closer, "{")
            else:
                e.open("{+", self.hand_suffix(el) + "}", "{")
            self.walk_children(el)
            e.close()
        elif tag == "subst":
            dels, adds = children(el, "del"), children(el, "add")
            if len(dels) == 1 and len(adds) == 1 and list(el).index(dels[0]) < list(el).index(adds[0]):
                self.substitution(dels[0], adds[0])
            else:
                self.walk_children(el)
        elif tag == "addSpan":
            if self.span_end:
                self.cause("overlapping addSpan ranges", REVIEW)
            else:
                self.span_end = attr(el, "spanTo", "").lstrip("#")
                e.open("{+", self.hand_suffix(el) + "}", "{")
        elif tag == "anchor":
            if self.span_end and attr(el, "id") == self.span_end:
                e.close()
                self.span_end = None
        elif tag == "supplied":
            reason = attr(el, "reason") or ""
            low = attr(el, "cert") in ("low", "medium")
            opener = "[+" if reason == "omitted" else "["
            e.open(opener, "?]" if low else "]", "[")
            self.walk_children(el)
            e.close()
        elif tag == "unclear":
            e.open("[?", "]", "[")
            self.walk_children(el)
            e.close()
        elif tag == "sic":
            e.open("[!", "]", "[")
            self.walk_children(el)
            e.close()
        elif tag == "choice":
            self.choice(el)
        elif tag == "gap":
            unit = attr(el, "unit") or ""
            qty = attr(el, "quantity") or attr(el, "extent") or ""
            n = qty if unit in ("chars", "char", "characters") and qty.isdigit() else "?"
            reason = attr(el, "reason") or ""
            e.isolated(f"[?.{n}]" if reason in ("illegible", "") else f"[.{n}]", "[")
        elif tag == "space":
            unit, qty = attr(el, "unit") or "", attr(el, "quantity") or attr(el, "extent") or ""
            if attr(el, "dim") == "vertical" or unit == "lines":
                e.blank()
            elif qty.isdigit():
                e.isolated(f"[_{qty}]", "[")
        elif tag == "handShift":
            scribe = (attr(el, "scribe") or attr(el, "new") or "").lstrip("#")
            if scribe and scribe != self.cur_hand:
                e.isolated("{@" + self.hand(scribe) + "}", "{")
                self.cur_hand = scribe
        elif tag == "note":
            self.note(el)
        elif tag == "fw":
            value = "catchword" if attr(el, "type") == "catchwords" else re.sub(r"[^A-Za-z]", "", attr(el, "type") or "fw")
            e.open("{", f"@{value}}}", "{")
            self.walk_children(el)
            e.close()
        elif tag == "seg" and attr(el, "type") == "shorthand":
            e.open("{", "@shorthand}", "{")
            self.walk_children(el)
            e.close()
        elif tag == "foreign" and attr(el, "lang"):
            e.open("{", "@" + re.sub(r"[^A-Za-z\-]", "", attr(el, "lang")) + "}", "{")
            self.walk_children(el)
            e.close()
        elif tag in ("ref", "persName", "placeName", "orgName", "date", "title", "name", "rs", "country",
                     "term", "num", "measure", "seg", "g", "orig", "abbr", "foreign",
                     "w", "c", "q", "quote", "said", "emph", "mentioned", "address", "addrLine",
                     "settlement", "region", "geogName", "roleName", "forename", "surname", "time"):
            self.walk_children(el)
        elif tag in ("reg", "expan"):
            e.open("[", "]", "[")
            self.walk_children(el)
            e.close()
        elif tag == "corr":
            e.open("[+", "]", "[")
            self.walk_children(el)
            e.close()
        elif tag in ("col",):
            pass
        else:
            self.cause(f"unmapped element <{tag}> kept as plain text", REVIEW)
            self.walk_children(el)

    def text_after(self, el):
        seen = False
        for node in self.root.iter():
            if node is el:
                seen = True
                if (el.tail or "").strip():
                    return True
                continue
            if seen and local(node.tag) != "note" and (node.text or "").strip():
                return True
        return False

    def emphasis(self, el, delim):
        e = self.e
        e.open(delim, delim, "*")
        self.walk_children(el)
        e.close()

    def choice(self, el):
        kind, reading = choice_reading(el)
        e = self.e
        if kind == "sic+corr":
            corr = next(c for c in el if local(c.tag) == "corr")
            e.isolated("[!" + escape_text(" ".join("".join(reading.itertext()).split())) + ">"
                       + escape_text(" ".join("".join(corr.itertext()).split())) + "]", "[")
        elif kind == "sic":
            self.walk(reading)
        elif reading is not None:
            if kind == "first":
                self.cause("choice without sic, orig, abbr or an Expanded reading kept as its first reading", REVIEW)
            self.walk_children(reading)

    def description(self, label, text):
        self.e.isolated(f"[={label}: {text}]", "[")

    def note(self, el):
        kind = self.p.note_kind(el)
        t = attr(el, "type") or "untyped"
        if kind == "unknown":
            self.cause(f"note type '{t}' sent to the editorial companion", REVIEW)
            kind = "companion"
        if kind == "drop":
            self.dropped[t] = self.dropped.get(t, 0) + 1
        elif kind == "description":
            text = " ".join(prose(el, lambda n: "").split())
            if text:
                self.description("comment", text)
        elif kind == "companion":
            self.companion_notes.append((el, self.e.anchor()))
        else:
            n = len(self.source_notes) + 1
            self.source_notes.append(f"[^{n}]: " + " ".join(prose(el, lambda n: "").split()))
            self.e.raw(f"[^{n}]")

    def table_rows(self, el):
        rows = []
        for c in el:
            t = local(c.tag)
            if t in ("tr", "row"):
                rows.append(c)
            elif t in ("thead", "tbody", "tfoot"):
                rows.extend(r for r in c if local(r.tag) in ("tr", "row"))
        return rows

    def table(self, el):
        trs = self.table_rows(el)
        if self.e.inline:
            # A table nested in a table cell: its cells run on inside the outer cell.
            self.cause("table nested in a table cell written inline", INFO)
            for tr in trs:
                for td in tr:
                    if local(td.tag) in ("td", "cell"):
                        self.walk_children(td)
                        self.e.text(" ")
            return
        self.cause("table converted to a GFM table", INFO)
        rows, notes = [], []
        for tr in trs:
            cells = []
            for td in tr:
                if local(td.tag) not in ("td", "cell"):
                    continue
                sub = Converter(self.p, self.root, self.mode, names=self.names)
                sub.e = Emitter(inline=True)
                sub.hands, sub.hand_names = self.hands, self.hand_names
                sub.pbs, sub.pb_index = self.pbs, self.pb_index
                sub.cur_hand = self.cur_hand
                sub.walk_children(td)
                if sub.span_end:
                    sub.e.close()
                    sub.span_end = None
                    self.cause("addition span crossing table cells closed at the cell end", REVIEW)
                for entry in reversed(sub.e._live()):
                    sub.e._close_entry(entry)
                text = re.sub(r" {2,}", " ", "".join(str(t) for t in sub.e.cur).strip())
                self.causes.extend(sub.causes + sub.e.causes)
                notes.extend((n, len(rows)) for n, _ in sub.companion_notes)
                self.source_notes.extend(sub.source_notes)
                for k, v in sub.dropped.items():
                    self.dropped[k] = self.dropped.get(k, 0) + v
                if descendants(td, "lb"):
                    self.cause("line breaks inside a table cell joined", INFO)
                cells.append(text)
            if cells:
                rows.append(cells)
        if not rows:
            return
        width = max(len(r) for r in rows)
        self.e.blank()
        start = len(self.e.lines)
        for i, r in enumerate(rows):
            r = r + [""] * (width - len(r))
            self.e.lines.append("| " + " | ".join(r) + " |")
            if i == 0:
                self.e.lines.append("| " + " | ".join(["---"] * width) + " |")
        for n, ri in notes:
            self.companion_notes.append((n, start + ri + (1 if ri else 0)))
        self.e.lines.append("")


def choice_reading(el):
    """The reading of a <choice> that the witness shows: the source's form, or JSP's Expanded text."""
    kids = [c for c in el if isinstance(c.tag, str)]
    by = {}
    for c in kids:
        by.setdefault(local(c.tag), c)
    if "sic" in by and "corr" in by:
        return "sic+corr", by["sic"]
    for tag in ("orig", "abbr"):
        if tag in by:
            return tag, by[tag]
    if "sic" in by:
        return "sic", by["sic"]
    for c in kids:
        if local(c.tag) == "reg" and attr(c, "type") == "Expanded":
            return "expanded", c
    return "first", kids[0] if kids else None


def prose(el, note_cb, skip_root_tail=True):
    """Flatten an apparatus element to one escaped Markdown line."""
    out = []

    def walk(node):
        tag = local(node.tag)
        if not isinstance(node.tag, str):
            return
        if tag == "note" and node is not el:
            out.append(note_cb(node))
            return
        if tag in ("lb",):
            out.append(" ")
        italic = tag == "title" or (tag == "hi" and "italic" in (attr(node, "rend") or ""))
        bracket = tag == "supplied"
        inner = []
        saved = out[:]
        out.clear()
        if node.text:
            out.append(escape_text(node.text))
        for c in node:
            walk(c)
            if c.tail:
                out.append(escape_text(c.tail))
        inner = "".join(out)
        out.clear()
        out.extend(saved)
        squeezed = " ".join(inner.split())
        if italic and squeezed:
            lead = " " if inner[:1].isspace() else ""
            trail = " " if inner[-1:].isspace() else ""
            out.append(f"{lead}*{squeezed}*{trail}")
        elif bracket and squeezed:
            out.append(f"\\[{squeezed}\\]")
        else:
            out.append(inner)

    walk(el)
    return re.sub(r"\s+", " ", "".join(out)).strip()


def baseline(roots, profile):
    """The transcription's source text, drawn from the XML independently of the emitter."""
    out = []
    block = {"p", "ab", "div", "div1", "div2", "div3", "div4", "head", "l", "item", "tr", "row",
             "table", "lg", "list", "floatingText", "body", "closer", "opener", "salute", "signed",
             "dateline", "postscript"}
    skip = {"note", "supplied", "corr", "reg", "expan", "anchor", "handShift", "col"}

    def walk(el):
        tag = local(el.tag)
        if not isinstance(el.tag, str):
            return
        if profile.element_kind(el) == "drop":
            return
        if profile.element_kind(el) == "description" or (tag == "note" and profile.note_kind(el) == "description"):
            out.append(" ")
            return
        if tag in skip:
            # Edge spaces inside skipped text still separate words, as the witness view shows.
            inner = "".join(el.itertext()) if tag != "note" else ""
            if inner[:1].isspace():
                out.append(" ")
            for d in el.iter():
                if local(d.tag) == "lb" and tag != "note":
                    out.append("\n")
                elif local(d.tag) == "pb" and tag != "note":
                    out.append("\n\f")
            if inner[-1:].isspace() or (tag != "note" and any(
                    local(d.tag) == "note" and profile.note_kind(d) == "description" for d in el.iter())):
                out.append(" ")
            return
        if tag == "choice":
            kind, reading = choice_reading(el)
            if reading is not None:
                if reading.text:
                    out.append(re.sub(r"\s+", " ", reading.text))
                for c in reading:
                    walk(c)
                    if c.tail:
                        out.append(re.sub(r"\s+", " ", c.tail))
            return
        if tag == "subst" and len(children(el, "del")) == 1 and len(children(el, "add")) == 1:
            # The substitution reads "old new"; whitespace inside <subst> is formatting.
            walk(children(el, "del")[0])
            out.append(" ")
            walk(children(el, "add")[0])
            return
        if tag in ("gap", "space"):
            out.append(" ")
            return
        if tag == "lb":
            out.append("\n")
        elif tag == "pb":
            out.append("\n\f")
        if el.text:
            out.append(re.sub(r"\s+", " ", el.text))
        kids = list(el)
        for i, c in enumerate(kids):
            walk(c)
            if c.tail:
                out.append(re.sub(r"\s+", " ", c.tail))
            elif (local(c.tag) == "del" and i + 1 < len(kids) and local(kids[i + 1].tag) == "add"
                  and attr(kids[i + 1], "type") != "formfill"):
                out.append(" ")
        if tag in block:
            out.append("\n")
        elif tag in ("td", "cell"):
            out.append(" ")

    for r in roots:
        walk(r)
        out.append("\n")
    for r in roots:
        for n in descendants(r, "note"):
            if profile.note_kind(n) == "source":
                out.append(re.sub(r"\s+", " ", "".join(n.itertext())) + "\n")
    text = nfc("".join(out))
    lines = [" ".join(x.split()) for x in text.split("\n")]
    return "\n".join(x for x in lines if x).replace("\n\f", "\f") + "\n"


# ---------------------------------------------------------------- per-document

def convert_one(path, input_root, profile, mode_override=None):
    raw = open(path, encoding="utf-8-sig").read()
    d = Draft()
    d.input = path
    d.causes = []
    try:
        root, undeclared = parse_xml(raw)
    except ET.ParseError as exc:
        d.status, d.reason = "failed", f"XML parse error: {exc}"
        return d
    if undeclared:
        d.causes.append(("undeclared namespace prefixes declared for parsing", INFO))
    if local(root.tag) != "TEI":
        d.status, d.reason = "skipped", f"root element is <{local(root.tag)}>, not one TEI document"
        return d
    roots = profile.transcription_roots(root)
    if not roots or not any(flat(r) for r in roots):
        state = attr(first(root, "Tracking") if first(root, "Tracking") is not None else root, "TranscriptState")
        d.status, d.reason = "skipped", "edition has no transcription text" + (f" (TranscriptState {state})" if state else "")
        return d
    meta = profile.metadata(root, path, d.causes)
    d.collection = profile.collection(path, input_root)
    d.editorial_collection = d.collection + " Editorial"
    d.profile, d.meta, d.dropped = profile, meta, {}
    if profile.editorial_document(root, meta):
        return editorial_only(d, root, roots, profile)
    mode = "diplomatic" if any(descendants(r, "lb") for r in roots) else "prose"
    conv = Converter(profile, root, mode)
    lines = conv.run(roots)
    d.causes.extend(conv.causes)
    body, mapping = tidy(lines)
    d.body = body
    d.mapping = mapping
    d.source_notes = conv.source_notes
    d.companion_notes = conv.companion_notes
    d.dropped = conv.dropped
    d.hands = conv.hand_names
    d.mode = mode
    d.meta = meta
    d.elements = sorted(conv.elements)
    d.baseline = baseline(roots, profile)
    d.editorial_only = False
    d.apparatus = profile.apparatus(root)
    d.has_editorial = bool(d.apparatus or d.companion_notes)
    d.editorial_year = profile.editorial_date(root, meta, d.causes) if d.has_editorial else None
    if d.has_editorial and not d.editorial_year:
        if profile.opts.editorial_date:
            d.editorial_year = profile.opts.editorial_date
            d.causes.append((f"editorial date set by option: {d.editorial_year}", INFO))
        else:
            d.causes.append(("editorial date unknown; companion held back", REVIEW))
    if not meta["date"]:
        d.status, d.reason = "held", "no date; key cannot be built"
    else:
        d.status, d.reason = "ready", ""
    if len(body) > LONG_FILE_LINES:
        d.causes.append((f"witness over {LONG_FILE_LINES} lines; consider splitting at the work's volumes or parts", REVIEW))
    d.profile = profile
    return d


def blocks(roots):
    """Paragraph-level elements of a transcription, outside notes."""
    out = []

    def walk(el):
        tag = local(el.tag)
        if tag == "note":
            return
        if tag in ("p", "ab", "head", "item", "l"):
            out.append(el)
            return
        for c in el:
            walk(c)

    for r in roots:
        walk(r)
    return out


def editorial_only(d, root, roots, profile):
    """A document that is wholly the edition's writing goes to the editorial collection alone."""
    d.editorial_only = True
    d.causes = [(c, lvl) for c, lvl in d.causes
                if not c.startswith(("author not stated", "type inferred", "no date found", "date from JSP", "source lacks"))]
    d.causes.append(("edition-written document (introduction or calendar) sent to the editorial collection", INFO))
    d.body, d.mapping, d.source_notes, d.companion_notes = [], {}, [], []
    d.hands, d.mode, d.elements, d.baseline = {}, "prose", ["editorial-document"], ""
    d.apparatus = profile.apparatus(root) + [(None, blocks(roots))]
    d.has_editorial = True
    d.fm_lines = 0
    d.editorial_year = profile.editorial_date(root, d.meta, d.causes)
    if not d.editorial_year and profile.opts.editorial_date:
        d.editorial_year = profile.opts.editorial_date
    d.status, d.reason = ("ready", "") if d.editorial_year else ("held", "editorial date unknown")
    if not d.editorial_year:
        d.causes.append(("editorial date unknown; companion held back", REVIEW))
    return d


def witness_text(d, key):
    m = d.meta
    fm = [("title", m["title"])]
    if m["authors"]:
        fm.append(("author", "; ".join(m["authors"])))
    fm += [("date", m["date"]), ("source", m["source"]), ("type", m["type"] or "manuscript"),
           ("lang", m["lang"]), ("mode", d.mode), ("layer", d.profile.witness_layer),
           ("verified", f"checked; corpus-curator {TODAY:%Y-%m}, diffed against TEI text")]
    if d.hands:
        fm.append(("hands", "; ".join(f"{k} {v}" for k, v in sorted(d.hands.items(), key=lambda x: int(x[0][1:])))))
    fm.append(("resp", f"corpus-curator {TODAY:%Y-%m}; converted from {d.profile.resp_source()} "
                       f"by tei_convert.py, diffed against TEI text"))
    out = ["---"] + [f"{k}: {yaml_value(v)}" for k, v in fm] + ["---"]
    d.fm_lines = len(out)
    out += d.body
    if d.source_notes:
        out += ["", "@notes"] + d.source_notes
    return nfc("\n".join(out)) + "\n"


def editorial_text(d, witness_key):
    m = d.meta
    fm = [("title", m["title"] if d.editorial_only else f"{m['title']}: Source Note and Annotation"),
          ("date", d.editorial_year), ("source", d.profile.editorial_source(m)),
          ("type", "chapter"), ("lang", "en"), ("mode", "prose"), ("layer", "editorial"),
          ("verified", f"checked; corpus-curator {TODAY:%Y-%m}, validated"),
          ("resp", f"corpus-curator {TODAY:%Y-%m}; converted from {d.profile.resp_source()} apparatus "
                   f"by tei_convert.py, validated")]
    out = ["---"] + [f"{k}: {yaml_value(v)}" for k, v in fm] + ["---"]
    defs = []

    def note_ref(n):
        if d.profile.note_kind(n) in ("companion", "unknown", "source"):
            defs.append(f"[^{len(defs) + 1}]: " + prose(n, lambda x: ""))
            return f"[^{len(defs)}]"
        return ""

    for heading, elements in d.apparatus:
        paras = [prose(p, note_ref) for p in elements]
        paras = [p for p in paras if p]
        if not paras:
            continue
        if heading:
            out += ["", f"# {heading}"]
        for p in paras:
            out += ["", p]
    links = []
    if d.companion_notes:
        out += ["", "# Footnotes"]
        for note, anchor in d.companion_notes:
            text = prose(note, lambda x: "")
            if not text:
                continue
            line = d.fm_lines + d.mapping.get(anchor, len(d.body) - 1) + 1
            links.append(f"[^e{len(links) + 1}]: Annotates [[{witness_key}]]:{line}.")
            out += ["", f"{text}[^e{len(links)}]"]
    if defs or links:
        out += ["", "@notes"] + defs + links
    lines = []
    for line in out:
        if line == "" and lines and lines[-1] == "":
            continue
        lines.append(line)
    return nfc("\n".join(lines)) + "\n"


# ---------------------------------------------------------------- corpus scan and keys

def corpus_index(corpus):
    keys, tei_ids = {}, {}
    if not corpus or not os.path.isdir(corpus):
        return keys, tei_ids
    for coll in sorted(os.listdir(corpus)):
        cdir = os.path.join(corpus, coll)
        if coll.startswith(".") or not os.path.isdir(cdir) or coll == "Assets":
            continue
        for name in os.listdir(cdir):
            if not name.endswith(".md"):
                continue
            p = os.path.join(cdir, name)
            keys[fold(name[:-3])] = p
            try:
                with open(p, encoding="utf-8") as fh:
                    head = "".join(fh.readline() for _ in range(14))
            except (OSError, UnicodeDecodeError):
                continue
            m = re.search(r"^source: .*\bTEI (\S+?)[\"]?$", head, re.M)
            if m:
                tei_ids.setdefault(m.group(1), []).append(p)
    return keys, tei_ids


def assign(base, used):
    if fold(base) not in used:
        return base
    rng = re.search(r"\((\d{4})–\d{4}\)$", base)
    if rng:
        # A year range cannot carry a suffix; the start year can (N5, N10).
        base = base[:rng.start()] + f"({rng.group(1)})"
        if fold(base) not in used:
            return base
    stem, close = base[:-1], ")"
    for sfx in SUFFIXES:
        cand = stem + sfx + close
        if fold(cand) not in used:
            return cand
    return None


# ---------------------------------------------------------------- commands

def find_inputs(src, profile_skip):
    if os.path.isfile(src):
        return [src], []
    files, skipped = [], []
    for root, dirs, fs in os.walk(src):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for d in list(dirs):
            if d in profile_skip:
                skipped.append({"input": os.path.join(root, d), "status": "skipped",
                                "reason": "edition folder outside the per-document transcriptions"})
                dirs.remove(d)
        for f in sorted(fs):
            if f.startswith("."):
                continue
            p = os.path.join(root, f)
            if f.lower().endswith(".xml"):
                files.append(p)
            else:
                skipped.append({"input": p, "status": "skipped", "reason": "not an XML file"})
    return files, skipped


def detect_profile(path):
    with open(path, encoding="utf-8-sig") as fh:
        head = fh.read(4000)
    return "jsp" if re.search(r"<TEI\b[^>]*\s(?:pm|lds):", head) else "generic"


def pilot_pick(drafts, n):
    pool = [d for d in drafts if d.status == "ready"]
    feats = {}
    for d in pool:
        f = set("el:" + x for x in d.elements) | set("cause:" + c for c, _ in d.causes)
        f |= {"mode:" + d.mode, "type:" + str(d.meta["type"]), "editorial:" + str(d.has_editorial),
              "pages:" + ("multi" if sum(1 for x in d.body if x.startswith("@p")) > 1 else "single")}
        f |= set("dropped:" + k for k in d.dropped)
        feats[d.input] = f
    chosen, covered = [], set()
    while pool and len(chosen) < n:
        best = max(pool, key=lambda d: (len(feats[d.input] - covered), -pool.index(d)))
        if not feats[best.input] - covered and chosen:
            break
        chosen.append(best)
        covered |= feats[best.input]
        pool.remove(best)
    for d in pool:
        if len(chosen) >= n:
            break
        chosen.append(d)
    return {d.input for d in chosen}


def cmd_convert(args):
    src, work = os.path.abspath(args.input), os.path.abspath(args.workdir)
    if not os.path.exists(src):
        print(f"input not found: {src}", file=sys.stderr)
        return 2
    first_xml = src if os.path.isfile(src) else next(iter(find_inputs(src, set())[0]), None)
    if first_xml is None:
        print("no XML files found", file=sys.stderr)
        return 2
    pname = detect_profile(first_xml) if args.profile == "auto" else args.profile
    args.edition_years = dict(x.split("=", 1) for x in args.edition_year)
    profile = (JSP if pname == "jsp" else Generic)(args)
    files, skipped = find_inputs(src, profile.skip_dirs)
    print(f"profile: {profile.name}; {len(files)} XML file(s)")

    drafts = []
    for i, p in enumerate(files, 1):
        drafts.append(convert_one(p, src, profile))
        if i % 500 == 0:
            print(f"  converted {i}/{len(files)}")

    keys, tei_ids = corpus_index(args.corpus)
    used = dict(keys)
    ready = sorted((d for d in drafts if d.status == "ready"), key=lambda d: (d.meta["sortkey"], d.input))
    seen_ids = {}
    for d in ready:
        m = d.meta
        if m["tei_id"] in seen_ids:
            d.status, d.reason = "duplicate input", f"same TEI id as {seen_ids[m['tei_id']]}"
            continue
        seen_ids[m["tei_id"]] = d.input
        if m["tei_id"] in tei_ids:
            d.status, d.reason = "already imported", "; ".join(tei_ids[m["tei_id"]])
            continue
        title, shortened = short_title(m["head"] or m["title"])
        if shortened:
            d.causes.append(("short title shortened to seven words", INFO))
        if not title:
            title = "Untitled"
            d.causes.append(("no usable title words; 'Untitled' used", REVIEW))
        if d.editorial_only:
            when = f" {key_date(m['date']).replace('–', '-')}" if m["date"] else ""
            ekey = assign(f"{title}{when} Editorial ({d.editorial_year})", used)
            if ekey is None:
                d.status, d.reason = "held", "suffixes exhausted for key"
                continue
            used[fold(ekey)] = d.input
            d.editorial_key, d.key = ekey, None
            continue
        ak = author_key(m["authors"])
        base = f"{ak + ' - ' if ak else ''}{title} ({key_date(m['date'])})"
        key = assign(base, used)
        if key is None:
            d.status, d.reason = "held", "suffixes exhausted for key"
            continue
        if key != base:
            if fold(base) in keys:
                d.causes.append((f"key collides with existing corpus file {os.path.basename(keys[fold(base)])}", REVIEW))
                d.collision = keys[fold(base)]
            else:
                d.causes.append(("suffix assigned in edition order", INFO))
        used[fold(key)] = d.input
        d.key = key
        if len(key) > 80:
            d.causes.append(("key longer than 80 characters", REVIEW))
        if d.has_editorial and d.editorial_year:
            ebase = f"{title} {key_date(m['date']).replace('–', '-')} Editorial ({d.editorial_year})"
            ekey = assign(ebase, used)
            if ekey:
                used[fold(ekey)] = d.input
                d.editorial_key = ekey

    selected = pilot_pick(drafts, args.pilot) if args.pilot else None
    if os.path.isdir(os.path.join(work, "drafts")):
        shutil.rmtree(os.path.join(work, "drafts"))
    os.makedirs(os.path.join(work, "drafts"), exist_ok=True)
    manifest, causes = [], {}
    for idx, d in enumerate(drafts, 1):
        entry = {"input": d.input, "status": d.status}
        if d.reason:
            entry["reason"] = d.reason
        if hasattr(d, "meta"):
            entry["tei_id"] = d.meta["tei_id"]
        if d.status == "ready" and (getattr(d, "key", None) or getattr(d, "editorial_key", None)):
            if selected is not None and d.input not in selected:
                entry["status"] = "not in pilot"
            else:
                slot = os.path.join(work, "drafts", f"{idx:05d}_{re.sub(r'[^A-Za-z0-9]+', '_', d.meta['tei_id'])}")
                os.makedirs(slot)
                entry.update(slot=slot)
                if d.key:
                    with open(os.path.join(slot, "witness.md"), "w", encoding="utf-8", newline="\n") as fh:
                        fh.write(witness_text(d, d.key))
                    with open(os.path.join(slot, "baseline.txt"), "w", encoding="utf-8", newline="\n") as fh:
                        fh.write(d.baseline)
                    entry.update(key=d.key, collection=d.collection, mode=d.mode,
                                 type=d.meta["type"], date=d.meta["date"], authors=d.meta["authors"])
                if getattr(d, "editorial_key", None):
                    with open(os.path.join(slot, "editorial.md"), "w", encoding="utf-8", newline="\n") as fh:
                        fh.write(editorial_text(d, d.key))
                    entry.update(editorial_key=d.editorial_key, editorial_collection=d.editorial_collection)
                elif not d.has_editorial:
                    entry["editorial"] = "no apparatus"
                if getattr(d, "collision", None):
                    entry["collision"] = d.collision
        elif d.status == "ready":
            entry["status"] = "held"
        if hasattr(d, "dropped") and d.dropped:
            entry["dropped_notes"] = d.dropped
        uniq = []
        for c, lvl in d.causes:
            if (c, lvl) not in uniq:
                uniq.append((c, lvl))
        entry["causes"] = [c for c, _ in uniq]
        for c, lvl in uniq:
            g = causes.setdefault(c, {"level": lvl, "count": 0, "examples": []})
            g["count"] += 1
            if len(g["examples"]) < 3:
                g["examples"].append(d.input)
        manifest.append(entry)
    manifest.extend(skipped)
    with open(os.path.join(work, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"profile": profile.name, "input": src, "pilot": args.pilot, "entries": manifest},
                  fh, ensure_ascii=False, indent=1)
    ordered = dict(sorted(causes.items(), key=lambda kv: (kv[1]["level"] != REVIEW, -kv[1]["count"])))
    with open(os.path.join(work, "causes.json"), "w", encoding="utf-8") as fh:
        json.dump(ordered, fh, ensure_ascii=False, indent=1)

    tally = {}
    for e in manifest:
        tally[e["status"]] = tally.get(e["status"], 0) + 1
    print("status: " + ", ".join(f"{k} {v}" for k, v in sorted(tally.items())))
    print("causes needing review:")
    for c, g in ordered.items():
        if g["level"] == REVIEW:
            print(f"  {g['count']:6}  {c}")
    return 0


def cmd_write(args):
    work, corpus = os.path.abspath(args.workdir), os.path.abspath(args.corpus)
    with open(os.path.join(work, "manifest.json"), encoding="utf-8") as fh:
        man = json.load(fh)
    os.makedirs(corpus, exist_ok=True)
    conv = os.path.join(corpus, "CONVENTIONS.md")
    created = []
    if not os.path.exists(conv):
        shutil.copyfile(os.path.join(HERE, "..", "templates", "CONVENTIONS.md"), conv)
        created.append("CONVENTIONS.md")
    keys, tei_ids = corpus_index(corpus)
    written, skipped = [], []
    skip_causes, skip_ids, replace = set(args.skip_cause), set(args.skip_file), set(args.replace)
    for e in man["entries"]:
        if not e.get("slot"):
            continue
        tid = e.get("tei_id")
        if tid in skip_ids or skip_causes & set(e.get("causes", [])):
            skipped.append((e["input"], "skipped by decision"))
            continue
        if tid in tei_ids and tid not in replace:
            skipped.append((e["input"], "already imported"))
            continue
        pairs = [("witness.md", e["collection"], e["key"])] if e.get("key") else []
        if e.get("editorial_key"):
            pairs.append(("editorial.md", e["editorial_collection"], e["editorial_key"]))
        targets = [(os.path.join(e["slot"], f), os.path.join(corpus, c, k + ".md")) for f, c, k in pairs]
        clash = [t for _, t in targets if os.path.exists(t) and tid not in replace]
        if clash:
            skipped.append((e["input"], f"target exists: {clash[0]}"))
            continue
        for src, dst in targets:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            written.append(dst)
    with open(os.path.join(work, "written.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(written) + ("\n" if written else ""))
    print(f"wrote {len(written)} file(s); skipped {len(skipped)} input(s)"
          + (f"; created {', '.join(created)}" if created else ""))
    for inp, why in skipped[:50]:
        print(f"  skipped {os.path.basename(inp)}: {why}")
    if len(skipped) > 50:
        print(f"  ... {len(skipped) - 50} more (see manifest)")
    return 0


def cmd_audit(args):
    work, corpus = os.path.abspath(args.workdir), os.path.abspath(args.corpus)
    listing = os.path.join(work, "written.txt")
    written = [x for x in open(listing, encoding="utf-8").read().split("\n") if x]
    sys.path.insert(0, HERE)
    sys.dont_write_bytecode = True   # keep the skill folder free of __pycache__
    import fidelity_check
    val = subprocess.run([sys.executable, os.path.join(HERE, "validate_corpus.py"), corpus,
                          "--files-from", listing], capture_output=True, text=True)
    lines = val.stdout.strip().split("\n")
    problems = [x for x in lines if x.startswith("ERROR")]
    warns = [x for x in lines if x.startswith("WARN")]
    with open(os.path.join(work, "manifest.json"), encoding="utf-8") as fh:
        man = json.load(fh)
    by_target = {}
    for e in man["entries"]:
        if e.get("slot") and e.get("key"):
            by_target[os.path.join(corpus, e["collection"], e["key"] + ".md")] = e["slot"]
    fid_fail = 0
    for target in written:
        slot = by_target.get(target)
        if not slot:
            continue
        with open(target, encoding="utf-8") as fh:
            src_text = fh.read()
        with open(os.path.join(slot, "baseline.txt"), encoding="utf-8") as fh:
            base = fh.read()
        failures, report = fidelity_check.compare(src_text, base, strict=True)
        if failures:
            fid_fail += 1
            print(f"FIDELITY {os.path.relpath(target, corpus)}: {failures} unexplained difference(s)")
            for r in report[:8]:
                print(f"    {r}")
    for p in problems:
        print(p)
    print(f"\nvalidator: {len(problems)} error(s), {len(warns)} warning(s) across {len(written)} file(s)")
    print(f"fidelity: {fid_fail} witness file(s) with unexplained differences")
    return 1 if problems or fid_fail else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("convert")
    c.add_argument("input")
    c.add_argument("workdir")
    c.add_argument("--corpus")
    c.add_argument("--pilot", type=int, default=0)
    c.add_argument("--profile", choices=["auto", "generic", "jsp"], default="auto")
    c.add_argument("--collection")
    c.add_argument("--formfill", choices=["rendition", "addition"], default="rendition")
    c.add_argument("--default-author")
    c.add_argument("--edition-year", action="append", default=[])
    c.add_argument("--editorial-date")
    w = sub.add_parser("write")
    w.add_argument("workdir")
    w.add_argument("corpus")
    w.add_argument("--skip-cause", action="append", default=[])
    w.add_argument("--skip-file", action="append", default=[])
    w.add_argument("--replace", action="append", default=[])
    a = sub.add_parser("audit")
    a.add_argument("workdir")
    a.add_argument("corpus")
    args = ap.parse_args()
    return {"convert": cmd_convert, "write": cmd_write, "audit": cmd_audit}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
