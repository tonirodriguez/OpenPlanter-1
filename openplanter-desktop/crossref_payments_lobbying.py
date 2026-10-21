"""Cross-reference vendor payments against lobbying disclosures and flag overlaps.

This script is designed to run in a restricted environment where shell access may be disabled.
It only requires Python 3 and local input files.

Inputs (expected in workspace root unless --paths provided):
  - vendor_payments.(csv|tsv|jsonl)
  - lobbying_disclosures.(csv|tsv|jsonl)

Outputs:
  - overlaps.json
  - overlaps.csv

Matching:
  - exact match on normalized organization name key (name_key)
  - optional confirmed tier if zip match is available in both records

Usage examples:
  python3 crossref_payments_lobbying.py --payments data/payments.csv --lobbying data/lobbying.csv

"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple


SUFFIXES = {
    "INC",
    "INCORPORATED",
    "LLC",
    "L L C",
    "LTD",
    "LIMITED",
    "CORP",
    "CORPORATION",
    "CO",
    "COMPANY",
    "LP",
    "L P",
    "LLP",
    "L L P",
    "PLC",
    "P L C",
    "PC",
    "P C",
}

STOPWORDS = {
    "THE",
    "AND",
    "OF",
}


def _norm_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def normalize_org_name(name: str) -> str:
    """Return a normalized org name (still human-readable)."""
    if name is None:
        return ""
    s = name.strip().upper()
    s = s.replace("&", " AND ")
    s = re.sub(r"[\.,;:/\\()\[\]{}\"'`]+", " ", s)
    s = _norm_spaces(s)

    # remove trailing suffix tokens
    parts = s.split(" ")
    # drop stopwords anywhere
    parts = [p for p in parts if p and p not in STOPWORDS]

    # iteratively strip suffixes from end
    while parts:
        tail = parts[-1]
        if tail in SUFFIXES:
            parts.pop()
            continue
        # handle "L.L.C" etc already removed punctuation; may appear as "L" "L" "C"
        if len(parts) >= 3 and " ".join(parts[-3:]) in SUFFIXES:
            parts = parts[:-3]
            continue
        break

    return " ".join(parts)


def name_key(name: str) -> str:
    """A deterministic key: alnum only."""
    n = normalize_org_name(name)
    return re.sub(r"[^A-Z0-9]", "", n)


def extract_zip(row: Dict[str, Any]) -> Optional[str]:
    # try common field names
    for k in ["zip", "zipcode", "zip_code", "postal", "postal_code", "zip5"]:
        if k in row and row[k] is not None:
            z = str(row[k]).strip()
            if z:
                m = re.search(r"(\d{5})", z)
                if m:
                    return m.group(1)
    # try a generic address field
    for k in ["address", "vendor_address", "payee_address", "registrant_address"]:
        if k in row and row[k] is not None:
            m = re.search(r"(\d{5})", str(row[k]))
            if m:
                return m.group(1)
    return None


def detect_delimiter(path: str) -> str:
    if path.lower().endswith(".tsv"):
        return "\t"
    return ","


def read_rows(path: str) -> List[Dict[str, Any]]:
    if path.lower().endswith(".jsonl"):
        rows: List[Dict[str, Any]] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rows.append(json.loads(line))
        return rows

    delim = detect_delimiter(path)
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=delim)
        return [dict(r) for r in reader]


def pick_first_present(row: Dict[str, Any], keys: List[str]) -> Optional[str]:
    for k in keys:
        if k in row and row[k] is not None:
            v = str(row[k]).strip()
            if v:
                return v
    return None


def get_payment_vendor_name(row: Dict[str, Any]) -> Optional[str]:
    return pick_first_present(
        row,
        [
            "vendor_name",
            "vendor",
            "payee",
            "payee_name",
            "supplier",
            "supplier_name",
            "entity_name",
            "name",
        ],
    )


def get_lobby_entity_names(row: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Return list of (role, name)."""
    out: List[Tuple[str, str]] = []
    for role, keys in [
        (
            "registrant",
            [
                "registrant_name",
                "registrant",
                "client_name",
                "client",
                "principal",
                "principal_name",
                "employer",
                "employer_name",
            ],
        ),
        (
            "lobbying_firm",
            [
                "lobbying_firm",
                "firm_name",
                "lobbying_firm_name",
                "registrant_firm",
            ],
        ),
    ]:
        v = pick_first_present(row, keys)
        if v:
            out.append((role, v))
    # lobbyist names are often individuals; we skip by default.
    return out


def compute_overlaps(
    payments: List[Dict[str, Any]],
    lobbying: List[Dict[str, Any]],
    payments_path: str,
    lobbying_path: str,
) -> List[Dict[str, Any]]:
    # index lobbying by name_key
    lobby_index: Dict[str, List[Dict[str, Any]]] = {}
    for i, row in enumerate(lobbying):
        rec_id = row.get("id") or row.get("record_id") or row.get("filing_id") or str(i)
        row["__record_id"] = str(rec_id)
        for role, nm in get_lobby_entity_names(row):
            k = name_key(nm)
            if not k:
                continue
            lobby_index.setdefault(k, []).append({"role": role, "name": nm, "row": row})

    overlaps: List[Dict[str, Any]] = []

    for j, prow in enumerate(payments):
        pay_id = prow.get("id") or prow.get("payment_id") or prow.get("record_id") or str(j)
        prow["__record_id"] = str(pay_id)
        vname = get_payment_vendor_name(prow)
        if not vname:
            continue
        pk = name_key(vname)
        if not pk:
            continue
        if pk not in lobby_index:
            continue

        pzip = extract_zip(prow)
        for match in lobby_index[pk]:
            lrow = match["row"]
            lzip = extract_zip(lrow)
            confidence = "probable"
            match_type = "name_key"
            if pzip and lzip and pzip == lzip:
                confidence = "confirmed"
                match_type = "name_key+zip"

            overlaps.append(
                {
                    "vendor_name_raw": vname,
                    "vendor_name_normalized": normalize_org_name(vname),
                    "vendor_name_key": pk,
                    "vendor_zip": pzip,
                    "payment_record_id": prow["__record_id"],
                    "payment_source": payments_path,
                    "lobby_role": match["role"],
                    "lobby_entity_name_raw": match["name"],
                    "lobby_entity_name_normalized": normalize_org_name(match["name"]),
                    "lobby_zip": lzip,
                    "lobby_record_id": lrow.get("__record_id"),
                    "lobby_source": lobbying_path,
                    "match_type": match_type,
                    "confidence": confidence,
                    "evidence_chain": [
                        {
                            "dataset": "vendor_payments",
                            "record_id": prow["__record_id"],
                            "matched_field": "vendor_name",
                            "value": vname,
                        },
                        {
                            "dataset": "lobbying_disclosures",
                            "record_id": lrow.get("__record_id"),
                            "matched_field": match["role"],
                            "value": match["name"],
                        },
                        {"link": match_type, "key": pk},
                    ],
                }
            )

    return overlaps


def write_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    # flatten evidence_chain to JSON string
    out_rows: List[Dict[str, Any]] = []
    for r in rows:
        rr = dict(r)
        rr["evidence_chain"] = json.dumps(r.get("evidence_chain", []), ensure_ascii=False)
        out_rows.append(rr)

    fieldnames: List[str] = []
    for r in out_rows:
        for k in r.keys():
            if k not in fieldnames:
                fieldnames.append(k)

    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--payments", default=None, help="Path to vendor payments file (csv/tsv/jsonl)")
    ap.add_argument("--lobbying", default=None, help="Path to lobbying disclosures file (csv/tsv/jsonl)")
    ap.add_argument("--out-json", default="overlaps.json")
    ap.add_argument("--out-csv", default="overlaps.csv")
    args = ap.parse_args(argv)

    payments_path = args.payments
    lobbying_path = args.lobbying

    # reasonable defaults
    if payments_path is None:
        for cand in [
            "vendor_payments.csv",
            "vendor_payments.tsv",
            "vendor_payments.jsonl",
            "payments.csv",
            "payments.tsv",
            "payments.jsonl",
        ]:
            if os.path.exists(cand):
                payments_path = cand
                break

    if lobbying_path is None:
        for cand in [
            "lobbying_disclosures.csv",
            "lobbying_disclosures.tsv",
            "lobbying_disclosures.jsonl",
            "lobbying.csv",
            "lobbying.tsv",
            "lobbying.jsonl",
        ]:
            if os.path.exists(cand):
                lobbying_path = cand
                break

    if not payments_path or not os.path.exists(payments_path):
        print("ERROR: payments file not found. Provide --payments PATH.", file=sys.stderr)
        return 2
    if not lobbying_path or not os.path.exists(lobbying_path):
        print("ERROR: lobbying file not found. Provide --lobbying PATH.", file=sys.stderr)
        return 2

    payments = read_rows(payments_path)
    lobbying = read_rows(lobbying_path)

    overlaps = compute_overlaps(payments, lobbying, payments_path, lobbying_path)

    summary = {
        "payments_source": payments_path,
        "lobbying_source": lobbying_path,
        "payments_records": len(payments),
        "lobbying_records": len(lobbying),
        "overlap_records": len(overlaps),
        "confidence_counts": {
            "confirmed": sum(1 for o in overlaps if o.get("confidence") == "confirmed"),
            "probable": sum(1 for o in overlaps if o.get("confidence") == "probable"),
        },
    }

    write_json(args.out_json, {"summary": summary, "overlaps": overlaps})
    write_csv(args.out_csv, overlaps)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
