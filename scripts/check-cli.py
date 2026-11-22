#!/usr/bin/env python3
"""Fail when the skill names a command or flag the installed CLI does not have.

The CLI's `soulpass schema` is the source of truth for commands and flags; this
skill only points at them. Every `soulpass <command> --flag` (and every
backticked `<command> --flag` in a table) in SKILL.md and references/ must
resolve to a command in the schema, and each flag to that command or one of
its subcommands.

    python3 scripts/check-cli.py                 # runs `soulpass schema`
    python3 scripts/check-cli.py schema.json     # or reads a saved schema
"""
import json, pathlib, re, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent
schema = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else json.loads(
    subprocess.run(["soulpass", "schema"], check=True, capture_output=True, text=True).stdout)

tree = {}
def walk(commands, prefix):
    for c in commands:
        path = f"{prefix} {c['name']}".strip()
        flags = set()
        for a in c.get("arguments", []):
            flags.add(a["name"]); flags.update(a.get("aliases") or [])
            if a.get("inverse"): flags.add(a["inverse"])
        tree[path] = flags
        walk(c.get("commands") or [], path)
walk(schema["commands"], "")
top = {p.split()[0] for p in tree}

def flags_under(path):
    return set().union(*(f for p, f in tree.items() if p == path or p.startswith(path + " ")))

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
                if flag not in flags_under(path):
                    problems.append(f"{file.name}:{n}: `{path}` has no {flag}")

print("\n".join(problems) or f"PASS: skill matches soulpass {schema.get('toolVersion')}")
sys.exit(1 if problems else 0)
