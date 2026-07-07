#!/usr/bin/env python3
"""Portability lint - flags workspace-specific leaks in prof-DA's portable layer.

The plugin claims "portable-first": the references and the bundled templates must not bake in
ONE workspace's private paths, brand palette, or competitor benchmarks. This heuristic scanner
catches the unambiguous leaks so a "portable" file cannot silently ship a machine-specific
hardcode. It is high-precision by design (few, confident rules) so it stays trusted, not muted.

Usage:
    python portability_lint.py [path ...]      # default: skills/da/references + templates
    python portability_lint.py --list-rules

Exit 0 = clean; exit 2 = at least one unacknowledged leak.

Acknowledge an intentional example inline with a trailing  `portability-lint: allow`  marker,
or keep the content in a designated org-specific file (org-extensions / momo-extensions /
mcp example config), which are skipped wholesale. The point is: a leak is either removed,
genericised, or explicitly acknowledged - never silent.
"""
import re
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[4]
ALLOW_MARKER = "portability-lint: allow"
SKIP_FILES = {"org-extensions.md", "momo-extensions.md", "example-org-mcp.json"}
SCAN_EXT = {".md", ".html", ".json", ".js", ".txt"}

# (rule-name, compiled-pattern, why-it-is-a-leak)
RULES = [
    ("momo-palette",
     re.compile(r"#(?:d82d8b|fce4ec|fdf6ee|00b4a0)\b", re.I),
     "brand hex literal - a portable file must use a var(--token), not one org's colour"),
    ("competitor-rate",
     re.compile(r"\b(?:Techcombank|Techcom|LPBank|MSB|Cake|VPBank|Vietcombank)\b[^\n]{0,15}\d+(?:\.\d+)?\s?%"),
     "hardcoded competitor benchmark - belongs in a live cache or the org-extensions layer"),
    ("preview-host",
     re.compile(r"a01preview\.web\.app"),
     "one workspace's portal host - parameterise the host, do not hardcode"),
    ("absolute-user-path",
     re.compile(r"(?:[A-Za-z]:[\\/]Users[\\/]|/c/Users/)(?!<)"),
     "absolute machine path - use ${CLAUDE_PLUGIN_ROOT} / <your-workspace> / ~"),
    ("private-workspace-root",
     re.compile(r"(?<![\w<-])personal-workspace/"),
     "one user's private workspace root - genericise to <your-workspace>/"),
]


def scan_file(path: Path):
    hits = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return hits
    for lineno, line in enumerate(text.splitlines(), 1):
        if ALLOW_MARKER in line:
            continue
        for name, rx, why in RULES:
            m = rx.search(line)
            if m:
                hits.append((lineno, name, m.group(0).strip(), why))
    return hits


def iter_targets(paths):
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in SCAN_EXT and f.name not in SKIP_FILES:
                    yield f
        elif p.is_file() and p.name not in SKIP_FILES:
            yield p


def main(argv):
    if "--list-rules" in argv:
        for name, _, why in RULES:
            print(f"{name}: {why}")
        return 0
    args = [a for a in argv if not a.startswith("--")]
    targets = args or [PLUGIN_ROOT / "skills" / "da" / "references", PLUGIN_ROOT / "templates"]
    total = 0
    for f in iter_targets(targets):
        for lineno, name, snippet, why in scan_file(f):
            rel = f.relative_to(PLUGIN_ROOT) if PLUGIN_ROOT in f.parents else f
            print(f"{rel}:{lineno}: [{name}] {snippet!r} - {why}")
            total += 1
    if total:
        print(
            f"\nportability_lint: {total} unacknowledged leak(s). "
            f"Remove, genericise, or mark the line with `{ALLOW_MARKER}`.",
            file=sys.stderr,
        )
        return 2
    print("portability_lint: clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
