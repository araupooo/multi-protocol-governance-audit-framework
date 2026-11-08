#!/usr/bin/env python3
"""Multi-Protocol Governance Audit Framework - audit engine.

Stdlib only. Loads framework/rubric.json and protocols/*.json, scores each
protocol against the rubric, and emits deterministic outputs:

  <name>.score.json   per-protocol scores, verdicts, findings
  <name>.report.md    rendered per-protocol audit report
  findings.json       global severity-ranked findings (F-01..)
  run-manifest.json   sha256 digests of the generated files (excluding itself)

Deterministic: no timestamps, no absolute paths, sorted keys. Run with:
  python3 audit-engine/audit.py --profiles protocols --out outputs/run1
"""
import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def area_score(checks, outcomes):
    """Mean of check values (pass=1, partial=0.5, fail=0), as a Fraction 0..1."""
    values = []
    for chk in checks:
        outcome = outcomes.get(chk["id"])
        if outcome is None:
            raise ValueError(f"missing outcome for check {chk['id']}")
        if outcome == "not_applicable":
            continue
        values.append(Fraction(str({"pass": 1.0, "partial": 0.5, "fail": 0.0}[outcome])))
    if not values:
        return Fraction(0)
    return sum(values) / len(values)


def fmt2(frac):
    """Format a Fraction in 0..1 as a 0..100 number with two decimals (half-up)."""
    hundredths = frac * 10000
    n = hundredths.numerator
    d = hundredths.denominator
    q, r = divmod(n, d)
    if 2 * r >= d:
        q += 1
    return q / 100.0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def render_report(profile, rubric, areas, total, findings_here):
    p = profile["protocol"]
    lines = []
    lines.append(f"# Audit Report — {p}")
    lines.append("")
    lines.append(f"Governance system: {profile['system']}. Chain: {profile['chain']}.")
    lines.append(f"Governance token: {profile['governance_token']}.")
    lines.append("")
    lines.append(f"**Overall score: {total:.2f} / 100**")
    lines.append("")
    lines.append("## Scores by control area")
    lines.append("")
    lines.append("| Area | Control area | Weight | Score / 100 |")
    lines.append("|------|--------------|--------|-------------|")
    for a in areas:
        lines.append(f"| {a['id']} | {a['name']} | {a['weight']} | {a['score']:.2f} |")
    lines.append("")
    lines.append("## Verified parameters")
    lines.append("")
    lines.append("| Parameter | Value | Verified | Sources |")
    lines.append("|-----------|-------|----------|---------|")
    for key in sorted(profile["parameters"].keys()):
        par = profile["parameters"][key]
        val = par["value"]
        if val is None:
            val = "(not stated / not present)"
        lines.append(f"| {key} | {val} {par['unit']} | {'yes' if par['verified'] else 'no'} | {', '.join(par['source'])} |")
    notes = {k: v for k, v in profile["parameters"].items() if v.get("note")}
    if notes:
        lines.append("")
        lines.append("### Parameter notes")
        lines.append("")
        for key in sorted(notes):
            lines.append(f"- **{key}**: {notes[key]['note']}")
    lines.append("")
    lines.append("## Per-check verdicts")
    lines.append("")
    lines.append("| Check | Control | Verdict |")
    lines.append("|-------|---------|---------|")
    for area in rubric["areas"]:
        for chk in area["checks"]:
            outcome = profile["checks"][chk["id"]]
            lines.append(f"| {chk['id']} | {chk['control']} | {outcome} |")
    lines.append("")
    lines.append("## Findings (this protocol)")
    lines.append("")
    if findings_here:
        for f in findings_here:
            lines.append(f"### {f['id']} — {f['severity']} — {f['check']} {f['control']}")
            lines.append("")
            lines.append(f"Observed: {f['observed']}")
            lines.append("")
            lines.append(f"Expected: {f['expected']}")
            lines.append("")
            lines.append(f"Evidence: {', '.join(f['evidence'])}")
            lines.append("")
    else:
        lines.append("No findings.")
        lines.append("")
    lines.append("## Executed proposal (evidence)")
    lines.append("")
    ep = profile["executed_proposal"]
    lines.append(f"- ID: {ep['id']}")
    lines.append(f"- Title: {ep['title']}")
    lines.append(f"- Date: {ep['date']}")
    lines.append(f"- Outcome: {ep['outcome']}")
    lines.append(f"- Votes for: {ep['votes_for']}")
    lines.append(f"- Votes against: {ep['votes_against']}")
    lines.append(f"- Note: {ep['note']}")
    lines.append(f"- Sources: {', '.join(ep['sources'])}")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("Scored by audit-engine/audit.py from framework/rubric.json and this "
                 "protocol's profile. Every parameter value cites a primary source; "
                 "unverified values are recorded as such and scored partial or fail, "
                 "never invented. See citations.md for the source table.")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Governance audit engine")
    ap.add_argument("--rubric", default="framework/rubric.json")
    ap.add_argument("--profiles", default="protocols")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rubric = load_json(args.rubric)
    profile_paths = sorted(Path(args.profiles).glob("*.json"))
    if not profile_paths:
        print("audit.py: no profiles found", file=sys.stderr)
        return 1
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    total_checks = sum(len(a["checks"]) for a in rubric["areas"])
    print(f"audit.py: loaded rubric v{rubric['version']} "
          f"({len(rubric['areas'])} areas, {total_checks} checks)")

    # Pass 1: validate, score, collect findings (no IDs yet).
    per_protocol = []
    all_findings = []
    for ppath in profile_paths:
        profile = load_json(ppath)
        name = ppath.stem
        for area in rubric["areas"]:
            for chk in area["checks"]:
                if chk["id"] not in profile["checks"]:
                    print(f"audit.py: ERROR {name} missing outcome for {chk['id']}",
                          file=sys.stderr)
                    return 1
                if profile["checks"][chk["id"]] not in ("pass", "partial", "fail", "not_applicable"):
                    print(f"audit.py: ERROR {name} bad outcome for {chk['id']}",
                          file=sys.stderr)
                    return 1
        for key, par in profile["parameters"].items():
            if not par.get("source"):
                print(f"audit.py: ERROR {name} parameter {key} has no source",
                      file=sys.stderr)
                return 1
        for area in rubric["areas"]:
            for chk in area["checks"]:
                if profile["checks"][chk["id"]] != "pass" and chk["id"] not in profile.get("check_notes", {}):
                    print(f"audit.py: ERROR {name} non-pass check {chk['id']} has no check_note",
                          file=sys.stderr)
                    return 1

        areas_out = []
        total = Fraction(0)
        for area in rubric["areas"]:
            frac = area_score(area["checks"], profile["checks"])
            areas_out.append({"id": area["id"], "name": area["name"],
                              "weight": area["weight"], "score": fmt2(frac)})
            total += frac * area["weight"]
        total_score = fmt2(total / 100)

        findings_here = []
        for area in rubric["areas"]:
            for chk in area["checks"]:
                outcome = profile["checks"][chk["id"]]
                if outcome == "pass":
                    continue
                sev = chk["severity"]["fail" if outcome == "fail" else "partial"]
                findings_here.append({
                    "protocol": profile["protocol"],
                    "check": chk["id"],
                    "control": chk["control"],
                    "outcome": outcome,
                    "severity": sev,
                    "observed": profile["check_notes"][chk["id"]],
                    "expected": chk["criteria"]["pass"],
                    "evidence": sorted(
                        {s for k, par in profile["parameters"].items() for s in par["source"]}
                        | set(profile["executed_proposal"]["sources"])),
                    "trigger": "bash scripts/run_all.sh",
                })
        all_findings.extend(findings_here)
        per_protocol.append({"name": name, "profile": profile, "areas": areas_out,
                             "total": total_score, "findings": findings_here})

    # Global finding IDs: severity-ranked (High, Medium, Low), then protocol, then check.
    sev_rank = {"High": 0, "Medium": 1, "Low": 2}
    all_findings.sort(key=lambda f: (sev_rank[f["severity"]], f["protocol"].lower(), f["check"]))
    for i, f in enumerate(all_findings, start=1):
        f["id"] = f"F-{i:02d}"
    all_findings.sort(key=lambda f: f["id"])

    # Pass 2: write outputs.
    generated = []
    for entry in per_protocol:
        name = entry["name"]
        profile = entry["profile"]
        findings_here = sorted(entry["findings"], key=lambda f: f["id"])
        score_doc = {
            "protocol": profile["protocol"],
            "system": profile["system"],
            "framework_version": rubric["version"],
            "score": entry["total"],
            "areas": entry["areas"],
            "checks": {chk["id"]: profile["checks"][chk["id"]]
                       for area in rubric["areas"] for chk in area["checks"]},
            "findings": [f["id"] for f in findings_here],
        }
        spath = outdir / f"{name}.score.json"
        spath.write_text(json.dumps(score_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        generated.append(spath)
        report = render_report(profile, rubric, entry["areas"], entry["total"], findings_here)
        rpath = outdir / f"{name}.report.md"
        rpath.write_text(report, encoding="utf-8")
        generated.append(rpath)
        n_high = sum(1 for f in findings_here if f["severity"] == "High")
        n_med = sum(1 for f in findings_here if f["severity"] == "Medium")
        n_low = sum(1 for f in findings_here if f["severity"] == "Low")
        print(f"audit.py: profile {name}: {total_checks} checks, "
              f"score {entry['total']:.2f}, findings {len(findings_here)} "
              f"({n_high} High, {n_med} Medium, {n_low} Low)")

    fpath = outdir / "findings.json"
    fpath.write_text(json.dumps({"findings": all_findings}, indent=2, sort_keys=True) + "\n",
                     encoding="utf-8")
    generated.append(fpath)
    n_high = sum(1 for f in all_findings if f["severity"] == "High")
    n_med = sum(1 for f in all_findings if f["severity"] == "Medium")
    n_low = sum(1 for f in all_findings if f["severity"] == "Low")
    print(f"audit.py: total findings {len(all_findings)} "
          f"({n_high} High, {n_med} Medium, {n_low} Low)")

    manifest = {"files": {p.name: sha256_file(p) for p in sorted(generated, key=lambda x: x.name)}}
    mpath = outdir / "run-manifest.json"
    mpath.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"audit.py: wrote {len(generated) + 1} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
