# Multi-Protocol Governance Audit Framework — Specification

Version 1.0.0 — framework for auditing on-chain governance of live DeFi protocols.

## 1. Purpose

This framework scores the governance systems of live protocols against a fixed
control catalogue, using only parameters verified against primary sources
(official documentation, governance contract references, executed proposals).
Every scored value carries a citation to the primary source that establishes
it. Where a parameter could not be verified from a primary source, the profile
records it as unverified and the engine scores it as a partial or failed check
rather than inventing a value.

## 2. Scope

Three protocols are audited in this release:

| Protocol  | Governance system            | Chain    |
|-----------|------------------------------|----------|
| Compound  | Governor Bravo + Timelock    | Ethereum |
| Uniswap   | Governor Bravo + Timelock    | Ethereum |
| Aave      | Governance V3 (Core + Executors) | Ethereum (Core), Polygon / Avalanche (voting) |

Each protocol profile (`protocols/<name>.json`) records: proposal threshold,
quorum, voting delay, voting period, timelock delay, grace period, execution
path, emergency powers / guardian, and at least one real executed proposal,
each with a citation.

## 3. Control catalogue

Six control areas, weights summing to 100, with 23 checks in total
(A1: 4, A2: 5, A3: 4, A4: 3, A5: 3, A6: 4).
Checks are scored pass (1.0), partial (0.5), fail (0.0). Area score is the
mean of its checks, scaled to 0–100. The protocol score is the weighted sum
of area scores. See `framework/scoring-rubric.md` and the machine-readable
`framework/rubric.json` (the engine's single source of truth).

| Area | Control area | Weight | What it tests |
|------|--------------|--------|---------------|
| A1 | Proposal lifecycle & access | 15 | Who can propose, proposer-power maintenance, autonomous path, action bounds |
| A2 | Voting & quorum rules | 20 | Delay, period, quorum definition, differential, cross-source consistency |
| A3 | Timelock & execution | 20 | Delay, grace period, timelock admin, permissionless execution |
| A4 | Treasury execution | 15 | Treasury only via timelock, observed outcomes, standing bounds |
| A5 | Emergency powers & guardians | 15 | Pause/cancel exists, powers limited, guardian composition public |
| A6 | Transparency & verifiability | 15 | Parameters published, contracts verified, proposal record public, no discrepancies |

## 4. Scoring rules

- A check is **pass** only when the primary source establishes the control
  fully and the observed record (executed proposals) does not contradict it.
- A check is **partial** when the control exists but is incomplete, bounded
  only in part, or verified from a secondary source / by inference.
- A check is **fail** when the control is absent, contradicted by an observed
  event, or the parameter is unverifiable from any primary source.
- A check marked `not_applicable` in a profile is excluded from the area mean
  (none are used in this release; all 23 checks apply to all three protocols).
- Scores are computed by `audit-engine/audit.py` from `framework/rubric.json`
  and the protocol profiles. Scores are never hand-written.

## 5. Severity rules

Each check declares a severity for its fail and partial outcomes in
`rubric.json`. Severity is a property of the control, not of the protocol:

- **High** — the gap can move protocol or treasury funds, or remove the
  timelock / quorum protection entirely.
- **Medium** — the gap weakens a protection, creates ambiguity in a core
  parameter, or hides who holds an emergency power.
- **Low** — a documentation, verifiability, or bounded-delegation gap with
  no direct path to fund movement.

## 6. Threat model

The framework is built around these attacker / failure scenarios:

1. **Treasury raid by narrow majority.** A bloc holding just over the
   quorum pushes a proposal that moves treasury funds to an address outside
   DAO recall (observed: Compound Proposal 289, 682,191 for vs 633,636
   against, 499,000 COMP). Controls: A2-4 (vote differential), A4-2
   (observed treasury outcomes), A4-3 (standing bounds).
2. **Parameter ambiguity.** Two primary sources state different values for
   the same parameter, so voters cannot know the rule they are voting under
   (observed: Uniswap voting period stated as 6 days in one process summary
   and 7 days in the body text and in the contract-level docs). Controls:
   A2-5, A6-4.
3. **Guardian capture / unaccountable emergency power.** An emergency actor
   can pause, cancel, or seize without a published identity or limit.
   Controls: A5-2, A5-3.
4. **Timelock bypass.** Execution without delay, or a timelock admin that is
   not the governor. Controls: A3-1, A3-3.
5. **Silent parameter change.** A core parameter (quorum, differential,
   creation threshold) is not published, so a change cannot be detected.
   Controls: A6-1, A2-3.
6. **Cross-chain voting complexity (Aave V3).** Voting on a second network
   via storage proofs adds a validation surface (snapshot block hash,
   proof submission). Controls: A2-1..A2-3 (parameters still defined),
   A6-1 (process documented).

## 7. Evidence standard

- Every parameter value in a profile cites a primary source by ID; the
  citation table is `citations.md`.
- Every finding is emitted by the engine from a check outcome; the trigger
  command and the observed vs expected values are recorded in `findings.md`.
- Every claim in `claims.md` maps to an evidence file, a script, and an
  output line.
- `scripts/run_all.sh` regenerates all outputs; `scripts/clean_reproduce.sh`
  re-runs from a fresh copy and requires byte-identical outputs.
- `docs/index.html` is generated from the engine output by
  `scripts/build_docs.py` and is therefore excluded from `SHA256SUMS`
  (stated here and in the README).

## 8. Limitations (honest)

- Compound's Governor Bravo mainnet contract address was not verified from a
  primary source at audit time (Compound docs use a `0x123...` placeholder);
  scored partial under A6-2.
- Uniswap's Timelock grace period (14 days) is inferred from the shared
  Compound Timelock codebase, not separately verified for Uniswap; scored
  partial under A3-2.
- Uniswap's guardian holder is not verified from a primary source; scored
  fail under A5-3.
- Aave Governance V3 Level 2 quorum and vote-differential exact values, and
  the on-chain proposal-creation threshold, are not stated in the current
  official docs; scored partial under A6-1 and A1-1.
- The engine scores documented parameters and observed proposals; it does
  not re-execute proposals on-chain and does not audit contract source code
  beyond the published parameters.
