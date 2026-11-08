# Audit Report — Aave

Governance system: Governance V3 (Core + Executors + PayloadsController). Chain: Ethereum Mainnet (Core); Polygon / Avalanche (voting networks).
Governance token: AAVE.

**Overall score: 92.50 / 100**

## Scores by control area

| Area | Control area | Weight | Score / 100 |
|------|--------------|--------|-------------|
| A1 | Proposal lifecycle & access | 15 | 75.00 |
| A2 | Voting & quorum rules | 20 | 100.00 |
| A3 | Timelock & execution | 20 | 100.00 |
| A4 | Treasury execution | 15 | 100.00 |
| A5 | Emergency powers & guardians | 15 | 100.00 |
| A6 | Transparency & verifiability | 15 | 75.00 |

## Verified parameters

| Parameter | Value | Verified | Sources |
|-----------|-------|----------|---------|
| execution | any address may call executePayload() on the PayloadsController after the timelock expires call | yes | C-AAVE-DOCS |
| level1_grace_days | 7 days | yes | C-AAVE-DOCS |
| level1_quorum_aave | 320000 AAVE/stkAAVE/aAAVE | yes | C-AAVE-DOCS |
| level1_timelock_days | 1 days | yes | C-AAVE-DOCS |
| level1_vote_differential_aave | 80000 AAVE | yes | C-AAVE-ARFC |
| level1_voting_delay_days | 1 days | yes | C-AAVE-DOCS |
| level1_voting_period_days | 3 days | yes | C-AAVE-DOCS |
| level2_proposition_power_aave | 320000 AAVE proposition power | yes | C-AAVE-L2RFC |
| level2_quorum | (not stated / not present) AAVE | no | C-AAVE-DOCS |
| level2_timelock_days | 7 days | yes | C-AAVE-DOCS |
| level2_voting_period_days | 10 days | yes | C-AAVE-DOCS |
| onchain_creation_threshold | (not stated / not present) AAVE proposition power | no | C-AAVE-DOCS |
| proposal_maintenance | proposition power must be maintained; below-threshold proposals can be cancelled by anyone rule | yes | C-AAVE-L2RFC |
| snapshot_author_gate | approved author list, or at least 80,000 AAVE proposition power AAVE | yes | C-AAVE-DOCS |
| snapshot_delay_days | 1 days | yes | C-AAVE-DOCS |
| snapshot_threshold_aave | 320000 AAVE | yes | C-AAVE-DOCS |
| snapshot_voting_days | 3 days | yes | C-AAVE-DOCS |
| voting_networks | Polygon PoS, Avalanche C-Chain, Ethereum Mainnet (backup) networks | yes | C-AAVE-DOCS |
| voting_power | AAVE + stkAAVE + aAAVE balances on Ethereum Mainnet, validated on the voting network with storage proofs votes | yes | C-AAVE-DOCS |

### Parameter notes

- **level1_quorum_aave**: At least 320,000 must participate AND the winning option must receive at least 320,000 votes.
- **level1_vote_differential_aave**: ARFC framework: YAE votes must exceed the second-largest option (NAY or ABSTAIN) by at least 80,000.
- **level1_voting_delay_days**: Short Executor (Level 1): 1-day voting delay, 3-day voting period, 1-day timelock, 7-day grace period.
- **level2_proposition_power_aave**: 2022 Level 2 update: 320,000 AAVE proposition delegation required to create the proposal, and it had to be maintained for the 17-day vote + queue period or anyone could cancel it.
- **level2_quorum**: NOT STATED in the current official docs ('higher quorum and vote differential' only). V2 planned configuration: quorum 20%, vote differential 15%, proposition threshold 2% (secondary source C-AAVE-V2-CONFIG). The 2022 Level 2 update needed about 900,000 AAVE to pass (C-AAVE-L2RFC).
- **level2_voting_period_days**: Long Executor (Level 2): 10-day voting period, 7-day timelock, higher quorum and vote differential.
- **onchain_creation_threshold**: NOT STATED in the current official docs: the on-chain proposal-creation threshold is described only as 'sufficient proposal power'. The V2 planned configuration was 0.5% (Short Executor) / 2% (Long Executor) of supply (secondary source C-AAVE-V2-CONFIG).
- **snapshot_threshold_aave**: If the 320,000 AAVE threshold is met, the proposal proceeds to the AIP stage; if not, it fails. A quorum failure may reopen the Snapshot vote once.

## Per-check verdicts

| Check | Control | Verdict |
|-------|---------|---------|
| A1-1 | Proposal threshold exists and is public | partial |
| A1-2 | Proposer must maintain delegated power through voting | pass |
| A1-3 | Permissionless / autonomous proposal path | partial |
| A1-4 | Actions per proposal bounded | pass |
| A2-1 | Voting delay (review period) >= 1 day | pass |
| A2-2 | Voting period >= 3 days | pass |
| A2-3 | Quorum defined as explicit for-votes threshold | pass |
| A2-4 | Vote-differential / anti-close-call rule | pass |
| A2-5 | Voting period consistent across primary sources | pass |
| A3-1 | Timelock delay >= 1 day | pass |
| A3-2 | Grace period defined | pass |
| A3-3 | Timelock admin is the governor | pass |
| A3-4 | Execution is permissionless after delay | pass |
| A4-1 | Treasury moves only via timelocked governance | pass |
| A4-2 | No observed treasury transfer outside DAO recall | pass |
| A4-3 | Standing bounds / whitelists on treasury operations | pass |
| A5-1 | Emergency pause / cancel power exists and is documented | pass |
| A5-2 | Emergency powers are limited | pass |
| A5-3 | Guardian composition is public | pass |
| A6-1 | All lifecycle parameters published in official docs | partial |
| A6-2 | Governance contracts verified with published addresses | partial |
| A6-3 | Executed proposal record publicly accessible | pass |
| A6-4 | No unresolved parameter discrepancy across primary sources | pass |

## Findings (this protocol)

### F-02 — Medium — A1-1 Proposal threshold exists and is public

Observed: Snapshot author gate (80,000 AAVE) is public; the on-chain creation threshold is not stated in the current docs.

Expected: Exact threshold stated in official docs and readable on-chain

Evidence: C-AAVE-ARFC, C-AAVE-DOCS, C-AAVE-L2RFC

### F-03 — Medium — A6-1 All lifecycle parameters published in official docs

Observed: Level 2 quorum and vote-differential exact values are not stated in the current docs.

Expected: Every parameter (threshold, quorum, delay, period, timelock, grace) stated

Evidence: C-AAVE-ARFC, C-AAVE-DOCS, C-AAVE-L2RFC

### F-10 — Low — A1-3 Permissionless / autonomous proposal path

Observed: No built-in autonomous-proposal path; a one-off autonomous contract was built for the 2022 Level 2 update.

Expected: Any address can lock a small amount to create an autonomous proposal, or equivalent

Evidence: C-AAVE-ARFC, C-AAVE-DOCS, C-AAVE-L2RFC

### F-11 — Low — A6-2 Governance contracts verified with published addresses

Observed: Governance contract addresses are linked from the docs but were not verified from a primary source at audit time.

Expected: Contract addresses published in official reference and verifiable

Evidence: C-AAVE-ARFC, C-AAVE-DOCS, C-AAVE-L2RFC

## Executed proposal (evidence)

- ID: Level 2 requirements update (2022)
- Title: Adjust Level 2 requirements (long-executor)
- Date: 2022-09 / proposals created 2022-10-04
- Outcome: Approved on Snapshot with 325,000 AAVE votes; implemented via on-chain proposals created through an Autonomous Proposal contract
- Votes for: 325000
- Votes against: None
- Note: The update replaced the Level 2 Executor and the AAVE ecosystem reserve implementation. Creation used an Autonomous Proposal smart contract (0x6E1A6728829BC0FcA82C1A39834c6212C250F1c1) that accumulated 320,000 AAVE proposition power. About 900,000 AAVE were required to pass the Level 2 proposal.
- Sources: C-AAVE-L2RFC

## Method

Scored by audit-engine/audit.py from framework/rubric.json and this protocol's profile. Every parameter value cites a primary source; unverified values are recorded as such and scored partial or fail, never invented. See citations.md for the source table.
