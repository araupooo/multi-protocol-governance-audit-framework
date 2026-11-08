#!/usr/bin/env python3
"""Build findings.md from outputs/<run>/findings.json (deterministic).

Usage: python3 scripts/build_findings.py --in outputs/run1/findings.json --out findings.md
"""
import argparse
import json


def main():
    ap = argparse.ArgumentParser(description="Build findings.md")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    data = json.load(open(args.inp, encoding="utf-8"))
    findings = data["findings"]
    n_high = sum(1 for f in findings if f["severity"] == "High")
    n_med = sum(1 for f in findings if f["severity"] == "Medium")
    n_low = sum(1 for f in findings if f["severity"] == "Low")
    lines = []
    lines.append("# Findings — Multi-Protocol Governance Audit Framework")
    lines.append("")
    lines.append(f"Total: {len(findings)} findings — {n_high} High, {n_med} Medium, {n_low} Low.")
    lines.append("Every finding is emitted by the audit engine from a rubric check outcome.")
    lines.append("Trigger for every finding: `bash scripts/run_all.sh`")
    lines.append("")
    lines.append("## Severity-ranked findings")
    lines.append("")
    for f in findings:
        lines.append(f"### {f['id']} — {f['severity']} — {f['protocol']} — {f['check']} {f['control']}")
        lines.append("")
        lines.append(f"- Outcome: {f['outcome']}")
        lines.append(f"- Observed: {f['observed']}")
        lines.append(f"- Expected: {f['expected']}")
        lines.append(f"- Evidence: {', '.join(f['evidence'])}")
        lines.append(f"- Trigger: `{f['trigger']}`")
        lines.append("")
    lines.append("## Findings by protocol")
    lines.append("")
    for proto in sorted({f["protocol"] for f in findings}):
        ids = [f["id"] for f in findings if f["protocol"] == proto]
        lines.append(f"- {proto}: {', '.join(ids)}")
    lines.append("")
    open(args.out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"build_findings.py: wrote {len(findings)} findings to {args.out}")


if __name__ == "__main__":
    main()
