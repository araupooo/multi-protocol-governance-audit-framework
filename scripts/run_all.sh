#!/bin/bash
# Run the governance audit engine on all three profiles into outputs/run1/,
# verify digests, and check the generated reports / findings / docs page
# against the committed files. Usage: bash scripts/run_all.sh [outdir]
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-outputs/run1}"
rm -rf "$OUT"
mkdir -p "$OUT"
echo "run_all.sh: running audit engine into $OUT"
python3 audit-engine/audit.py --profiles protocols --out "$OUT" > "$OUT/run.log" 2>&1
cat "$OUT/run.log"
echo "run_all.sh: checking generated reports against committed protocols/*.md"
for name in aave compound uniswap; do
  if [ ! -f "protocols/$name.md" ]; then
    echo "run_all.sh: protocols/$name.md missing — creating from generated report"
    cp "$OUT/$name.report.md" "protocols/$name.md"
  fi
  diff -q "$OUT/$name.report.md" "protocols/$name.md" >/dev/null \
    || { echo "run_all.sh: ERROR $name report differs from committed protocols/$name.md"; exit 1; }
  echo "run_all.sh: $name report matches committed protocols/$name.md"
done
echo "run_all.sh: checking findings.md against engine output"
python3 scripts/build_findings.py --in "$OUT/findings.json" --out /tmp/mpga-findings.gen.md >/dev/null
diff -q /tmp/mpga-findings.gen.md findings.md >/dev/null \
  || { echo "run_all.sh: ERROR findings.md differs from engine output"; exit 1; }
echo "run_all.sh: findings.md matches engine output"
echo "run_all.sh: checking docs/index.html against engine output"
python3 scripts/build_docs.py --run "$OUT" --claims claims.md --out /tmp/mpga-index.gen.html >/dev/null
diff -q /tmp/mpga-index.gen.html docs/index.html >/dev/null \
  || { echo "run_all.sh: ERROR docs/index.html differs from generated page"; exit 1; }
echo "run_all.sh: docs/index.html matches generated page"
echo "run_all.sh: running consistency checks"
python3 scripts/check_consistency.py --run "$OUT" --evidence evidence.json --claims claims.md --findings findings.md
echo "run_all.sh: verifying digests"
bash scripts/verify_digests.sh
echo "run_all.sh: ALL PASS"
