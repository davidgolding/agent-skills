#!/usr/bin/env python3
"""Add the `layer` and `verified` frontmatter keys (F-table) to sources that
lack them, one rule per collection. A dry run by default: it prints what each
collection would get and a sample of the changes, and writes nothing.

Usage:
    python3 backfill_fields.py CORPUS_ROOT \
        --set "JSP Documents=edition|checked; corpus-curator 2026-11, diffed against TEI text" \
        --set "Evening and Morning Star=transcription|unchecked" [--write]

Each --set is `Collection=layer|verified`. Keys already present are left
alone, and collections without a rule are reported, not changed. The keys go
after `mode` (or after the last key that precedes them in the F-table order).
Standard library only.
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

ORDER = ["title", "author", "date", "source", "type", "lang", "mode", "layer", "verified", "images",
         "hands", "resp"]
LAYERS = {"edition", "transcription", "typescript", "ocr", "hwr", "model", "publication", "editorial"}
VERIFIED = {"unknown", "unchecked", "checked", "collated"}


def parse_rules(specs: list[str]) -> dict[str, dict[str, str]]:
    rules = {}
    for spec in specs:
        coll, _, rest = spec.partition("=")
        layer, _, verified = rest.partition("|")
        layer, verified = layer.strip(), verified.strip()
        if layer not in LAYERS:
            sys.exit(f"--set {spec!r}: layer must be one of {', '.join(sorted(LAYERS))}")
        if verified.split(";")[0].strip() not in VERIFIED:
            sys.exit(f"--set {spec!r}: verified must start with one of {', '.join(sorted(VERIFIED))}")
        rules[coll.strip()] = {"layer": layer, "verified": verified}
    return rules


def backfill(text: str, values: dict[str, str]) -> str | None:
    """`text` with the missing keys inserted in F-table order, or None if unchanged."""
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    present = [ln.split(":", 1)[0] for ln in lines[1:end]]
    changed = False
    for key, value in values.items():
        if key in present:
            continue
        rank = ORDER.index(key)
        at = 1
        for i, k in enumerate(present, start=1):
            if k in ORDER and ORDER.index(k) < rank:
                at = i + 1
        lines.insert(at, f"{key}: {value}")
        present.insert(at - 1, key)
        end += 1
        changed = True
    return "\n".join(lines) if changed else None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("root", type=Path)
    ap.add_argument("--set", action="append", default=[], dest="rules", metavar="COLLECTION=LAYER|VERIFIED")
    ap.add_argument("--write", action="store_true", help="write the changes (default: dry run)")
    ap.add_argument("--sample", type=int, default=3, help="changed headers to show per collection")
    args = ap.parse_args()
    rules = parse_rules(args.rules)

    stats: Counter[tuple[str, str]] = Counter()
    shown: Counter[str] = Counter()
    for coll_dir in sorted(p for p in args.root.iterdir() if p.is_dir() and p.name != "Assets"
                           and not p.name.startswith(".")):
        coll = coll_dir.name
        for f in sorted(coll_dir.glob("*.md")):
            if coll not in rules:
                stats[(coll, "no rule")] += 1
                continue
            text = f.read_text(encoding="utf-8")
            new = backfill(text, rules[coll])
            if new is None:
                stats[(coll, "unchanged")] += 1
                continue
            stats[(coll, "changed")] += 1
            if shown[coll] < args.sample:
                shown[coll] += 1
                head = new.split("\n")[:new.split("\n").index("---", 1) + 1]
                print(f"--- {coll}/{f.name}\n" + "\n".join(head) + "\n")
            if args.write:
                f.write_text(new, encoding="utf-8")

    print(f"{'collection':<40} {'rule':<45} changed  unchanged  no rule")
    for coll in sorted({c for c, _ in stats}):
        r = rules.get(coll)
        rule = f"{r['layer']} | {r['verified']}" if r else "-"
        print(f"{coll:<40} {rule[:45]:<45} {stats[(coll, 'changed')]:>7}  {stats[(coll, 'unchanged')]:>9}  "
              f"{stats[(coll, 'no rule')]:>7}")
    print("written" if args.write else "dry run: nothing written (add --write)")


if __name__ == "__main__":
    main()
