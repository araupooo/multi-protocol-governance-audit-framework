# Audit Report — Uniswap

Governance system: Governor Bravo + Timelock. Chain: Ethereum Mainnet.
Governance token: UNI.

**Overall score: 75.88 / 100**

## Scores by control area

| Area | Control area | Weight | Score / 100 |
|------|--------------|--------|-------------|
| A1 | Proposal lifecycle & access | 15 | 87.50 |
| A2 | Voting & quorum rules | 20 | 70.00 |
| A3 | Timelock & execution | 20 | 87.50 |
| A4 | Treasury execution | 15 | 83.33 |
| A5 | Emergency powers & guardians | 15 | 50.00 |
| A6 | Transparency & verifiability | 15 | 75.00 |

## Verified parameters

| Parameter | Value | Verified | Sources |
|-----------|-------|----------|---------|
| execution | any address may execute after the timelock delay call | yes | C-UNI-PROC-ORIG |
| governor_bravo_address | 0x408ED6354d4973f66138C91495F2f2FCbd8724C3 address | yes | C-UNI-TECHREF |
| grace_period_days | 14 days | no | C-UNI-PROCESS-MIRROR |
| guardian | Governor Bravo guardian can cancel pending proposals role | no | C-UNI-PROCESS-MIRROR |
| majority_rule | for > against votes | yes | C-UNI-PROC-ORIG |
| max_actions_per_proposal | 10 actions | yes | C-UNI-PROCESS-MIRROR |
| proposal_threshold_uni_current | 1000000 UNI delegated | yes | C-UNI-PROC-2023 |
| proposal_threshold_uni_original | 2500000 UNI delegated | yes | C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR |
| quorum_for_votes_uni | 40000000 UNI for-votes | yes | C-UNI-PROC-2023, C-UNI-PROC-ORIG |
| rfc_minimum_days | 7 days | yes | C-UNI-PROC-2023 |
| temperature_check | 5 days; at least 10M UNI for, and for > against Snapshot poll | yes | C-UNI-PROC-2023 |
| timelock_address | 0x1a9C8182C09F50C8318d769245beA52c32BE35BC address | yes | C-UNI-TECHREF |
| timelock_admin | Governor Bravo contract | yes | C-UNI-TECHREF, C-UNI-CONTRACT-READS |
| timelock_delay_days | 2 days | yes | C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-TECHREF |
| timelock_delay_seconds | 172800 seconds | no | C-UNI-CONTRACT-READS |
| vote_differential | (not stated / not present) votes | no | C-UNI-PROC-2023 |
| voting_delay_days | 2 days | yes | C-UNI-PROC-2023, C-UNI-PROC-ORIG |
| voting_period_blocks_secondary | 40320 blocks | no | C-UNI-CONTRACT-READS |
| voting_period_days_body | 7 days | yes | C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR |
| voting_period_days_summary | 6 days | yes | C-UNI-PROC-2023 |
| voting_power | UNI delegated, snapshot at proposal start votes | yes | C-UNI-PROCESS-MIRROR |

### Parameter notes

- **grace_period_days**: NOT SEPARATELY VERIFIED for Uniswap: 14 days is the grace period of the shared Compound Timelock contract; Uniswap uses the same Timelock codebase.
- **guardian**: NOT VERIFIED: the guardian holder / identity was not verified from a primary source at audit time.
- **proposal_threshold_uni_current**: Current process (Jan 2023 update): at least 1M UNI delegated to submit an on-chain proposal.
- **proposal_threshold_uni_original**: Original process: 2.5M UNI (0.25% of supply). Lowered to 1M UNI by the Dec 2022 governance vote summarised in the Jan 2023 update.
- **quorum_for_votes_uni**: 4% of 1B supply; only for-votes count toward quorum.
- **timelock_admin**: Official technical reference lists the Timelock and Governor Bravo as the active mainnet contracts.
- **timelock_delay_seconds**: SECONDARY SOURCE (Oct 2026 contract reads): timelock delay is 172,800 seconds (2 days), admin is Governor Bravo.
- **vote_differential**: NOT PRESENT: no vote-differential rule; a proposal passes on a simple majority plus the 40M for-votes quorum.
- **voting_period_blocks_secondary**: SECONDARY SOURCE (Oct 2026 contract reads): on-chain votingPeriod is 40,320 blocks, closer to 6 days than 7 at current block times. Corroborates the 6-day figure; not a primary source.
- **voting_period_days_body**: Same Jan 2023 post, body text: 'a seven day voting period begins'. The older process docs and the process mirror also state 7 days. DISCREPANCY: 6 vs 7 days within one primary source.
- **voting_period_days_summary**: Jan 2023 update Phase 3 timeframe line states '2 day waiting period, 6 day voting period, 2 day timelock'.
- **voting_power**: If the proposer does not maintain their vote weight throughout the voting period, the proposal may be canceled by anyone.

## Per-check verdicts

| Check | Control | Verdict |
|-------|---------|---------|
| A1-1 | Proposal threshold exists and is public | pass |
| A1-2 | Proposer must maintain delegated power through voting | pass |
| A1-3 | Permissionless / autonomous proposal path | partial |
| A1-4 | Actions per proposal bounded | pass |
| A2-1 | Voting delay (review period) >= 1 day | pass |
| A2-2 | Voting period >= 3 days | pass |
| A2-3 | Quorum defined as explicit for-votes threshold | pass |
| A2-4 | Vote-differential / anti-close-call rule | partial |
| A2-5 | Voting period consistent across primary sources | fail |
| A3-1 | Timelock delay >= 1 day | pass |
| A3-2 | Grace period defined | partial |
| A3-3 | Timelock admin is the governor | pass |
| A3-4 | Execution is permissionless after delay | pass |
| A4-1 | Treasury moves only via timelocked governance | pass |
| A4-2 | No observed treasury transfer outside DAO recall | pass |
| A4-3 | Standing bounds / whitelists on treasury operations | partial |
| A5-1 | Emergency pause / cancel power exists and is documented | pass |
| A5-2 | Emergency powers are limited | partial |
| A5-3 | Guardian composition is public | fail |
| A6-1 | All lifecycle parameters published in official docs | pass |
| A6-2 | Governance contracts verified with published addresses | pass |
| A6-3 | Executed proposal record publicly accessible | pass |
| A6-4 | No unresolved parameter discrepancy across primary sources | fail |

## Findings (this protocol)

### F-05 — Medium — A2-4 Vote-differential / anti-close-call rule

Observed: No differential rule; majority plus 40M for-votes quorum only.

Expected: Winning option must exceed the runner-up by a stated margin

Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF

### F-06 — Medium — A2-5 Voting period consistent across primary sources

Observed: Jan 2023 process update states 6 days in its Phase 3 timeframe line and 7 days in its body text.

Expected: All primary sources agree

Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF

### F-07 — Medium — A5-2 Emergency powers are limited

Observed: Guardian cancel power is documented; a pause power and its limits are not verified in the sources used.

Expected: Documented limits: cannot seize funds, cannot unpause, cannot upgrade

Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF

### F-08 — Medium — A5-3 Guardian composition is public

Observed: Guardian holder not verifiable from any primary source used.

Expected: Multisig threshold and signers published

Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF

### F-09 — Medium — A6-4 No unresolved parameter discrepancy across primary sources

Observed: Same 6-vs-7-day discrepancy as A2-5.

Expected: All primary sources agree on all parameters

Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF

### F-15 — Low — A1-3 Permissionless / autonomous proposal path

Observed: No autonomous-proposal path; the 1M UNI threshold is the only gate.

Expected: Any address can lock a small amount to create an autonomous proposal, or equivalent

Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF

### F-16 — Low — A3-2 Grace period defined

Observed: Grace period 14 days inferred from the shared Timelock codebase, not separately verified for Uniswap.

Expected: Expiry window stated in docs

Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF

### F-17 — Low — A4-3 Standing bounds / whitelists on treasury operations

Observed: Each treasury transfer needs its own vote; no standing per-operation bounds or whitelists.

Expected: Explicit per-operation bounds or whitelists

Evidence: C-UNI-CONTRACT-READS, C-UNI-PROC-2023, C-UNI-PROC-ORIG, C-UNI-PROCESS-MIRROR, C-UNI-TECHREF, C-UNI-UNIF

## Executed proposal (evidence)

- ID: UNIfication
- Title: UNIfication proposal
- Date: 2025-12-18 (on-chain), voting 2025-12-19 to 2025-12-25
- Outcome: Passed
- Votes for: 125342017
- Votes against: 742
- Note: Passed with 125,342,017 UNI for vs 742 against (above the 40M quorum). Activates the protocol fee switch and a one-time burn of 100M UNI from the treasury after the 2-day timelock, plus a 20M UNI/year growth budget.
- Sources: C-UNI-UNIF

## Method

Scored by audit-engine/audit.py from framework/rubric.json and this protocol's profile. Every parameter value cites a primary source; unverified values are recorded as such and scored partial or fail, never invented. See citations.md for the source table.
