#!/usr/bin/env python3
"""Consistency checks between engine output, evidence.json, claims.md, findings.md.

Usage: python3 scripts/check_consistency.py --run outputs/run1 --evidence evidence.json --claims claims.md --findings findings.md
Exits non-zero on any mismatch.
"""
import argparse
import json
import re
import sys


def main():
    ap = argparse.ArgumentParser(description="Consistency checks")
    ap.add_argument("--run", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--claims", required=True)
    ap.add_argument("--findings", required=True)
    args = ap.parse_args()
    errors = []
    import pathlib
    rundir = pathlib.Path(args.run)
    findings = json.load(open(rundir / "findings.json", encoding="utf-8"))["findings"]
    scores = {}
    for sp in sorted(rundir.glob("*.score.json")):
        doc = json.load(open(sp, encoding="utf-8"))
        scores[doc["protocol"]] = doc

    evidence = json.load(open(args.evidence, encoding="utf-8"))
    for proto, ev in evidence["protocols"].items():
        if proto not in scores:
            errors.append(f"evidence.json: protocol {proto} has no score file")
            continue
        if abs(scores[proto]["score"] - ev["score"]) > 0.001:
            errors.append(f"evidence.json: {proto} score {ev['score']} != engine {scores[proto]['score']}")
        ev_findings = [f["id"] for f in findings if f["protocol"] == proto]
        if sorted(ev["findings"]) != sorted(ev_findings):
            errors.append(f"evidence.json: {proto} findings {ev['findings']} != engine {ev_findings}")
    n_high = sum(1 for f in findings if f["severity"] == "High")
    n_med = sum(1 for f in findings if f["severity"] == "Medium")
    n_low = sum(1 for f in findings if f["severity"] == "Low")
    counts = {"total": len(findings), "High": n_high, "Medium": n_med, "Low": n_low}
    if evidence["findings_counts"] != counts:
        errors.append(f"evidence.json: findings_counts {evidence['findings_counts']} != engine {counts}")

    claims_text = open(args.claims, encoding="utf-8").read()
    claim_ids = re.findall(r"^### (C-\d+) —", claims_text, flags=re.M)
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("claims.md: duplicate claim IDs")
    for cid in claim_ids:
        block = claims_text.split(f"### {cid}")[1].split("### ")[0]
        m = re.search(r"^Evidence: (.*)$", block, flags=re.M)
        if not m:
            errors.append(f"claims.md: {cid} has no Evidence line")
            continue
        for ref in m.group(1).split(","):
            ref = ref.strip()
            if not ref:
                continue
            # evidence references are files, or file:line
            fname = ref.split(":")[0]
            # claims cite the canonical run dir (outputs/run1); when this
            # check runs against another run dir (e.g. outputs/run2-clean
            # in a fresh copy), remap the prefix to that run dir.
            if fname.startswith("outputs/run1/"):
                fname = args.run.rstrip("/") + "/" + fname[len("outputs/run1/"):]
            if not pathlib.Path(fname).exists():
                errors.append(f"claims.md: {cid} cites missing file {fname}")

    citations_text = open("citations.md", encoding="utf-8").read()
    cid_pat = r"C-(?:COMP|UNI|AAVE|BRAVO)-[A-Z0-9-]+"
    defined_ids = set(re.findall(r"^### (" + cid_pat + r") —", citations_text, flags=re.M))
    for prof in sorted(pathlib.Path("protocols").glob("*.json")):
        used_ids = set(re.findall(cid_pat, prof.read_text(encoding="utf-8")))
        missing = used_ids - defined_ids
        if missing:
            errors.append(f"{prof}: citation IDs not defined in citations.md: {sorted(missing)}")

    findings_text = open(args.findings, encoding="utf-8").read()
    for f in findings:
        if f["id"] not in findings_text:
            errors.append(f"findings.md: missing {f['id']}")

    if errors:
        for e in errors:
            print(f"check_consistency.py: ERROR {e}", file=sys.stderr)
        return 1
    print(f"check_consistency.py: OK ({len(scores)} protocols, {len(findings)} findings, "
          f"{len(claim_ids)} claims)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
