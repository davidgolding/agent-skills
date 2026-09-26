#!/usr/bin/env python3
"""Sound-change engine for conlang-linguist language workspaces.

Compiles every daughter surface form from the etyma in the Lexicon file through
the ordered cascade in the Cascade file, applying the dated irregularity events
in the Events file at the points where they occurred. Loans and later coinages
enter at their recorded stage and undergo only the laws from that stage onward.

A workspace is one flat folder of Markdown files, each named
"<Language> <Section>.md" so names stay unique across a project or Obsidian
vault holding several languages. The language name is read from the folder's
one "<Language> Cascade.md". Inputs are the Cascade file (rules in fenced
```cascade blocks), the Lexicon and Events files (Markdown tables), and the
Corpus file; outputs are "<Language> Compiled Lexicon.md", "... Compiled
Corpus.md", and "... Compiled Changes.md", written beside them.

Commands:
    check   <workspace>                     validate every workspace input
    compile <workspace>                     rebuild the Compiled files and report changes
    trace   <workspace> <entry-id>...       show the step-by-step derivation
    apply   <workspace> <form> [--from N]   run an ad hoc form through the cascade

See references/engine.md for the cascade notation.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

MODIFIERS = set("ːˑʰʷʲˠˤⁿˡʼ˞")
TIES = {"͡", "͜"}
EMPTY = {"∅", "0"}
RESERVED = {"class", "stage", "segments"}
EVENT_TYPES = {
    "analogy", "suppletion", "learned", "semi-learned", "taboo",
    "spelling-pronunciation", "dialect-borrowing", "contamination",
    "back-formation", "other",
}
CASCADE_SUFFIX = " Cascade.md"
FORBIDDEN_NAME_CHARS = set("#^[]|\\/:*?\"<>")
REF_RE = re.compile(r"\{([^{}]+)\}")
ID_RE = re.compile(r"^[A-Za-z][\w.\-]*$")


class EngineError(Exception):
    pass


def attaches(ch, prev):
    return bool(unicodedata.combining(ch)) or ch in MODIFIERS or prev[-1] in TIES


class Tokenizer:
    """Splits IPA strings into segments, longest declared multigraph first.

    Combining diacritics, length marks, and secondary-articulation modifiers
    attach to the preceding segment; a tie bar joins the next character too.
    """

    def __init__(self, multigraphs):
        self.multi = sorted({unicodedata.normalize("NFC", m) for m in multigraphs if len(m) > 1},
                            key=len, reverse=True)

    def one(self, text, i):
        for m in self.multi:
            if text.startswith(m, i):
                seg, i = m, i + len(m)
                break
        else:
            seg, i = text[i], i + 1
        while i < len(text) and attaches(text[i], seg):
            seg += text[i]
            i += 1
        return seg, i

    def __call__(self, text):
        text = unicodedata.normalize("NFC", text.strip().lstrip("*"))
        segs, i = [], 0
        while i < len(text):
            if text[i].isspace():
                raise EngineError(f"whitespace inside form {text!r}; one lexicon entry is one word")
            seg, i = self.one(text, i)
            segs.append(seg)
        return segs


class Rule:
    def __init__(self, rid, stage, target, repl, envs, excs, source):
        self.id, self.stage = rid, stage
        self.target, self.repl = target, repl
        self.envs, self.excs = envs, excs
        self.source = source

    def _holds(self, envs, word, i, j):
        return any(any(True for _ in match_bwd(left, word, i)) and
                   any(True for _ in match_fwd(right, word, j))
                   for left, right in envs)

    def applies_at(self, word, i, j):
        if self.envs and not self._holds(self.envs, word, i, j):
            return False
        return not (self.excs and self._holds(self.excs, word, i, j))

    def realize(self, matched):
        out = []
        for k, e in enumerate(self.repl):
            if e[0] == "seg":
                out.append(e[1])
            else:
                out.append(e[1][self.target[k][1].index(matched[k])])
        return out

    def apply(self, word):
        """Apply once, simultaneously, left to right; contexts read the input form."""
        out, i, n, tlen = [], 0, len(word), len(self.target)
        if tlen == 0:
            for i in range(n + 1):
                if self.applies_at(word, i, i):
                    out.extend(self.realize([]))
                if i < n:
                    out.append(word[i])
            return out
        while i < n:
            j = i + tlen
            if j <= n and all(seg_matches(e, word[i + k]) for k, e in enumerate(self.target)) \
                    and self.applies_at(word, i, j):
                out.extend(self.realize(word[i:j]))
                i = j
            else:
                out.append(word[i])
                i += 1
        return out


def seg_matches(e, seg):
    return seg == e[1] if e[0] == "seg" else seg in e[1]


def match_fwd(elems, word, pos, k=0):
    if k == len(elems):
        yield pos
        return
    e = elems[k]
    if e[0] == "bound":
        if pos == len(word):
            yield from match_fwd(elems, word, pos, k + 1)
    elif e[0] == "opt":
        for p in match_fwd(e[1], word, pos):
            yield from match_fwd(elems, word, p, k + 1)
        yield from match_fwd(elems, word, pos, k + 1)
    elif pos < len(word) and seg_matches(e, word[pos]):
        yield from match_fwd(elems, word, pos + 1, k + 1)


def match_bwd(elems, word, pos, k=None):
    if k is None:
        k = len(elems) - 1
    if k < 0:
        yield pos
        return
    e = elems[k]
    if e[0] == "bound":
        if pos == 0:
            yield from match_bwd(elems, word, pos, k - 1)
    elif e[0] == "opt":
        for p in match_bwd(e[1], word, pos):
            yield from match_bwd(elems, word, p, k - 1)
        yield from match_bwd(elems, word, pos, k - 1)
    elif pos > 0 and seg_matches(e, word[pos - 1]):
        yield from match_bwd(elems, word, pos - 1, k - 1)


class Cascade:
    def __init__(self, path):
        self.path = path
        self.classes, self.stages, self.rules = {}, [], []
        lines = fenced_lines(path, "cascade")
        if not lines:
            raise EngineError(f"{path.name}: no ```cascade code block found")
        multi = []
        for _, raw in lines:
            line = self._strip(raw)
            if line.startswith("segments:"):
                multi += line.split(":", 1)[1].split()
            elif line.startswith("class "):
                multi += line.split(":", 1)[1].split()
        self.tok = Tokenizer(multi)
        stage = None
        seen = set()
        for n, raw in lines:
            line = self._strip(raw)
            if not line or line.startswith("segments:"):
                continue
            where = f"{path.name}:{n}"
            try:
                if line.startswith("class "):
                    name, members = line[6:].split(":", 1)
                    name = name.strip()
                    if not re.fullmatch(r"[A-Z]", name):
                        raise EngineError(f"class name {name!r} must be one ASCII capital letter")
                    self.classes[name] = [self.tok(m)[0] if len(self.tok(m)) == 1 else self._bad(m)
                                          for m in members.split()]
                elif line.startswith("stage "):
                    num, name = line[6:].split(":", 1)
                    num = int(num)
                    if self.stages and num <= self.stages[-1][0]:
                        raise EngineError("stage numbers must increase")
                    self.stages.append((num, name.strip()))
                    stage = num
                else:
                    rid, body = line.split(":", 1)
                    rid = rid.strip()
                    if not ID_RE.match(rid) or rid in RESERVED:
                        raise EngineError(f"invalid rule id {rid!r}")
                    if rid in seen:
                        raise EngineError(f"duplicate rule id {rid!r}")
                    if stage is None:
                        raise EngineError("rule appears before any 'stage N: name' line")
                    seen.add(rid)
                    self.rules.append(self._rule(rid, stage, body.strip()))
            except (ValueError, EngineError) as exc:
                raise EngineError(f"{where}: {exc}") from None
        self.rule_ids = {r.id: r for r in self.rules}
        self.stage_nums = {s for s, _ in self.stages}

    @staticmethod
    def _strip(raw):
        line = raw.split(" ;", 1)[0].strip()
        return "" if line.startswith("#") else line

    @staticmethod
    def _bad(member):
        raise EngineError(f"class member {member!r} is not a single segment; declare it under segments:")

    def _elems(self, text, allow_focus=False):
        elems, i, focus = [], 0, None
        text = unicodedata.normalize("NFC", text)
        while i < len(text):
            ch = text[i]
            if ch.isspace():
                i += 1
            elif ch == "_" and allow_focus:
                if focus is not None:
                    raise EngineError(f"environment {text!r} has more than one '_'")
                focus = len(elems)
                i += 1
            elif ch == "#":
                elems.append(("bound",))
                i += 1
            elif ch == "{":
                end = text.index("}", i)
                members = []
                for m in text[i + 1:end].split():
                    segs = self.tok(m)
                    if len(segs) != 1:
                        self._bad(m)
                    members.append(segs[0])
                elems.append(("set", members))
                i = end + 1
            elif ch == "(":
                end = text.index(")", i)
                elems.append(("opt", self._elems(text[i + 1:end])))
                i = end + 1
            elif ch in EMPTY:
                i += 1
            elif "A" <= ch <= "Z":
                if ch not in self.classes:
                    raise EngineError(f"undefined class {ch!r}")
                elems.append(("set", self.classes[ch]))
                i += 1
            else:
                seg, i = self.tok.one(text, i)
                elems.append(("seg", seg))
        if allow_focus:
            if focus is None:
                raise EngineError(f"environment {text!r} has no '_'")
            return elems[:focus], elems[focus:]
        return elems

    def _envs(self, text):
        return [self._elems(part, allow_focus=True) for part in text.split(",") if part.strip()]

    def _rule(self, rid, stage, body):
        if ">" not in body:
            raise EngineError("rule needs 'target > replacement'")
        target_s, rest = body.split(">", 1)
        repl_s, env_s = (rest.split("/", 1) + [""])[:2]
        env_s, exc_s = (env_s.split("!", 1) + [""])[:2]
        target, repl = self._elems(target_s), self._elems(repl_s)
        for e in target + repl:
            if e[0] not in ("seg", "set"):
                raise EngineError("target and replacement may contain only segments and classes")
        for k, e in enumerate(repl):
            if e[0] == "set" and (k >= len(target) or target[k][0] != "set"
                                  or len(target[k][1]) != len(e[1])):
                raise EngineError(f"replacement class at position {k + 1} needs a target class "
                                  "of the same size at the same position")
        if not target and not repl:
            raise EngineError("rule changes nothing")
        if not target and not env_s.strip():
            raise EngineError("insertion rule needs an environment")
        return Rule(rid, stage, target, repl, self._envs(env_s), self._envs(exc_s), body)

    def derive(self, etymon, entry_stage=0, events=None):
        """Return the list of (step, form) from etymon to surface."""
        events = events or {}
        form = self.tok(etymon)
        history = [("etymon", form)]

        def fire(point):
            nonlocal form
            for ev in events.get(point, []):
                form = self.tok(ev["form"])
                history.append((f"{ev['id']} ({ev['type']})", form))

        by_stage = {}
        for r in self.rules:
            by_stage.setdefault(r.stage, []).append(r)
        for num, _ in self.stages:
            if num < entry_stage:
                continue
            fire(f"stage:{num}")
            for r in by_stage.get(num, []):
                new = r.apply(form)
                if new != form:
                    form = new
                    history.append((r.id, form))
                fire(r.id)
        return history


def fenced_lines(path, tag):
    """Return (line number, text) for every line inside ```tag fenced blocks."""
    out, inside = [], False
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        s = line.strip()
        if s.startswith("```"):
            inside = not inside and s[3:].strip() == tag
            continue
        if inside:
            out.append((n, line))
    return out


SEPARATOR_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]
    return [c[1:-1].strip() if len(c) > 1 and c[0] == c[-1] == "`" else c for c in cells]


def read_tables(path, required, must_exist=True):
    """Read every Markdown table in path whose header has the required columns.

    Headers are matched case-insensitively with spaces read as underscores, so
    'Entry stage' matches entry_stage. Tables inside code fences are ignored.
    """
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    rows, found, fence, i = [], False, False, 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("```"):
            fence = not fence
        elif not fence and s.startswith("|") and i + 1 < len(lines) \
                and SEPARATOR_RE.match(lines[i + 1].strip()):
            header = [h.lower().replace(" ", "_") for h in split_row(s)]
            i += 2
            body = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                body.append((i + 1, split_row(lines[i])))
                i += 1
            if all(c in header for c in required):
                found = True
                for n, cells in body:
                    row = {h: (cells[k] if k < len(cells) else "") for k, h in enumerate(header)}
                    if row[required[0]]:
                        row["_line"] = f"{path.name}:{n}"
                        rows.append(row)
            continue
        i += 1
    if must_exist and not found:
        raise EngineError(f"{path.name}: no table with columns {', '.join(required)}")
    return rows


def md_table(header, rows):
    cell = lambda x: str(x).replace("|", "\\|")
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(cell(x) for x in r) + " |" for r in rows]
    return out


class Workspace:
    def __init__(self, root):
        self.root = Path(root)
        if not self.root.is_dir():
            raise EngineError(f"{self.root}: not a folder")
        cascades = sorted(p for p in self.root.glob(f"*{CASCADE_SUFFIX}")
                          if p.is_file() and not p.name.startswith("."))
        if len(cascades) != 1:
            found = ", ".join(p.name for p in cascades) or "none"
            raise EngineError(f"{self.root}: expected exactly one '<Language>{CASCADE_SUFFIX}' "
                              f"file, found {found}")
        self.language = cascades[0].name[:-len(CASCADE_SUFFIX)]
        bad = sorted(set(self.language) & FORBIDDEN_NAME_CHARS)
        if not self.language.strip() or bad:
            raise EngineError(f"language name {self.language!r} is empty or contains "
                              f"characters Obsidian can't use in file names: {' '.join(bad)}")
        self.cascade = Cascade(cascades[0])
        self.entries = read_tables(self.file("Lexicon"),
                                   ["id", "gloss", "etymon", "stratum", "entry_stage"])
        self.events = read_tables(self.file("Events"),
                                  ["id", "entry", "after", "form", "type", "motivation"])
        corpus = self.file("Corpus")
        self.corpus = corpus.read_text(encoding="utf-8") if corpus.exists() else None

    def file(self, section):
        """Path of a workspace file: '<Language> <Section>.md'."""
        return self.root / f"{self.language} {section}.md"

    def validate(self):
        errors, warnings = [], []
        c = self.cascade
        ids = {}
        for e in self.entries:
            if e["id"] in ids:
                errors.append(f"{e['_line']}: duplicate entry id {e['id']!r}")
            ids[e["id"]] = e
            try:
                e["_stage"] = int(e["entry_stage"])
            except ValueError:
                errors.append(f"{e['_line']}: entry_stage must be an integer")
                e["_stage"] = 0
                continue
            if e["_stage"] != 0 and e["_stage"] not in c.stage_nums:
                errors.append(f"{e['_line']}: entry_stage {e['_stage']} is not a stage in {c.path.name}")
            if e["stratum"] != "inherited" and not e.get("source"):
                errors.append(f"{e['_line']}: {e['stratum']} entry {e['id']!r} needs a source")
            try:
                c.tok(e["etymon"])
            except EngineError as exc:
                errors.append(f"{e['_line']}: {exc}")
        ev_ids = set()
        for ev in self.events:
            where = ev["_line"]
            if ev["id"] in ev_ids:
                errors.append(f"{where}: duplicate event id {ev['id']!r}")
            ev_ids.add(ev["id"])
            if ev["entry"] not in ids:
                errors.append(f"{where}: unknown entry {ev['entry']!r}")
                continue
            if ev["type"] not in EVENT_TYPES:
                errors.append(f"{where}: type {ev['type']!r} not in {sorted(EVENT_TYPES)}")
            if not ev["motivation"]:
                errors.append(f"{where}: event {ev['id']!r} has no motivation; "
                              "an irregularity without a cause is not permitted")
            after = ev["after"]
            if after.startswith("stage:"):
                try:
                    point_stage = int(after[6:])
                except ValueError:
                    point_stage = None
                if point_stage not in c.stage_nums:
                    errors.append(f"{where}: {after!r} is not a stage in {c.path.name}")
                    continue
            elif after in c.rule_ids:
                point_stage = c.rule_ids[after].stage
            else:
                errors.append(f"{where}: 'after' must be a rule id or stage:N, got {after!r}")
                continue
            if point_stage < ids[ev["entry"]].get("_stage", 0):
                errors.append(f"{where}: event precedes the entry's entry_stage")
        phon = self.file("Phonology")
        if phon.exists():
            text = phon.read_text(encoding="utf-8")
            for r in c.rules:
                if not re.search(rf"(?<![\w.\-]){re.escape(r.id)}(?![\w\-]|\.\w)", text):
                    warnings.append(f"rule {r.id} is not documented in {phon.name}")
        else:
            warnings.append(f"{phon.name} is missing; every rule needs a philological statement")
        for n, line in enumerate((self.corpus or "").splitlines(), 1):
            for ref in REF_RE.findall(line):
                if ref not in ids:
                    errors.append(f"{self.file('Corpus').name}:{n}: unknown entry {{{ref}}}")
        for p in sorted(self.root.iterdir()):
            if p.name.startswith("."):
                continue
            if p.is_dir():
                warnings.append(f"subfolder {p.name}/ found; a language folder must stay flat")
            elif p.suffix != ".md":
                warnings.append(f"{p.name} is not Markdown; every workspace file must be .md")
            elif not p.name.startswith(f"{self.language} "):
                warnings.append(f"{p.name} lacks the '{self.language} ' prefix; workspace file "
                                "names must be unique across the project")
        return errors, warnings

    def events_for(self, entry_id):
        grouped = {}
        for ev in self.events:
            if ev["entry"] == entry_id:
                grouped.setdefault(ev["after"], []).append(ev)
        return grouped

    def derive(self, entry):
        return self.cascade.derive(entry["etymon"], entry["_stage"], self.events_for(entry["id"]))


NOTICE = "Compiled by scripts/soundchange.py. Do not edit; change the inputs and recompile."


def compile_ws(ws):
    old = {r["id"]: r["surface"]
           for r in read_tables(ws.file("Compiled Lexicon"), ["id", "surface"], must_exist=False)}
    forms, rows = {}, []
    for e in ws.entries:
        surface = "".join(ws.derive(e)[-1][1])
        forms[e["id"]] = surface
        evs = ", ".join(sorted({ev["id"] for evl in ws.events_for(e["id"]).values() for ev in evl}))
        stratum = e["stratum"] + (f" < {e['source']}" if e.get("source") else "")
        rows.append([e["id"], surface, e["gloss"], e["etymon"], stratum, e["entry_stage"], evs])

    out = ["# Lexicon (compiled)", "", f"> {NOTICE}", ""]
    out += md_table(["ID", "Surface", "Gloss", "Etymon", "Stratum", "Entry stage", "Events"], rows)
    (ws.file("Compiled Lexicon")).write_text("\n".join(out) + "\n", encoding="utf-8")

    ntexts = 0
    if ws.corpus is not None:
        ntexts = len(re.findall(r"^## ", ws.corpus, flags=re.M))
        body = REF_RE.sub(lambda m: forms[m.group(1)], ws.corpus)
        ws.file("Compiled Corpus").write_text(f"> {NOTICE}\n\n{body.rstrip()}\n", encoding="utf-8")

    changes = [(i, old.get(i, "(new)"), forms.get(i, "(removed)"))
               for i in sorted(set(old) | set(forms)) if old.get(i) != forms.get(i)]
    changes_path = ws.file("Compiled Changes")
    if old and changes:
        out = ["# Changed forms (last compile)", "", f"> {NOTICE}", ""]
        out += md_table(["ID", "Old", "New"], changes)
        changes_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    elif changes_path.exists():
        changes_path.unlink()
    return forms, (changes if old else []), ntexts


def format_history(hist):
    return "\n".join(f"  {step:<28} {''.join(form) or '∅'}" for step, form in hist)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "compile"):
        sub.add_parser(name).add_argument("workspace")
    p = sub.add_parser("trace")
    p.add_argument("workspace")
    p.add_argument("ids", nargs="+")
    p = sub.add_parser("apply")
    p.add_argument("workspace")
    p.add_argument("form")
    p.add_argument("--from", dest="from_stage", type=int, default=0,
                   help="stage at which the form enters (default 0)")
    args = ap.parse_args(argv)

    try:
        ws = Workspace(args.workspace)
        errors, warnings = ws.validate()
        for msg in warnings:
            print(f"warning: {msg}", file=sys.stderr)
        if errors:
            for msg in errors:
                print(f"error: {msg}", file=sys.stderr)
            return 1
        if args.cmd == "check":
            print(f"ok: {len(ws.cascade.rules)} rules in {len(ws.cascade.stages)} stages, "
                  f"{len(ws.entries)} entries, {len(ws.events)} events")
        elif args.cmd == "compile":
            forms, changes, ntexts = compile_ws(ws)
            print(f"compiled {len(forms)} entries and {ntexts} corpus texts into the Compiled files")
            if changes:
                print(f"{len(changes)} form(s) changed since the last compile ({ws.file('Compiled Changes').name}):")
                for i, prev, new in changes:
                    print(f"  {i}: {prev} → {new}")
        elif args.cmd == "trace":
            by_id = {e["id"]: e for e in ws.entries}
            for i in args.ids:
                if i not in by_id:
                    raise EngineError(f"unknown entry {i!r}")
                print(f"{i} '{by_id[i]['gloss']}'")
                print(format_history(ws.derive(by_id[i])))
        elif args.cmd == "apply":
            print(format_history(ws.cascade.derive(args.form, args.from_stage)))
    except EngineError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
