# Scoring Rubric — Multi-Protocol Governance Audit Framework

Version 1.0.0. Machine-readable form: `framework/rubric.json`.
Area score = mean of its checks (pass = 1.0, partial = 0.5, fail = 0.0),
scaled to 0–100. Protocol score = weighted sum of area scores (weights below).

## A1 — Proposal lifecycle & access (weight 15)

| Check | Control | Pass | Partial | Fail | Fail sev. | Partial sev. |
|-------|---------|------|---------|------|-----------|--------------|
| A1-1 | Proposal threshold exists and is public | Exact threshold stated in official docs and readable on-chain | Threshold stated only for the off-chain (Snapshot) stage, or on-chain threshold not stated | No threshold stated anywhere | High | Medium |
| A1-2 | Proposer must maintain delegated power through voting | Contract cancels the proposal if the proposer falls below threshold | Rule stated in docs but not confirmed on-chain | No maintenance rule | Medium | Low |
| A1-3 | Permissionless / autonomous proposal path | Any address can lock a small amount to create an autonomous proposal, or equivalent | One-off autonomous contract used historically; no built-in path | No autonomous path and threshold is the only gate | Low | Low |
| A1-4 | Actions per proposal bounded | Explicit max actions per proposal (e.g. 10) | Bound exists via executor/payload limits, not a stated max | Unbounded actions per proposal | Medium | Low |

## A2 — Voting & quorum rules (weight 20)

| Check | Control | Pass | Partial | Fail | Fail sev. | Partial sev. |
|-------|---------|------|---------|------|-----------|--------------|
| A2-1 | Voting delay (review period) >= 1 day | Delay >= 1 day, stated in docs | Delay stated but < 1 day | No delay | Medium | Low |
| A2-2 | Voting period >= 3 days | Period >= 3 days, stated in docs | Period stated but < 3 days | No period stated | Medium | Low |
| A2-3 | Quorum defined as explicit for-votes threshold | Exact for-votes quorum in docs | Quorum defined as % of supply only, no absolute number | No quorum definition | High | Medium |
| A2-4 | Vote-differential / anti-close-call rule | Winning option must exceed the runner-up by a stated margin | Majority + quorum only, no differential | No majority rule at all | Medium | Medium |
| A2-5 | Voting period consistent across primary sources | All primary sources agree | — | Two primary sources state different values | Medium | Low |

## A3 — Timelock & execution (weight 20)

| Check | Control | Pass | Partial | Fail | Fail sev. | Partial sev. |
|-------|---------|------|---------|------|-----------|--------------|
| A3-1 | Timelock delay >= 1 day | Delay >= 1 day, stated in docs | Delay stated but < 1 day | No timelock | High | Medium |
| A3-2 | Grace period defined | Expiry window stated in docs | Inferred from shared contract codebase, not separately verified | No grace period | Medium | Low |
| A3-3 | Timelock admin is the governor | Admin is the Governor contract, stated in docs | Admin is a multisig with a documented path to governance | Admin is an EOA or unknown | High | Medium |
| A3-4 | Execution is permissionless after delay | Any address can execute after delay | Execution restricted to proposer or guardian | Execution restricted to an admin | Low | Low |

## A4 — Treasury execution (weight 15)

| Check | Control | Pass | Partial | Fail | Fail sev. | Partial sev. |
|-------|---------|------|---------|------|-----------|--------------|
| A4-1 | Treasury moves only via timelocked governance | Treasury controlled only through the timelock | Treasury partly controlled by a steward with bounds | Treasury movable without a vote | High | Medium |
| A4-2 | No observed treasury transfer outside DAO recall | No executed proposal moved funds to an address the DAO cannot recall | — | An executed proposal moved funds to an address outside DAO recall | High | Medium |
| A4-3 | Standing bounds / whitelists on treasury operations | Explicit per-operation bounds or whitelists | Bounds exist only per-proposal (each transfer needs its own vote) | No bounds of any kind | Medium | Low |

## A5 — Emergency powers & guardians (weight 15)

| Check | Control | Pass | Partial | Fail | Fail sev. | Partial sev. |
|-------|---------|------|---------|------|-----------|--------------|
| A5-1 | Emergency pause / cancel power exists and is documented | Pause and/or cancel power documented | Only one of pause/cancel documented | No emergency power documented | Medium | Low |
| A5-2 | Emergency powers are limited | Documented limits: cannot seize funds, cannot unpause, cannot upgrade | Some limits documented; other powers (e.g. pause) not verified | Unlimited emergency power | High | Medium |
| A5-3 | Guardian composition is public | Multisig threshold and signers published | Guardian is a named multisig but signers not published | Guardian holder not verifiable from any primary source | Medium | Low |

## A6 — Transparency & verifiability (weight 15)

| Check | Control | Pass | Partial | Fail | Fail sev. | Partial sev. |
|-------|---------|------|---------|------|-----------|--------------|
| A6-1 | All lifecycle parameters published in official docs | Every parameter (threshold, quorum, delay, period, timelock, grace) stated | One or more core parameters not stated in current docs | Parameters not published | Medium | Medium |
| A6-2 | Governance contracts verified with published addresses | Contract addresses published in official reference and verifiable | Addresses published but not verified at audit time, or vice versa | No addresses published | Medium | Low |
| A6-3 | Executed proposal record publicly accessible | At least one executed proposal with ID, outcome, and link | Proposal record exists but outcome or link incomplete | No executed proposal on record | Medium | Low |
| A6-4 | No unresolved parameter discrepancy across primary sources | All primary sources agree on all parameters | — | A parameter differs between primary sources | Medium | Low |
