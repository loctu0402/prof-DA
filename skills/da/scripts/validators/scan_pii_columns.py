#!/usr/bin/env python3
"""
scan_pii_columns.py - propose a data-classification tier + PII entity per column.

A stdlib port of Microsoft Presidio's recognizer model (no spaCy): a column-NAME deny-list
recognizer (EN + VN) plus an optional sample-VALUE pattern/checksum recognizer. It only
PROPOSES; the DA confirms the tier into the model `.yml` `meta` (same no-guessing discipline
as every other tier - an ambiguous column is proposed [DA-INPUT], never silently PUBLIC).

Taxonomy + entities + propagation: references/data-classification.md.

Output: a worksheet CSV (one row per column, status=open) the DA reviews, plus a summary.

Usage:
  python scan_pii_columns.py                          # scan ./models, write the worksheet
  python scan_pii_columns.py --models <dir>           # scan another models tree
  python scan_pii_columns.py --samples sample.csv     # add value evidence (header=column, rows=values)
  python scan_pii_columns.py --out <path.csv>         # worksheet destination

Exit 0 always (this is a proposer, not a gate). gate_pii_classification.py is the gate.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Presidio "deny-list" recognizer on the column NAME (EN + VN). Order matters: first hit wins.
NAME_RECOGNIZERS = [
    ("national_id", r"(cccd|cmnd|national[_-]?id|citizen[_-]?id|passport|id[_-]?no\b)"),
    ("card_pan",    r"(card[_-]?(no|num|pan)|\bpan\b|the[_-]?atm|card_number)"),
    ("bank_account", r"(bank[_-]?account|account[_-]?(no|num)|\bstk\b|so[_-]?tk|iban)"),
    ("phone",       r"(phone|mobile|\bmsisdn\b|\bsdt\b|so[_-]?dien[_-]?thoai|tel[_-]?no)"),
    ("email",       r"(\bemail\b|e[_-]?mail|mail[_-]?address)"),
    ("full_name",   r"(full[_-]?name|\bho[_-]?ten\b|customer[_-]?name|user[_-]?name\b|fullname)"),
    ("address",     r"(\baddress\b|dia[_-]?chi|street|ward|district)"),
    ("device_id",   r"(\bimei\b|\budid\b|device[_-]?id|mac[_-]?address)"),
    ("geo_precise", r"(latitude|longitude|\blat\b|\blng\b|\blon\b|geo[_-]?point)"),
    ("dob",         r"(date[_-]?of[_-]?birth|\bdob\b|ngay[_-]?sinh|birth[_-]?date)"),
]
NAME_RX = [(ent, re.compile(rx, re.I)) for ent, rx in NAME_RECOGNIZERS]

# Non-PII name signals (weaker; only used to propose a non-PII tier, else [DA-INPUT]).
MONEY_RX = re.compile(r"(amount|amt|revenue|balance|gmv|aum|cashin|cashout|netcash|fee|income|salary|value_vnd|price)", re.I)
PUBLIC_RX = re.compile(r"(_date$|^date|grass_date|^month|^year|_count$|count_|_flag$|is_|category|type$|^segment|status)", re.I)
ID_RX = re.compile(r"(user_id|customer_id|_id$|^id$|merchant_id|partner_id)", re.I)

# Presidio "pattern/checksum" recognizers on a sample VALUE.
VAL_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
VAL_PHONE_VN = re.compile(r"^(?:\+?84|0)(?:3|5|7|8|9)\d{8}$")


def luhn_ok(s):
    digits = [int(c) for c in re.sub(r"\D", "", s)]
    if len(digits) < 13:
        return False
    chk = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        chk += d
    return chk % 10 == 0


def value_entity(values):
    """Strongest entity inferable from sample values, or None."""
    vals = [v.strip() for v in values if v and v.strip()]
    if not vals:
        return None
    if sum(bool(VAL_EMAIL.match(v)) for v in vals) >= max(1, len(vals) // 2):
        return "email"
    if sum(bool(VAL_PHONE_VN.match(v)) for v in vals) >= max(1, len(vals) // 2):
        return "phone"
    if sum(bool(luhn_ok(v)) for v in vals) >= max(1, len(vals) // 2):
        return "card_pan"
    return None


def name_entity(col):
    for ent, rx in NAME_RX:
        if rx.search(col):
            return ent
    return None


def classify(col, name_ent, val_ent):
    """Return (tier, entity, confidence) following the no-guess rule."""
    if val_ent:                                   # value evidence is strongest
        return "RESTRICTED-PII", val_ent, "high (value)"
    if name_ent:
        return "RESTRICTED-PII", name_ent, "medium (name)"
    if MONEY_RX.search(col):
        return "CONFIDENTIAL", "none", "medium (name)"
    if ID_RX.search(col):
        return "INTERNAL", "none", "medium (name)"
    if PUBLIC_RX.search(col):
        return "PUBLIC", "none", "medium (name)"
    return "[DA-INPUT]", "none", "low (ambiguous)"


def parse_columns(models_dir):
    """Yield (model, column, existing_classification) from every model yml (stdlib walk)."""
    for p in Path(models_dir).rglob("*.yml"):
        if p.parent.name == "sources" or p.name.startswith("_"):
            continue
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        model = None
        for i, raw in enumerate(lines):
            mm = re.match(r"^  - name: (\S+)", raw)
            if mm:
                model = mm.group(1)
                continue
            cm = re.match(r"^      - name: (\S+)", raw)
            if cm and model:
                existing = ""
                for nl in lines[i + 1:i + 8]:
                    if re.match(r"^      - name:", nl) or re.match(r"^  - name:", nl):
                        break
                    em = re.search(r"classification:\s*['\"]?([A-Za-z\-\[\]]+)", nl)
                    if em:
                        existing = em.group(1)
                        break
                yield model, cm.group(1), existing


def load_samples(path):
    out = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        for col in (r.fieldnames or []):
            out[col] = []
        for row in r:
            for col, v in row.items():
                out.setdefault(col, []).append(v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=str(ROOT / "models"))
    ap.add_argument("--samples", default=None, help="CSV: header=column names, rows=sample values")
    ap.add_argument("--out", default=str(ROOT / "scripts" / "output" / "pii_classification_worksheet.csv"))
    args = ap.parse_args()

    samples = load_samples(args.samples) if args.samples else {}
    rows, counts = [], {"PUBLIC": 0, "INTERNAL": 0, "CONFIDENTIAL": 0, "RESTRICTED-PII": 0, "[DA-INPUT]": 0}
    skipped = 0
    for model, col, existing in parse_columns(args.models):
        if existing and existing != "[DA-INPUT]":
            skipped += 1
            continue                              # already DA-classified; leave it
        nent = name_entity(col)
        vent = value_entity(samples.get(col, []))
        tier, entity, conf = classify(col, nent, vent)
        counts[tier] = counts.get(tier, 0) + 1
        rows.append({"model": model, "column": col, "proposed_tier": tier,
                     "proposed_entity": entity, "confidence": conf, "status": "open"})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["model", "column", "proposed_tier",
                                           "proposed_entity", "confidence", "status"])
        w.writeheader()
        w.writerows(rows)

    print(f"scan_pii_columns: {len(rows)} columns proposed ({skipped} already classified, skipped)")
    for tier in ("RESTRICTED-PII", "CONFIDENTIAL", "INTERNAL", "PUBLIC", "[DA-INPUT]"):
        print(f"  {tier:16} {counts.get(tier, 0)}")
    pii = [r for r in rows if r["proposed_tier"] == "RESTRICTED-PII"]
    if pii:
        print(f"  -- {len(pii)} RESTRICTED-PII proposed; DA must confirm + decide masking before certify")
    print(f"  worksheet -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
