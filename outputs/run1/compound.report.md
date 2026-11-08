# Audit Report — Compound

Governance system: Governor Bravo + Timelock. Chain: Ethereum Mainnet.
Governance token: COMP.

**Overall score: 86.13 / 100**

## Scores by control area

| Area | Control area | Weight | Score / 100 |
|------|--------------|--------|-------------|
| A1 | Proposal lifecycle & access | 15 | 100.00 |
| A2 | Voting & quorum rules | 20 | 90.00 |
| A3 | Timelock & execution | 20 | 100.00 |
| A4 | Treasury execution | 15 | 50.00 |
| A5 | Emergency powers & guardians | 15 | 83.33 |
| A6 | Transparency & verifiability | 15 | 87.50 |

## Verified parameters

| Parameter | Value | Verified | Sources |
|-----------|-------|----------|---------|
| autonomous_proposal_lock_comp | 100 COMP | yes | C-COMP-DOCS |
| execution | any address may call execute() after the timelock delay call | yes | C-COMP-DOCS |
| governor_bravo_address | (not stated / not present) address | no | C-COMP-DOCS |
| grace_period_days | 14 days | yes | C-COMP-DOCS |
| majority_rule | for > against votes | yes | C-COMP-DOCS |
| max_actions_per_proposal | 10 actions | yes | C-COMP-DOCS |
| proposal_threshold_comp | 25000 COMP delegated | yes | C-COMP-DOCS |
| quorum_for_votes_comp | 400000 COMP for-votes | yes | C-COMP-DOCS |
| review_period_days | 2 days | yes | C-COMP-DOCS, C-COMP-P8 |
| timelock_admin | Governor Bravo contract | yes | C-COMP-DOCS |
| timelock_delay_days | 2 days | yes | C-COMP-DOCS |
| vote_differential | (not stated / not present) votes | no | C-COMP-DOCS |
| voting_period_days | 3 days | yes | C-COMP-DOCS |
| voting_power | COMP delegated, snapshot at proposal start (getPriorVotes) votes | yes | C-COMP-DOCS |

### Parameter notes

- **autonomous_proposal_lock_comp**: Any address can lock 100 COMP to create an Autonomous Proposal, which becomes a governance proposal after being delegated 25,000 COMP.
- **governor_bravo_address**: NOT VERIFIED: Compound docs use a 0x123... placeholder for the Governor Bravo address; no verified mainnet address established from a primary source at audit time.
- **grace_period_days**: Docs state a 14-day grace period after the timelock delay.
- **proposal_threshold_comp**: Docs: 'Addresses delegated at least 25,000 COMP can create governance proposals'; Governor Bravo requires proposer votes > proposalThreshold.
- **quorum_for_votes_comp**: Majority of votes cast AND at least 400,000 votes for the proposal (4% of 10M supply). Only for-votes count toward quorum.
- **review_period_days**: 2-day review period; 13,140 blocks per Uniswap Proposal 8 post describing Compound's setting.
- **timelock_delay_days**: Queued in the Timelock; can be implemented 2 days later.
- **vote_differential**: NOT PRESENT: no vote-differential rule; a proposal passes on a simple majority plus the 400,000 for-votes quorum.

## Per-check verdicts

| Check | Control | Verdict |
|-------|---------|---------|
| A1-1 | Proposal threshold exists and is public | pass |
| A1-2 | Proposer must maintain delegated power through voting | pass |
| A1-3 | Permissionless / autonomous proposal path | pass |
| A1-4 | Actions per proposal bounded | pass |
| A2-1 | Voting delay (review period) >= 1 day | pass |
| A2-2 | Voting period >= 3 days | pass |
| A2-3 | Quorum defined as explicit for-votes threshold | pass |
| A2-4 | Vote-differential / anti-close-call rule | partial |
| A2-5 | Voting period consistent across primary sources | pass |
| A3-1 | Timelock delay >= 1 day | pass |
| A3-2 | Grace period defined | pass |
| A3-3 | Timelock admin is the governor | pass |
| A3-4 | Execution is permissionless after delay | pass |
| A4-1 | Treasury moves only via timelocked governance | pass |
| A4-2 | No observed treasury transfer outside DAO recall | fail |
| A4-3 | Standing bounds / whitelists on treasury operations | partial |
| A5-1 | Emergency pause / cancel power exists and is documented | pass |
| A5-2 | Emergency powers are limited | pass |
| A5-3 | Guardian composition is public | partial |
| A6-1 | All lifecycle parameters published in official docs | pass |
| A6-2 | Governance contracts verified with published addresses | partial |
| A6-3 | Executed proposal record publicly accessible | pass |
| A6-4 | No unresolved parameter discrepancy across primary sources | pass |

## Findings (this protocol)

### F-01 — High — A4-2 No observed treasury transfer outside DAO recall

Observed: Proposal 289 moved 499,000 COMP to a group-controlled treasury the DAO could not recall.

Expected: No executed proposal moved funds to an address the DAO cannot recall

Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8

### F-04 — Medium — A2-4 Vote-differential / anti-close-call rule

Observed: No differential rule: Proposal 289 passed with 682,191 for vs 633,636 against (51.9%).

Expected: Winning option must exceed the runner-up by a stated margin

Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8

### F-12 — Low — A4-3 Standing bounds / whitelists on treasury operations

Observed: Each treasury transfer needs its own vote; no standing per-operation bounds or whitelists.

Expected: Explicit per-operation bounds or whitelists

Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8

### F-13 — Low — A5-3 Guardian composition is public

Observed: Pause Guardian is a named multisig, but its signer list was not verified from a primary source.

Expected: Multisig threshold and signers published

Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8

### F-14 — Low — A6-2 Governance contracts verified with published addresses

Observed: Governor Bravo mainnet address not verified from a primary source at audit time.

Expected: Contract addresses published in official reference and verifiable

Evidence: C-COMP-289, C-COMP-289-RESCIND, C-COMP-DOCS, C-COMP-P8

## Executed proposal (evidence)

- ID: 289
- Title: goldCOMP treasury funding
- Date: 2024-07-28
- Outcome: Passed; later agreed to be rescinded (2024-07-30 agreement) in favour of a staking proposal
- Votes for: 682191
- Votes against: 633636
- Note: Narrow 51.9% majority moved 499,000 COMP (about $24-25M) from the treasury to a yield-bearing vault controlled by the 'Golden Boys' group; the DAO could not recall the funds at its own discretion (withdrawal controlled by GoldenBoyzMultisig). Proposal 290 followed, proposing transfer of the Timelock admin to a CommunityMultiSig.
- Sources: C-COMP-289, C-COMP-289-RESCIND

## Method

Scored by audit-engine/audit.py from framework/rubric.json and this protocol's profile. Every parameter value cites a primary source; unverified values are recorded as such and scored partial or fail, never invented. See citations.md for the source table.
