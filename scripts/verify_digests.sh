#!/bin/bash
# Verify SHA256SUMS for every static pack file (excludes generated outputs,
# docs/index.html, and this file's own list). Usage: bash scripts/verify_digests.sh
set -euo pipefail
cd "$(dirname "$0")/.."
sha256sum -c SHA256SUMS
