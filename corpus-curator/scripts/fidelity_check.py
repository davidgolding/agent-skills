#!/usr/bin/env python3
"""Compare a corpus source file against the text extracted from its original.

Usage:
    python3 fidelity_check.py SOURCE_MD EXTRACT_TXT [--prose] [--loose]
                              [--allow-deletion TEXT ...]

The corpus file is reduced to its witness view: what the original shows,
without the apparatus. Milestones, frontmatter, editorial and variant notes,
gaps, editor-supplied text and figure descriptions are dropped; sic readings,
unclear readings, and source-hand additions and deletions are kept as text.
Both sides are NFC-normalized and split into words, then aligned.

    --prose            rejoin words hyphenated across extraction line ends
    --loose            compare letters and digits only (for existing transcriptions
                       whose bracket conventions were translated into the spec's marks)
    --allow-deletion   extraction text the agent deliberately left out (repeatable);
                       each use is printed so it can be reported

Differences are printed as CHANGED, INSERTED, DELETED or MOVED runs with the
corpus line number and extraction page. Deleted runs made only of page numbers,
or repeated identically (running heads), are listed as EXPECTED.

Exit status: 0 when only expected or allowed differences remain, 1 otherwise.
"""

import argparse
import difflib
import re
import sys
import unicodedata

LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi",
             "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st"}
PAGE_NUMBER = re.compile(r"^(?:\d+|[ivxlcdm]+|[IVXLCDM]+)$")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def witness_line(line):
    """Reduce one corpus body line to the text the witness shows."""
    line = re.sub(r"\[\^[^\]]+\]", "", line)                      # note references
    line = re.sub(r"^#{1,6} ", "", line)                          # printed headings
    line = re.sub(r"(?<!\\)\[(?:\.(?:\d+|\?)|\?\.(?:\d+|\?)|_\d+|=[^\]]*)\]", " ", line)
    line = re.sub(r"(?<!\\)\[!([^\]>]*)>[^\]]*\]", r"\1", line)  # sic>corr -> sic
    line = re.sub(r"(?<!\\)\[[!?-]([^\]]*)\]", r"\1", line)       # sic, unclear, surplus
    line = re.sub(r"(?<!\\)\[\+[^\]]*\]", "", line)               # supplied omission
    line = re.sub(r"(?<!\\)\[[^\]]*\]", "", line)                 # supplied lost text
    line = re.sub(r"(?<!\\)\{@[^}]*\}", "", line)                 # hand shift
    line = re.sub(r"(?<!\\)\{-([^}+@]*)\+([^}@]*)(?:@[^}]*)?\}", r"\1 \2", line)
    line = re.sub(r"(?<!\\)\{[+-]?([^}@]*)(?:@[^}]*)?\}", r"\1", line)
    line = re.sub(r"(?<=[^\W\d_])\((?:[^\W\d_]+|---)\)", "", line)  # expansions
    line = re.sub(r"(?<!\\)\*+", "", line)                        # emphasis, speakers
    line = re.sub(r"(?<!\\) ?\| ?", " ", line)                     # prose line breaks, tables
    line = re.sub(r"\\(.)", r"\1", line)                          # escapes
    return line


def corpus_tokens(text):
    lines = text.split("\n")
    start = 0
    if lines and lines[0] == "---":
        start = next((i for i in range(1, len(lines)) if lines[i] == "---"), 0) + 1
    tokens = []
    for idx in range(start, len(lines)):
        line = nfc(lines[idx])
        if line.startswith("@") or re.match(r"^\[\^[ea]\d+\]: ", line) or re.match(r"^\|?[\s:|-]+\|?$", line) and "-" in line:
            continue
        line = re.sub(r"^\[\^\d+\]: ", "", line)
        for word in witness_line(line).split():
            tokens.append((word, idx + 1))
    return tokens


def extract_tokens(text, prose, corpus_text):
    text = nfc(text)
    for lig, rep in LIGATURES.items():
        text = text.replace(lig, rep)
    tokens, page = [], 1
    for chunk in re.split(r"(\f)", text):
        if chunk == "\f":
            page += 1
            continue
        lines = chunk.split("\n")
        carry = None
        for line in lines:
            words = line.split()
            if carry and words:
                joined = carry + words[0]
                hyphenated = carry + "-" + words[0]
                tokens.append((hyphenated if hyphenated in corpus_text else joined, page))
                words = words[1:]
                carry = None
            elif carry:
                tokens.append((carry + "-", page))
                carry = None
            if prose and words and re.search(r"[^\W\d_]-$", words[-1]):
                carry = words.pop()[:-1]
            tokens.extend((w, page) for w in words)
        if carry:
            tokens.append((carry + "-", page))
    return tokens


def key(word, loose):
    return re.sub(r"[\W_]+", "", word) if loose else word


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("extract")
    ap.add_argument("--prose", action="store_true")
    ap.add_argument("--loose", action="store_true")
    ap.add_argument("--allow-deletion", action="append", default=[])
    args = ap.parse_args()

    with open(args.source, encoding="utf-8") as fh:
        corpus_text = fh.read()
    with open(args.extract, encoding="utf-8") as fh:
        extract_text = fh.read()

    out = corpus_tokens(corpus_text)
    src = extract_tokens(extract_text, args.prose, corpus_text)
    a = [key(w, args.loose) for w, _ in src]
    b = [key(w, args.loose) for w, _ in out]
    if args.loose:
        src = [t for t, k in zip(src, a) if k]
        out = [t for t, k in zip(out, b) if k]
        a, b = [k for k in a if k], [k for k in b if k]

    ops = [op for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op[0] != "equal"]
    deleted = [" ".join(a[i1:i2]) for tag, i1, i2, _, _ in ops if tag == "delete"]
    inserted = [" ".join(b[j1:j2]) for tag, _, _, j1, j2 in ops if tag == "insert"]
    allowed = [nfc(" ".join(t.split())) for t in args.allow_deletion]

    failures, expected = 0, 0
    for tag, i1, i2, j1, j2 in ops:
        old = " ".join(w for w, _ in src[i1:i2])
        new = " ".join(w for w, _ in out[j1:j2])
        page = src[i1][1] if i1 < len(src) else (src[-1][1] if src else 0)
        line = out[j1][1] if j1 < len(out) else (out[-1][1] if out else 0)
        where = f"line {line}, extract page {page}"
        if tag == "delete":
            joined = " ".join(a[i1:i2])
            if joined in inserted:
                label = "MOVED"
            elif all(PAGE_NUMBER.match(w) for w in a[i1:i2]):
                label = "EXPECTED"
            elif deleted.count(joined) > 1:
                label = "EXPECTED"
            elif nfc(old) in allowed:
                label = "ALLOWED"
            else:
                label = "DELETED"
            print(f"{label:8} {where}: {old!r}")
        elif tag == "insert":
            label = "MOVED" if " ".join(b[j1:j2]) in deleted else "INSERTED"
            print(f"{label:8} {where}: {new!r}")
        else:
            label = "CHANGED"
            print(f"{label:8} {where}: {old!r} -> {new!r}")
        if label in ("EXPECTED", "MOVED", "ALLOWED"):
            expected += 1
        else:
            failures += 1

    for text in args.allow_deletion:
        print(f"NOTE     allowed deletion requested: {text!r}")
    print(f"\n{len(src)} extracted words, {len(out)} corpus words; "
          f"{failures} unexplained difference(s), {expected} expected/moved/allowed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
