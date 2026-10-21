# Vendor Payments ↔ Lobbying Disclosures Cross-Reference (Workspace)

## Status (this run)
- No vendor payment dataset (`vendor_payments.*` / `payments.*`) and no lobbying disclosure dataset (`lobbying_disclosures.*` / `lobbying.*`) were found anywhere in the workspace outside OpenPlanter session logs.
- As a result, **no overlaps could be computed** in this workspace snapshot.

## Outputs present
- `overlaps.csv` exists but contains **header only** (1 line; no overlap rows).
- `overlaps.json` exists and reports `payments_source=null`, `lobbying_source=null`, and 0 records.

## How overlaps are defined (implemented in `crossref_payments_lobbying.py`)
A payment is flagged as overlapping a lobbying disclosure when:
- `name_key(vendor/payee)` == `name_key(lobbying registrant/client)` OR `name_key(lobbying firm)`

Normalization (`name_key`) uses:
- uppercase
- punctuation stripped
- `&` → `AND`
- common legal suffix removal (INC/LLC/LTD/CORP/CO/LP/LLP/PLC/PC)
- then alphanumeric-only key.

Confidence tiers:
- `confirmed`: name_key match + extracted ZIP match (5-digit) on both sides
- `probable`: name_key match only

## Next step to produce real overlaps
Add/point to the two input files, then run:
- `python3 crossref_payments_lobbying.py --payments <payments_file> --lobbying <lobbying_file>`

Note: in this environment snapshot, `python3` was not available on PATH (OS-level error). If you enable Python 3, the script will generate `overlaps.csv` and `overlaps.json`.
