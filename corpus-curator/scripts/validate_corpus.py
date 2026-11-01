#!/usr/bin/env python3
"""Validate a Markdown Source Corpus against the mechanical rules of the
Markdown Source Corpus Specification (D, N, F, B, M, E rules).

Usage:
    python3 validate_corpus.py CORPUS_ROOT [--files FILE ...]

With --files, per-file findings are reported only for the named source files,
while corpus-wide checks (key uniqueness, suffix siblings, cross-references)
still read every key in the corpus. Standard library only.

Exit status: 0 when no errors (warnings allowed), 1 when any error, 2 on usage.
"""

import argparse
import datetime
import os
import re
import sys
import unicodedata

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

KEY_RE = re.compile(
    r"^(?:(?P<author>.+?) - )?(?P<title>.+?) \("
    r"(?:(?P<y1>\d{4})–(?P<y2>\d{4})"
    r"|(?P<y>\d{4})(?: (?P<m>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"(?: (?P<d>[1-9]|[12]\d|3[01]))?)?(?P<sfx>[b-z]|[a-z]{2})?)\)$"
)

FM_KEYS = ["title", "author", "date", "source", "type", "lang", "mode", "hands", "resp"]
FM_REQUIRED = {"title", "date", "source", "type", "lang", "mode", "resp"}
TYPES = {"book", "chapter", "article", "newspaper", "letter", "diary", "minutes",
         "record", "legal", "manuscript", "transcript", "inscription"}

EDTF_SINGLE = (r"(?:\d{4}|\d{3}X|\d{2}XX)"
               r"(?:-(?:0[1-9]|1[0-2]|2[1-4])(?:-(?:0[1-9]|[12]\d|3[01]))?)?[~?%]?")
EDTF_RE = re.compile(rf"^(?P<a>{EDTF_SINGLE})(?:/(?P<b>{EDTF_SINGLE}))?$")
BCP47_RE = re.compile(r"^[a-z]{2,3}(?:-[A-Za-z0-9]{1,8})*$")
HTML_RE = re.compile(r"(?<!\\)<(?:/?[A-Za-z][A-Za-z0-9-]*(?:\s[^>]*)?/?|!--)>?")
NOTE_LABEL_RE = re.compile(r"^(?:\d+|e\d+|a\d+)$")
MILESTONE_RE = re.compile(r"^@(?:notes|[A-Za-z][A-Za-z0-9:.\-]*)$")


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, rule, path, line, msg):
        self.items.append((level, rule, path, line, msg))

    def error(self, rule, path, line, msg):
        self.add("ERROR", rule, path, line, msg)

    def warn(self, rule, path, line, msg):
        self.add("WARN", rule, path, line, msg)


def fold(s):
    return unicodedata.normalize("NFC", s).casefold()


def allowed_name_char(ch):
    if ch in "',.&-" or ch in "0123456789":
        return True
    cat = unicodedata.category(ch)
    if cat.startswith("M"):
        return True
    return cat.startswith("L") and unicodedata.name(ch, "").startswith("LATIN")


def check_name_part(part, label, rep, path):
    """N8 character allowlist and spacing for an author or title part."""
    if part != part.strip() or "  " in part:
        rep.error("N8", path, 0, f"{label} has leading, trailing or double spaces: {part!r}")
    for word in part.split(" "):
        if word.startswith("-"):
            rep.error("N8", path, 0, f"{label} word starts with a hyphen: {word!r}")
        for ch in word:
            if ch == "’":
                rep.error("N8", path, 0, f"{label} uses U+2019; the apostrophe is always U+0027")
            elif not allowed_name_char(ch):
                rep.error("N8", path, 0, f"{label} contains disallowed character {ch!r} (U+{ord(ch):04X})")


def suffix_predecessor(sfx):
    """Return the suffix that must already exist before sfx (N6); '' is the bare key."""
    if sfx == "b":
        return ""
    if len(sfx) == 1:
        return chr(ord(sfx) - 1)
    if sfx == "aa":
        return "z"
    first, second = sfx
    if second == "a":
        return chr(ord(first) - 1) + "z"
    return first + chr(ord(second) - 1)


def edtf_parts(single):
    """Split one EDTF date into (year, month or None, day or None) for filename comparison."""
    core = single.rstrip("~?%")
    bits = core.split("-")
    year = int(bits[0].replace("X", "0"))
    month = int(bits[1]) if len(bits) > 1 and int(bits[1]) <= 12 else None
    day = int(bits[2]) if len(bits) > 2 else None
    return year, month, day


def parse_frontmatter(lines, rep, path):
    """Return (dict, index of first body line). Checks F1, F2."""
    fm = {}
    if not lines or lines[0] != "---":
        rep.error("F1", path, 1, "file must open with '---' at its first byte")
        return fm, 0
    end = None
    for i in range(1, len(lines)):
        if lines[i] == "---":
            end = i
            break
    if end is None:
        rep.error("F1", path, 1, "frontmatter has no closing '---'")
        return fm, 0
    order = []
    for i in range(1, end):
        line = lines[i]
        m = re.match(r"^([a-z]+): (.*)$", line)
        if not m:
            rep.error("F1", path, i + 1, f"frontmatter line is not one flat 'key: value': {line!r}")
            continue
        key, value = m.group(1), m.group(2)
        if key in fm:
            rep.error("F1", path, i + 1, f"duplicate key '{key}'")
        if key not in FM_KEYS:
            rep.error("F2", path, i + 1, f"key '{key}' is not one of {', '.join(FM_KEYS)} (F2, F4)")
        if not value.strip():
            rep.error("F2", path, i + 1, f"key '{key}' is empty; leave unused optional keys out")
        if value[:1] in "[{>|&*!%@`" or value.startswith("- "):
            rep.error("F1", path, i + 1, f"value of '{key}' starts with a YAML indicator; quote it")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif ": " in value or " #" in value or value.endswith(":"):
            rep.error("F1", path, i + 1, f"value of '{key}' contains ': ' or ' #'; wrap it in double quotes")
        fm[key] = value
        order.append(key)
    known = [k for k in order if k in FM_KEYS]
    if known != sorted(known, key=FM_KEYS.index):
        rep.error("F2", path, 2, f"keys out of order: {', '.join(known)}")
    for k in sorted(FM_REQUIRED - fm.keys()):
        rep.error("F2", path, 1, f"required key '{k}' is missing")
    if end - 1 > 12:
        rep.warn("F4", path, 1, f"frontmatter is {end - 1} lines; keep it within about 12")
    return fm, end + 1


def check_frontmatter_values(fm, rep, path, types):
    dm = EDTF_RE.match(fm["date"]) if "date" in fm else None
    if "date" in fm and not dm:
        rep.error("F3", path, 1, f"date {fm['date']!r} is not EDTF Level 1")
    for single in (dm.group("a"), dm.group("b")) if dm else ():
        if single and "X" not in single:
            y, mo, d = edtf_parts(single)
            try:
                datetime.date(y, mo or 1, d or 1)
            except ValueError:
                rep.error("F3", path, 1, f"date {fm['date']!r} does not exist on the calendar")
    if "type" in fm and fm["type"] not in types:
        rep.error("F2", path, 1, f"type {fm['type']!r} is not listed in the spec or CONVENTIONS.md")
    if "mode" in fm and fm["mode"] not in ("diplomatic", "prose"):
        rep.error("F2", path, 1, f"mode {fm['mode']!r} must be 'diplomatic' or 'prose'")
    if "lang" in fm:
        for tag in re.split(r"\s*;\s*", fm["lang"]):
            if not BCP47_RE.match(tag):
                rep.error("F2", path, 1, f"lang value {tag!r} is not a BCP 47 tag")


def check_key(key, fm, rep, path, all_keys):
    """N1, N5, N6, N8, N9, N10 for one source key."""
    m = KEY_RE.match(key)
    if not m:
        rep.error("N1", path, 0, f"key does not match '{{Author}} - {{Short Title}} ({{Date}})': {key!r}")
        return
    if key.count(" - ") > 1:
        rep.error("N8", path, 0, "' - ' may occur only once, as the author delimiter")
    author, title = m.group("author"), m.group("title")
    for label, part in (("author", author), ("title", title)):
        if part is None:
            continue
        if any(c in part for c in "()–"):
            rep.error("N8", path, 0, f"{label} contains a parenthesis or en dash")
        check_name_part(part, label, rep, path)
    if len(key) > 80:
        rep.warn("N9", path, 0, f"key is {len(key)} characters; aim for 80 or fewer")
    if len((key + ".md").encode("utf-8")) > 200:
        rep.error("N9", path, 0, "filename exceeds 200 bytes of UTF-8")

    if m.group("y1"):
        if int(m.group("y1")) >= int(m.group("y2")):
            rep.error("N5", path, 0, "date range must run from an earlier to a later year")
    elif m.group("d"):
        try:
            datetime.date(int(m.group("y")), MONTHS.index(m.group("m")) + 1, int(m.group("d")))
        except ValueError:
            rep.error("N10", path, 0, "filename date does not exist on the calendar")

    sfx = m.group("sfx")
    if sfx:
        if sfx == "a" or (len(sfx) == 2 and sfx[0] > "z"):
            rep.error("N6", path, 0, f"invalid suffix {sfx!r}")
        else:
            base = key[: key.rindex(sfx + ")")]
            pred = base + suffix_predecessor(sfx) + ")"
            if fold(pred) not in all_keys:
                rep.error("N10", path, 0, f"suffix '{sfx}' has no '{suffix_predecessor(sfx) or 'unsuffixed'}' sibling")

    # N10: filename date is a truncation of frontmatter date.
    date = fm.get("date", "")
    dm = EDTF_RE.match(date) if date else None
    if dm:
        if m.group("y1"):
            if not dm.group("b"):
                rep.error("N10", path, 0, "filename has a year range but frontmatter date is not an interval")
            else:
                a, b = edtf_parts(dm.group("a"))[0], edtf_parts(dm.group("b"))[0]
                if (a, b) != (int(m.group("y1")), int(m.group("y2"))):
                    rep.error("N10", path, 0, f"filename range does not match frontmatter date {date!r}")
        else:
            y, mo, d = edtf_parts(dm.group("a"))
            if int(m.group("y")) != y:
                rep.error("N10", path, 0, f"filename year does not match frontmatter date {date!r}")
            if m.group("m") and MONTHS.index(m.group("m")) + 1 != mo:
                rep.error("N10", path, 0, f"filename month does not match frontmatter date {date!r}")
            if m.group("d") and int(m.group("d")) != d:
                rep.error("N10", path, 0, f"filename day does not match frontmatter date {date!r}")

    # N10: author surnames agree with frontmatter author.
    if author:
        fm_author = fold(fm.get("author", ""))
        if not fm_author:
            rep.error("N10", path, 0, "key names an author but frontmatter has no 'author'")
        else:
            if author.endswith(", et al."):
                names = [author[: -len(", et al.")]]
            else:
                names = author.split(" and ")
            for name in names:
                if fold(name) not in fm_author:
                    rep.error("N10", path, 0, f"key author {name!r} not found in frontmatter author")


def scan_marks(line, lineno, rep, path, refs, wikilinks, editorial_note):
    """M3, M4, M5 and mark-shape checks for one body line."""
    stack = []
    i, n = 0, len(line)
    while i < n:
        ch = line[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "[" and line.startswith("[^", i):
            j = line.find("]", i)
            label = line[i + 2: j] if j > 0 else ""
            if j < 0 or not NOTE_LABEL_RE.match(label):
                rep.error("B7", path, lineno, f"malformed note reference near column {i + 1}")
                i += 2
                continue
            if not (i == 0 and line[j + 1: j + 2] == ":"):
                refs.add(label)
            i = j + 1
            continue
        if ch == "[" and line.startswith("[[", i):
            j = line.find("]]", i)
            if j < 0:
                rep.error("M4", path, lineno, "unclosed '[[' cross-reference")
                return
            if not editorial_note:
                rep.error("B7", path, lineno, "cross-references [[key]] belong only in editorial notes")
            wikilinks.append(line[i + 2: j])
            i = j + 2
            continue
        if ch == "[":
            if stack and stack[-1][0] == "[":
                rep.error("M3", path, lineno, "editorial mark nested inside an editorial mark")
            stack.append(("[", i))
        elif ch == "{":
            if stack:
                rep.error("M3", path, lineno, "source-hand mark nested inside another mark")
            stack.append(("{", i))
        elif ch in "]}":
            want = "[" if ch == "]" else "{"
            if not stack or stack[-1][0] != want:
                rep.error("M4", path, lineno, f"unmatched '{ch}' at column {i + 1}; escape a literal as '\\{ch}'")
            else:
                _, start = stack.pop()
                check_mark_content(want, line[start + 1: i], lineno, rep, path)
                if ch == "]" and line[i + 1: i + 2] == "(":
                    rep.error("M5", path, lineno, "the sequence '](' must be escaped")
        i += 1
    for kind, start in stack:
        rep.error("M4", path, lineno, f"'{kind}' at column {start + 1} is not closed on its line")


def check_mark_content(kind, body, lineno, rep, path):
    if not body:
        rep.error("M1", path, lineno, f"empty '{kind}' mark")
        return
    if kind == "[":
        op = body[0]
        if op == "." and not re.fullmatch(r"\.(?:\d+|\?)", body):
            rep.error("M1", path, lineno, f"gap mark must be [.N] or [.?]: [{body}]")
        elif op == "_" and not re.fullmatch(r"_\d+", body):
            rep.error("M1", path, lineno, f"space mark must be [_N]: [{body}]")
        elif op == "?" and body.startswith("?.") and not re.fullmatch(r"\?\.(?:\d+|\?)", body):
            rep.error("M1", path, lineno, f"illegible gap must be [?.N]: [{body}]")
        elif op == "=" and not re.fullmatch(r"=[a-z]+: .+", body):
            rep.error("M1", path, lineno, f"description mark must be [=figure: description]: [{body}]")
        elif op == "!" and body.count(">") > 1:
            rep.error("M1", path, lineno, f"sic/corr mark takes one '>': [{body}]")
    else:
        if body[0] not in "+-@" and "@" not in body:
            rep.error("M1", path, lineno, f"source-hand mark needs an operator or '@' value: {{{body}}}")


def check_source(path, key, text, rep, all_keys, types):
    if text.startswith("﻿"):
        rep.error("E1", path, 1, "file starts with a byte-order mark")
        text = text[1:]
    if "\r" in text:
        rep.error("E1", path, 1, "file contains CR line endings; use LF")
    if not text.endswith("\n"):
        rep.error("E1", path, 1, "file lacks a final newline")
    if unicodedata.normalize("NFC", text) != text:
        rep.error("E1", path, 1, "body is not NFC-normalized")
    if unicodedata.normalize("NFC", key) != key:
        rep.error("E1", path, 0, "filename is not NFC-normalized")

    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    fm, body_start = parse_frontmatter(lines, rep, path)
    check_frontmatter_values(fm, rep, path, types)
    check_key(key, fm, rep, path, all_keys)

    refs, defs, wikilinks, hands_used = set(), set(), [], set()
    notes_line = None
    blank_run = 0
    for idx in range(len(lines)):
        lineno = idx + 1
        line = lines[idx]
        if line != line.rstrip():
            rep.error("E1", path, lineno, "trailing whitespace")
        if idx < body_start:
            continue
        if line == "":
            blank_run += 1
            if blank_run == 2:
                rep.error("B3", path, lineno, "more than one consecutive blank line")
            continue
        blank_run = 0
        if line[0] in " \t":
            rep.error("E5", path, lineno, "line begins with whitespace; record meaningful space with [_n]")
        if line.startswith("```") or line.startswith("~~~"):
            rep.warn("E4", path, lineno, "code fence in a source file")
        if HTML_RE.search(line):
            rep.error("E4", path, lineno, "HTML or XML markup is not allowed; escape a literal '<'")
        if line.startswith("@"):
            if line == "@notes":
                if notes_line is not None:
                    rep.error("B7", path, lineno, "'@notes' appears more than once")
                notes_line = lineno
            elif not MILESTONE_RE.match(line):
                rep.error("M5", path, lineno, "line opening with '@' is not a milestone; escape a literal '@'")
            continue
        definition = re.match(r"^\[\^([^\]]+)\]: ", line)
        if definition:
            defs.add(definition.group(1))
            if notes_line is None:
                rep.error("B7", path, lineno, "note definition appears before the '@notes' line")
        elif notes_line is not None:
            rep.error("B7", path, lineno, "only note definitions may follow '@notes'")
        editorial = bool(definition) and definition.group(1).startswith("e")
        scan_marks(line, lineno, rep, path, refs, wikilinks, editorial)
        for brace in re.findall(r"(?<!\\)\{([^{}]*)\}", line):
            if "@" in brace:
                for value in brace.split("@", 1)[1].split():
                    if re.fullmatch(r"h\d+", value):
                        hands_used.add(value)

    for label in sorted(refs - defs):
        rep.error("B7", path, 0, f"note reference [^{label}] has no definition")
    for label in sorted(defs - refs):
        rep.warn("B7", path, 0, f"note [^{label}] is defined but never referenced")
    for link in wikilinks:
        target = link.split("|")[0]
        if fold(target) not in all_keys:
            rep.error("B7", path, 0, f"cross-reference [[{target}]] names no key in the corpus")
    for hand in sorted(hands_used):
        if not re.search(rf"\b{hand}\b", fm.get("hands", "")):
            rep.error("F2", path, 0, f"hand '{hand}' is used in marks but not defined in 'hands'")
    if len(lines) > 2000:
        rep.warn("B9", path, 0, f"file has {len(lines)} lines; split at the work's own volumes or parts if it has them")


def conventions_types(root):
    types = set(TYPES)
    path = os.path.join(root, "CONVENTIONS.md")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            in_types = False
            for line in fh:
                if line.startswith("#"):
                    in_types = "type" in line.lower()
                elif in_types:
                    types.update(re.findall(r"`([a-z]+)`", line))
    return types


def check_collection_name(name, rep, path):
    core = re.sub(r" \([^()]+\)$", "", name)
    if re.search(r"\(\d{4}", name):
        rep.error("D3", path, 0, "collection name carries a date")
    check_name_part(core, "collection name", rep, path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--files", nargs="*", help="limit per-file findings to these source files")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    rep = Report()
    scope = {os.path.abspath(f) for f in args.files} if args.files else None

    if not os.path.isfile(os.path.join(root, "CONVENTIONS.md")):
        rep.error("D4", root, 0, "corpus root has no CONVENTIONS.md")

    sources, collections, assets = [], [], []
    for entry in sorted(os.listdir(root)):
        full = os.path.join(root, entry)
        if entry.startswith("."):
            continue
        if entry == "CONVENTIONS.md":
            continue
        if entry == "Assets" and os.path.isdir(full):
            assets = [a for a in sorted(os.listdir(full)) if not a.startswith(".")]
            continue
        if not os.path.isdir(full):
            rep.error("D1", full, 0, "root may hold only CONVENTIONS.md, Assets and collection folders")
            continue
        collections.append(entry)
        for name in sorted(os.listdir(full)):
            if name.startswith("."):
                continue
            item = os.path.join(full, name)
            if os.path.isdir(item):
                rep.error("D2", item, 0, "collection folders hold no subfolders")
            elif not name.endswith(".md"):
                rep.error("D2", item, 0, "collection folders hold only .md source files; binaries go in Assets")
            else:
                sources.append(item)

    seen = {}
    for name in collections:
        check_collection_name(name, rep, os.path.join(root, name))
        if fold(name) in seen:
            rep.error("D3", os.path.join(root, name), 0, f"collection name collides with {seen[fold(name)]!r}")
        seen[fold(name)] = name

    keys = {}
    for path in sources:
        key = os.path.basename(path)[:-3]
        k = fold(key)
        if k in keys:
            rep.error("D6", path, 0, f"key collides with {keys[k]} (NFC, case-insensitive)")
        else:
            keys[k] = path
    all_keys = set(keys)
    types = conventions_types(root)

    for path in sources:
        if scope is not None and path not in scope:
            continue
        try:
            with open(path, "rb") as fh:
                raw = fh.read()
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            rep.error("E1", path, 0, "file is not valid UTF-8")
            continue
        check_source(path, os.path.basename(path)[:-3], text, rep, all_keys, types)

    key_list = sorted(keys.values(), key=lambda p: -len(os.path.basename(p)))
    for asset in assets:
        stem = os.path.splitext(asset)[0]
        owner = next((p for p in key_list
                      if stem.startswith(os.path.basename(p)[:-3] + " ")
                      and re.fullmatch(r"\S+", stem[len(os.path.basename(p)) - 2:])), None)
        if owner is None:
            rep.error("D5", os.path.join(root, "Assets", asset), 0,
                      "asset name is not '{key} {label}.{ext}' for an existing key")

    errors = [i for i in rep.items if i[0] == "ERROR"]
    for level, rule, path, line, msg in rep.items:
        loc = os.path.relpath(path, root)
        loc = f"{loc}:{line}" if line else loc
        print(f"{level} {rule} {loc}: {msg}")
    checked = len(scope) if scope is not None else len(sources)
    print(f"\n{checked} source file(s) checked; {len(errors)} error(s), {len(rep.items) - len(errors)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
