# Findings — Multi-Protocol Governance Audit Framework

Total: 17 findings — 1 High, 8 Medium, 8 Low.
Every finding is emitted by the audit engine from a rubric check outcome.
Trigger for every finding: `bash scripts/run_all.sh`

## Severity-ranked findings

### F-01 — High — Compound — A4-2 No observed treasury transfer outside DAO recall

- Outcome: fail
- Observed: Proposal 289 moved 499,000 COMP to a group-controlled treasury the DAO could not recall.
- Expected: No executed proposal moved funds to an address the DAO cannot recall
- Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8
- Trigger: `bash scripts/run_all.sh`

### F-02 — Medium — Aave — A1-1 Proposal threshold exists and is public

- Outcome: partial
- Observed: Snapshot author gate (80,000 AAVE) is public; the on-chain creation threshold is not stated in the current docs.
- Expected: Exact threshold stated in official docs and readable on-chain
- Evidence: C-AAVE-ARFC, C-AAVE-DOCS, C-AAVE-L2RFC
- Trigger: `bash scripts/run_all.sh`

### F-03 — Medium — Aave — A6-1 All lifecycle parameters published in official docs

- Outcome: partial
- Observed: Level 2 quorum and vote-differential exact values are not stated in the current docs.
- Expected: Every parameter (threshold, quorum, delay, period, timelock, grace) stated
- Evidence: C-AAVE-ARFC, C-AAVE-DOCS, C-AAVE-L2RFC
- Trigger: `bash scripts/run_all.sh`

### F-04 — Medium — Compound — A2-4 Vote-differential / anti-close-call rule

- Outcome: partial
- Observed: No differential rule: Proposal 289 passed with 682,191 for vs 633,636 against (51.9%).
- Expected: Winning option must exceed the runner-up by a stated margin
- Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8
- Trigger: `bash scripts/run_all.sh`

### F-05 — Medium — Uniswap — A2-4 Vote-differential / anti-close-call rule

- Outcome: partial
- Observed: No differential rule; majority plus 40M for-votes quorum only.
- Expected: Winning option must exceed the runner-up by a stated margin
- Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF
- Trigger: `bash scripts/run_all.sh`

### F-06 — Medium — Uniswap — A2-5 Voting period consistent across primary sources

- Outcome: fail
- Observed: Jan 2023 process update states 6 days in its Phase 3 timeframe line and 7 days in its body text.
- Expected: All primary sources agree
- Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF
- Trigger: `bash scripts/run_all.sh`

### F-07 — Medium — Uniswap — A5-2 Emergency powers are limited

- Outcome: partial
- Observed: Guardian cancel power is documented; a pause power and its limits are not verified in the sources used.
- Expected: Documented limits: cannot seize funds, cannot unpause, cannot upgrade
- Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF
- Trigger: `bash scripts/run_all.sh`

### F-08 — Medium — Uniswap — A5-3 Guardian composition is public

- Outcome: fail
- Observed: Guardian holder not verifiable from any primary source used.
- Expected: Multisig threshold and signers published
- Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF
- Trigger: `bash scripts/run_all.sh`

### F-09 — Medium — Uniswap — A6-4 No unresolved parameter discrepancy across primary sources

- Outcome: fail
- Observed: Same 6-vs-7-day discrepancy as A2-5.
- Expected: All primary sources agree on all parameters
- Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF
- Trigger: `bash scripts/run_all.sh`

### F-10 — Low — Aave — A1-3 Permissionless / autonomous proposal path

- Outcome: partial
- Observed: No built-in autonomous-proposal path; a one-off autonomous contract was built for the 2022 Level 2 update.
- Expected: Any address can lock a small amount to create an autonomous proposal, or equivalent
- Evidence: C-AAVE-ARFC, C-AAVE-DOCS, C-AAVE-L2RFC
- Trigger: `bash scripts/run_all.sh`

### F-11 — Low — Aave — A6-2 Governance contracts verified with published addresses

- Outcome: partial
- Observed: Governance contract addresses are linked from the docs but were not verified from a primary source at audit time.
- Expected: Contract addresses published in official reference and verifiable
- Evidence: C-AAVE-ARFC, C-AAVE-DOCS, C-AAVE-L2RFC
- Trigger: `bash scripts/run_all.sh`

### F-12 — Low — Compound — A4-3 Standing bounds / whitelists on treasury operations

- Outcome: partial
- Observed: Each treasury transfer needs its own vote; no standing per-operation bounds or whitelists.
- Expected: Explicit per-operation bounds or whitelists
- Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8
- Trigger: `bash scripts/run_all.sh`

### F-13 — Low — Compound — A5-3 Guardian composition is public

- Outcome: partial
- Observed: Pause Guardian is a named multisig, but its signer list was not verified from a primary source.
- Expected: Multisig threshold and signers published
- Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8
- Trigger: `bash scripts/run_all.sh`

### F-14 — Low — Compound — A6-2 Governance contracts verified with published addresses

- Outcome: partial
- Observed: Governor Bravo mainnet address not verified from a primary source at audit time.
- Expected: Contract addresses published in official reference and verifiable
- Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8
- Trigger: `bash scripts/run_all.sh`

### F-15 — Low — Uniswap — A1-3 Permissionless / autonomous proposal path

- Outcome: partial
- Observed: No autonomous-proposal path; the 1M UNI threshold is the only gate.
- Expected: Any address can lock a small amount to create an autonomous proposal, or equivalent
- Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF
- Trigger: `bash scripts/run_all.sh`

### F-16 — Low — Uniswap — A3-2 Grace period defined

- Outcome: partial
- Observed: Grace period 14 days inferred from the shared Timelock codebase, not separately verified for Uniswap.
- Expected: Expiry window stated in docs
- Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF
- Trigger: `bash scripts/run_all.sh`

### F-17 — Low — Uniswap — A4-3 Standing bounds / whitelists on treasury operations

- Outcome: partial
- Observed: Each treasury transfer needs its own vote; no standing per-operation bounds or whitelists.
- Expected: Explicit per-operation bounds or whitelists
- Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF
- Trigger: `bash scripts/run_all.sh`

## Findings by protocol

- Aave: F-02, F-03, F-10, F-11
- Compound: F-01, F-04, F-12, F-13, F-14
- Uniswap: F-05, F-06, F-07, F-08, F-09, F-15, F-16, F-17
