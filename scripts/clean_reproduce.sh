#!/bin/bash
# Re-run the whole audit from a fresh copy of the pack and require
# byte-identical outputs. Usage: bash scripts/clean_reproduce.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PACK="$(pwd)"
CLEAN="/tmp/mpga-clean"
echo "clean_reproduce.sh: copying pack to $CLEAN (excluding outputs and .git)"
rm -rf "$CLEAN"
mkdir -p "$CLEAN"
tar --exclude=./outputs --exclude=./.git --exclude=./submission-text-final.txt -cf - . | (cd "$CLEAN" && tar xf -)
echo "clean_reproduce.sh: running audit in the fresh copy"
(cd "$CLEAN" && bash scripts/run_all.sh outputs/run2-clean > /tmp/mpga-clean-run.log 2>&1)
cat /tmp/mpga-clean-run.log
echo "clean_reproduce.sh: diffing outputs/run1 against outputs/run2-clean"
if diff -r "$PACK/outputs/run1" "$CLEAN/outputs/run2-clean" > /tmp/mpga-clean.diff; then
  echo "clean_reproduce.sh: MATCH — outputs/run1 and outputs/run2-clean are byte-identical"
  echo "clean_reproduce.sh: copying clean outputs into pack outputs/run2-clean"
  mkdir -p "$PACK/outputs/run2-clean"
  cp "$CLEAN/outputs/run2-clean/"* "$PACK/outputs/run2-clean/"
else
  echo "clean_reproduce.sh: MISMATCH"
  cat /tmp/mpga-clean.diff
  exit 1
fi
