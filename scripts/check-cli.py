#!/usr/bin/env python3
"""Fail when the skill names a command or flag the installed CLI does not have.

The CLI's `soulpass schema` is the source of truth for commands and flags; this
skill only points at them. Every `soulpass <command> --flag` (and every
backticked `<command> --flag` in a table) in SKILL.md and references/ must
resolve to a command in the schema, each flag to that command (or an ancestor
or, for a group, a subcommand — the rule soulpass-ai's check-cli-docs.mjs
applies), and each `--chain X` to a name in the schema's `chains` (a read) or
`writeChains` (anything else).

    python3 scripts/check-cli.py                 # runs `soulpass schema`
    python3 scripts/check-cli.py schema.json     # or reads a saved schema
"""
import json, pathlib, re, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent
schema = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else json.loads(
    subprocess.run(["soulpass", "schema"], check=True, capture_output=True, text=True).stdout)

reads = set()  # paths whose effects are read_only: any `chains` name; the rest write
tree = {}  # path -> flags legal on it: its own, its ancestors' and (for a group) its descendants'
def walk(commands, prefix, inherited):
    for c in commands:
        path = f"{prefix} {c['name']}".strip()
        own = set()
        for a in c.get("arguments", []):
            if not a["name"].startswith("-"):
                continue
            own.add(a["name"]); own.update(a.get("aliases") or [])
            if str(a.get("inverse", "")).startswith("-"): own.add(a["inverse"])
        tree[path] = own | inherited
        if c.get("effects", {}).get("kind") == "read_only": reads.add(path)
        walk(c.get("commands") or [], path, own | inherited)
walk(schema["commands"], "", set())
for path in sorted(tree, key=len, reverse=True):  # a group also accepts what its subcommands take
    parent = path.rsplit(" ", 1)[0] if " " in path else None
    if parent: tree[parent] |= tree[path]
top = {p.split()[0] for p in tree}
chains, write_chains = set(schema["chains"]), set(schema["writeChains"])

PROSE = {"has", "is", "to", "in", "provides", "describes"}  # "soulpass <verb> …" in a sentence
problems = []
for file in [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]:
    for n, line in enumerate(file.read_text().splitlines(), 1):
        spans = [m for m in re.findall(r"`([^`]+)`", line) if m.split()[0] in top]
        spans += [m[len("soulpass "):] for m in re.findall(r"soulpass [^`|\n;#]*", line)]
        for span in spans:
            words = [w.split("|")[0] for w in span.split()]
            if not words or not re.fullmatch(r"[a-z][a-z-]*", words[0]) or words[0] in PROSE:
                continue
            path = next((" ".join(words[:k]) for k in (3, 2, 1) if " ".join(words[:k]) in tree), None)
            if path is None:
                problems.append(f"{file.name}:{n}: no command `soulpass {span.strip()[:50]}`")
                continue
            for flag in re.findall(r"(?<![\w-])(--[a-z][a-z0-9-]*)", span):
                if flag not in tree[path]:
                    problems.append(f"{file.name}:{n}: `{path}` has no {flag}")
            for chain in re.findall(r"--chain ([A-Z][A-Z0-9_]*)", span):
                legal = chains if path in reads else write_chains
                if chain not in legal:
                    problems.append(f"{file.name}:{n}: `{path}` cannot use --chain {chain} in this release")

print("\n".join(problems) or f"PASS: skill matches soulpass {schema.get('toolVersion')}")
sys.exit(1 if problems else 0)
