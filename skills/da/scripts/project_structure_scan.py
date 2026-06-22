#!/usr/bin/env python3
"""
project_structure_scan.py - the CURATOR's project-folder structure pass (read-only, never moves).

The other curator scan (curator_scan.py) curates the MEMORY/notes layer. This one curates the
projects/ layer: it answers "which flat projects share a pattern and could be grouped, and which
MUST stay flat because a move would break them". It is the data behind a safe regroup proposal -
it SUGGESTS, the agent proposes, the user approves (golden rule: plan -> approve -> execute).

Per project it computes:
  - family       : the name-token cluster it belongs to (e.g. api-* / etl-*); clusters of >=2 are
                   real families worth grouping (semantically; physical move is gated by safety).
  - ext_refs     : how many files OUTSIDE the project reference `projects/<name>/` (slash or back-
                   slash), excluding the index + PKM + _archive. A move breaks every one of these.
  - live         : a scheduled/live pipeline (a .bat, or schtasks/Task Scheduler wiring) - NEVER move.
  - abs_path     : absolute `...\\projects\\<name>` references (hardest to fix on a move).
  - verdict      : KEEP-FLAT (live or many refs) / LOW-RISK (1-3 refs, fix them in the same commit)
                   / SAFE-TO-NEST (0 ext refs, not live).

Why mostly KEEP-FLAT: in a workspace with cross-project imports + scheduled jobs, deep physical
nesting trades navigability for fragility. The standard is flat + self-contained projects, GROUPED
in the index (the purpose-map), not in the filesystem. This scan also flags purpose-map DRIFT:
projects on disk that no index purpose-map line mentions.

Usage:
  python project_structure_scan.py <workspace_root>
  python project_structure_scan.py <workspace_root> --json

Exit 0 always (it reports; it never moves).
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

TEXT_EXT = {".py", ".md", ".bat", ".json", ".sh", ".yml", ".yaml", ".toml", ".txt", ".cfg", ".ini", ".ipynb"}
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "_archive", ".pytest_cache"}
NOISE_PREFIXES = (".index/", "notes/loctu-pkm/")   # index + PKM reference a project by design
REF_RE = re.compile(r"projects[/\\]([A-Za-z0-9_][A-Za-z0-9_-]*)")
LIVE_RE = re.compile(r"\b(schtasks|Task Scheduler|setup_scheduler|Register-ScheduledTask)\b", re.I)
MAX_BYTES = 1_500_000


def list_projects(root):
    pdir = root / "projects"
    if not pdir.is_dir():
        return []
    return sorted(p.name for p in pdir.iterdir() if p.is_dir() and p.name != "_archive")


def scan_refs(root, projects):
    """One walk over the workspace: tally external referencing FILES per project."""
    pset = set(projects)
    ext = defaultdict(set)      # project -> set of external referencing files
    abs_ref = defaultdict(set)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if Path(fn).suffix.lower() not in TEXT_EXT:
                continue
            fp = Path(dirpath) / fn
            rel = fp.relative_to(root).as_posix()
            try:
                if fp.stat().st_size > MAX_BYTES:
                    continue
                text = fp.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in REF_RE.finditer(text):
                proj = m.group(1)
                if proj not in pset:
                    continue
                if rel.startswith(f"projects/{proj}/"):
                    continue   # self-reference, not a blocker
                if any(rel.startswith(n) for n in NOISE_PREFIXES):
                    continue
                ext[proj].add(rel)
                # absolute-path form is the costliest to fix
                if re.search(rf"[A-Za-z]:[\\/].*projects[\\/]{re.escape(proj)}\b", text):
                    abs_ref[proj].add(rel)
    return ext, abs_ref


def is_live(root, proj):
    pdir = root / "projects" / proj
    if list(pdir.rglob("*.bat")):
        return True
    for fp in pdir.rglob("*"):
        if fp.is_file() and fp.suffix.lower() in {".py", ".md", ".ps1", ".sh", ".bat"}:
            try:
                if fp.stat().st_size <= MAX_BYTES and LIVE_RE.search(fp.read_text(encoding="utf-8", errors="replace")):
                    return True
            except OSError:
                pass
    return False


def family_of(name):
    """Generic clustering: the leading name token (split on '-'). api-* -> 'api', etl-* -> 'etl'."""
    return name.split("-", 1)[0]


def purpose_map_projects(root):
    """Project names already named in the index purpose-map (drift detection). Best-effort."""
    tree = root / ".index" / "_tree.md"
    if not tree.exists():
        return None
    try:
        txt = tree.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    block = re.search(r"Grouped by PURPOSE.*?```", txt, re.S)
    scope = block.group(0) if block else txt
    return set(re.findall(r"`([A-Za-z][A-Za-z0-9_-]+)`", scope))


def verdict(n_ext, live):
    if live:
        return "KEEP-FLAT", "live/scheduled job - a move breaks the pipeline"
    if n_ext == 0:
        return "SAFE-TO-NEST", "no external reference; nests under its family hub cleanly"
    if n_ext <= 3:
        return "LOW-RISK", f"{n_ext} external ref(s) - nest only if they are fixed in the same commit"
    return "KEEP-FLAT", f"{n_ext} external refs - a move breaks many paths; group it in the index instead"


def scan(root):
    root = Path(root)
    projects = list_projects(root)
    ext, abs_ref = scan_refs(root, projects)
    mapped = purpose_map_projects(root)
    fams = defaultdict(list)
    rows = []
    for p in projects:
        n = len(ext.get(p, ()))
        live = is_live(root, p)
        v, why = verdict(n, live)
        fam = family_of(p)
        fams[fam].append(p)
        rows.append({"project": p, "family": fam, "ext_refs": n, "abs_refs": len(abs_ref.get(p, ())),
                     "live": live, "verdict": v, "why": why,
                     "in_purpose_map": (p in mapped) if mapped is not None else None})
    families = {f: ps for f, ps in sorted(fams.items()) if len(ps) >= 2}
    drift = [r["project"] for r in rows if r["in_purpose_map"] is False] if mapped is not None else []
    return {"projects": len(projects), "families": families, "rows": rows, "purpose_map_drift": drift}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = scan(a.root)
    if a.json:
        print(json.dumps(r, indent=2))
        return 0
    print(f"== project-structure curation scan: {r['projects']} projects ==\n")
    print("## Name-pattern families (>=2 members - the clusters worth grouping)")
    if r["families"]:
        for fam, ps in r["families"].items():
            print(f"  {fam}-* : {', '.join(ps)}")
    else:
        print("  (no multi-member name clusters)")
    print("\n## Move-safety (a move breaks every external ref + any live job)")
    print(f"  {'project':26} {'family':10} {'ext':>4} {'abs':>4} {'live':>5}  verdict")
    for row in sorted(r["rows"], key=lambda x: (x["verdict"] != "SAFE-TO-NEST", x["project"])):
        print(f"  {row['project']:26} {row['family']:10} {row['ext_refs']:>4} {row['abs_refs']:>4} "
              f"{('yes' if row['live'] else '-'):>5}  {row['verdict']}")
    safe = [r2["project"] for r2 in r["rows"] if r2["verdict"] == "SAFE-TO-NEST"]
    low = [r2["project"] for r2 in r["rows"] if r2["verdict"] == "LOW-RISK"]
    flat = [r2["project"] for r2 in r["rows"] if r2["verdict"] == "KEEP-FLAT"]
    print(f"\n## Proposed (plan -> approve -> execute; nothing moved)")
    print(f"  SAFE-TO-NEST ({len(safe)}): {', '.join(safe) or '-'}")
    print(f"  LOW-RISK, fix-refs-then-nest ({len(low)}): {', '.join(low) or '-'}")
    print(f"  KEEP-FLAT, group in the index ({len(flat)}): {', '.join(flat) or '-'}")
    if r["purpose_map_drift"]:
        print(f"\n## Purpose-map DRIFT (on disk, not in the index purpose-map): {', '.join(r['purpose_map_drift'])}")
    print("\nPolicy: deep physical nesting trades navigability for fragility in a cross-ref + live-job "
          "workspace. Keep projects flat + self-contained; the index purpose-map is the grouping SoT. "
          "Nest only a SAFE-TO-NEST project under its family hub, with the user's OK + git mv on a branch.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
