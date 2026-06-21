# Reference — Data Classification & PII Tagging (Presidio-concept)

> A schema contract certifies WHAT a column means (grain, definition, gotchas). This adds HOW SENSITIVE
> it is, so the sensitivity travels with the model and any consumer can honour it. Distilled from
> Microsoft Presidio's design (a context-aware, pluggable PII model) but stdlib-only: a column-NAME
> deny-list recognizer plus an optional sample-VALUE pattern/checksum recognizer — no spaCy/heavy deps.
> Use it in `model` mode (schema design) and `process` mode (data-quality audit).
>
> Honest limit (Presidio states the same): automated detection finds MOST sensitive data, never ALL.
> Every uncertain column is a `[DA-INPUT]`, confirmed by the DA — never silently assumed PUBLIC.

## 1. The sensitivity taxonomy (4 tiers)

| Tier | Meaning | Examples | Handling |
|---|---|---|---|
| **PUBLIC** | non-sensitive, shareable outside | event_date, public category, aggregate counts | none |
| **INTERNAL** | business data, internal-only; pseudonymous ids | metric values, segment, a pseudonymous user_id | access by role |
| **CONFIDENTIAL** | sensitive business value | revenue, balance, transaction amount | restricted access + audit |
| **RESTRICTED-PII** | identifies an individual | phone, email, national id, card PAN, bank account, full name, address, precise geo | mask/hash/encrypt + access policy + never raw in a shared mart |

> Pseudonymous note: a hashed/surrogate `user_id` alone usually does not directly identify a person
> (it needs the mapping), so it is **INTERNAL/CONFIDENTIAL**, not RESTRICTED-PII by itself. A raw
> phone/national-id column IS RESTRICTED-PII.

## 2. PII entities (the `meta.pii_entity` vocabulary for RESTRICTED-PII columns)
`phone` · `email` · `national_id` · `card_pan` · `bank_account` · `full_name` · `address` ·
`device_id` (IMEI/UDID) · `geo_precise` (lat/long) · `dob` (date of birth). A non-PII column uses `none`.

## 3. Recognizers (Presidio's recognizer types, stdlib implementation)
`scripts/validators/scan_pii_columns.py` runs two recognizer families and combines their signal:

- **Deny-list on the column NAME** (Presidio deny-list recognizer): regex over the column name in
  English + locale terms (e.g. it ships Vietnamese aliases: `sdt`/`so_dien_thoai` for phone, `cccd`/`cmnd`
  for national id, `stk`/`so_tk` for bank account — extend the lists for your locale).
- **Pattern + checksum on a SAMPLE VALUE** (only with `--samples`): email/phone regex, a **Luhn** check
  for card PAN. Value evidence upgrades a name-only guess to high confidence.

The scanner PROPOSES a tier + entity per column; an ambiguous column is proposed `[DA-INPUT]`. The DA
confirms into the model `.yml` `meta` (it never auto-certifies).

## 4. Where the tags live (schema.yml `meta`)
```yaml
columns:
  - name: user_phone
    description: "Primary phone number of the user."
    meta:
      classification: RESTRICTED-PII      # one of the 4 tiers, or [DA-INPUT]
      pii_entity: phone                   # entity, or 'none'
  - name: txn_amount
    description: "Transaction amount."
    meta:
      classification: CONFIDENTIAL
      pii_entity: none
meta:
  data_sensitivity: RESTRICTED-PII        # model rollup = the highest column tier (or [DA-INPUT])
```

## 5. Operators (downstream handling per tier — Presidio anonymizer operators)
`redact` (drop) · `mask` (keep last 4) · `hash` (irreversible join key) · `encrypt` (reversible).
Policy: a RESTRICTED-PII column must not appear **raw** in the canonical mart (the agent/BI surface) —
mask/hash it there, or keep it only in a restricted upstream. The gate flags a raw one reaching a mart.

## 6. Propagation (sensitivity is sync-aware)
Once the DA certifies the classification in the schema, it should fan out to every reader surface the
schema feeds: a **data catalog** (the classification becomes a column tag — caught in the catalog
diff both ways), a **semantic layer** (a RESTRICTED-PII column in a shared model is hidden from broad
BI), and any **knowledge base / RAG reader** (so a harness can refuse to surface a RESTRICTED-PII
value). Propagation runs only on a DA-certified classification; an open `[DA-INPUT]` does not propagate.

## 7. Run it
```bash
python scripts/validators/scan_pii_columns.py --models <models-dir>            # propose -> worksheet
python scripts/validators/scan_pii_columns.py --models <dir> --samples s.csv   # add value evidence
python scripts/validators/gate_pii_classification.py --models <dir>            # flag raw RESTRICTED-PII in marts
python scripts/validators/gate_pii_classification.py --models <dir> --require-classified   # hard-fail unclassified
```
