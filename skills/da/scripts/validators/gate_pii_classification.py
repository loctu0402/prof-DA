#!/usr/bin/env python3
"""
gate_pii_classification.py - data-classification coverage + PII-policy gate (process pack).

It gates on DEFECTS, never on blanket coverage (forcing 100%
classification would pressure an author to guess a tier; an unknown is [DA-INPUT], not invented).
Taxonomy + entities: references/data-classification.md.

Column classification (meta.classification) states:
  - tier   : PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED-PII  (a real, DA-confirmed tier)
  - dainput: [DA-INPUT]            - honest gap, awaiting DA confirmation
  - none   : no meta.classification at all (unclassified - soft unless --require-classified)
  - bad    : an unrecognised value                              (DEFECT)

Hard ACs (exit 1 if any fail):
  AC1  every meta.classification is a known tier or [DA-INPUT]      (no garbage values)
  AC2  no RAW RESTRICTED-PII column in a canonical mart            (must be masked/hashed there)
  AC3  (only with --require-classified) zero unclassified columns

Soft signals (reported, never block): classification coverage, the RESTRICTED-PII inventory,
the [DA-INPUT] backlog. Exit 0 = pass; exit 1 = a hard AC failed (offenders printed).
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIERS = ("PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED-PII")
DA_INPUT = "[DA-INPUT]"
MASKED_RX = re.compile(r"_(masked|mask|hash|hashed|last4|enc|encrypted|tokenized)$", re.I)


def parse_yml(path):
    """[{name, is_mart, cols:[(col, classification_or_None), ...]}] - stdlib walk."""
    out, cur = [], None
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for i, raw in enumerate(lines):
        mm = re.match(r"^  - name: (\S+)", raw)
        if mm:
            cur = {"name": mm.group(1), "is_mart": mm.group(1).startswith("mart_"), "cols": []}
            out.append(cur)
            continue
        if cur is None:
            continue
        cm = re.match(r"^      - name: (\S+)", raw)
        if cm:
            classification = None
            for nl in lines[i + 1:i + 9]:
                if re.match(r"^      - name:", nl) or re.match(r"^  - name:", nl):
                    break
                em = re.search(r"classification:\s*['\"]?([A-Za-z\-\[\]]+)['\"]?", nl)
                if em:
                    classification = em.group(1)
                    break
            cur["cols"].append((cm.group(1), classification))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=str(ROOT / "models"))
    ap.add_argument("--require-classified", action="store_true",
                    help="treat an unclassified column as a hard DEFECT (post-classification repos)")
    args = ap.parse_args()

    models = []
    for p in Path(args.models).rglob("*.yml"):
        if p.parent.name == "sources" or p.name.startswith("_"):
            continue
        models += [m for m in parse_yml(p) if not m["name"].startswith("_")]

    n_cols = sum(len(m["cols"]) for m in models)
    counts = {t: 0 for t in TIERS}
    dainput = unclassified = 0
    bad, raw_pii_mart, pii_inv = [], [], []
    for m in models:
        for col, cl in m["cols"]:
            if cl is None:
                unclassified += 1
                continue
            if cl == DA_INPUT:
                dainput += 1
                continue
            if cl not in TIERS:
                bad.append((m["name"], col, cl))
                continue
            counts[cl] += 1
            if cl == "RESTRICTED-PII":
                pii_inv.append((m["name"], col))
                if m["is_mart"] and not MASKED_RX.search(col):
                    raw_pii_mart.append((m["name"], col))

    classified = sum(counts.values())
    print(f"gate_pii_classification: {len(models)} models, {n_cols} columns | "
          f"classified {classified}, [DA-INPUT] {dainput}, unclassified {unclassified}")
    print("  tiers: " + ", ".join(f"{t} {counts[t]}" for t in TIERS))

    for mn, c, cl in bad[:30]:
        print(f"  AC1 FAIL [bad-classification '{cl}'] {mn}.{c}")
    for mn, c in raw_pii_mart[:30]:
        print(f"  AC2 FAIL [raw RESTRICTED-PII in mart] {mn}.{c} (mask/hash it or keep upstream only)")
    require_fail = args.require_classified and unclassified > 0
    if require_fail:
        print(f"  AC3 FAIL [unclassified] {unclassified} columns lack meta.classification")

    if pii_inv:
        print(f"  [RESTRICTED-PII inventory] {len(pii_inv)} columns (review masking + access policy)")
    if dainput:
        print(f"  [DA-confirm backlog] {dainput} columns marked [DA-INPUT] (honest gaps, not defects)")

    fail = bool(bad) or bool(raw_pii_mart) or require_fail
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
