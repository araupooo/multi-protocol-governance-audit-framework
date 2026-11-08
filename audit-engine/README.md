# Audit Engine

`audit.py` — Python 3, standard library only, runs offline.

Usage (from the pack root):

```
python3 audit-engine/audit.py --profiles protocols --out outputs/run1
```

It loads `framework/rubric.json` and every `protocols/*.json` profile,
validates that each rubric check has an outcome and each non-pass check
carries a note, scores each protocol (area score = mean of its checks;
protocol score = weighted sum), and writes deterministic outputs
(no timestamps, no absolute paths, sorted keys):

- `<name>.score.json` — per-protocol scores, verdicts, finding check IDs
- `<name>.report.md` — rendered per-protocol audit report
- `findings.json` — global severity-ranked findings (F-01…)
- `run-manifest.json` — sha256 digests of the generated files

`scripts/run_all.sh` runs the engine and checks the generated reports
against the committed `protocols/*.md` reports (they must match byte for
byte); `scripts/clean_reproduce.sh` re-runs from a fresh copy and requires
byte-identical outputs.
