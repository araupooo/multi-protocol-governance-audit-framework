# Claims — Claim-to-Evidence Index

Every numbered claim maps to the evidence file, the script, and the output
line that proves it. Evidence references are pack-relative paths; a `:N`
suffix is a line number inside that file.

## Protocol parameters

### C-01 — Compound proposal threshold is 25,000 COMP delegated
Statement: Addresses delegated at least 25,000 COMP can create a Compound governance proposal; any address can lock 100 COMP for an Autonomous Proposal that becomes a proposal after 25,000 COMP is delegated.
Evidence: protocols/compound.json, citations.md

### C-02 — Compound quorum is 400,000 COMP for-votes plus a majority
Statement: A Compound proposal passes only if a majority votes for it AND at least 400,000 COMP (4% of the 10M supply) is cast for it; only for-votes count toward quorum.
Evidence: protocols/compound.json, citations.md

### C-03 — Compound lifecycle is 2-day review, 3-day vote, 2-day timelock, 14-day grace
Statement: Compound proposals enter a 2-day review period (13,140 blocks), then a 3-day voting period; passing proposals are queued in the Timelock and can be implemented 2 days later, within a 14-day grace period.
Evidence: protocols/compound.json, citations.md

### C-04 — Compound Proposal 289 passed narrowly and moved 499,000 COMP
Statement: Proposal 289 passed on 2024-07-28 with 682,191 for vs 633,636 against (51.9%), moving 499,000 COMP (about $24-25M) from the treasury to a group-controlled goldCOMP treasury the DAO could not recall; the proposers agreed to rescind it on 2024-07-30.
Evidence: protocols/compound.json, citations.md, findings.md

### C-05 — Uniswap proposal threshold is 1M UNI today (2.5M originally)
Statement: The current Uniswap process (Jan 2023 update) requires at least 1M UNI delegated to submit an on-chain proposal; the original process required 2.5M UNI (0.25% of supply).
Evidence: protocols/uniswap.json, citations.md

### C-06 — Uniswap quorum is 40M UNI for-votes
Statement: A Uniswap proposal passes only with at least 40M UNI (4% of the 1B supply) voting for it; only for-votes count toward quorum.
Evidence: protocols/uniswap.json, citations.md

### C-07 — Uniswap voting period is stated as both 6 and 7 days in one primary source
Statement: The Jan 2023 Community Governance Process Update states a "6 day voting period" in its Phase 3 timeframe line and "a seven day voting period begins" in its body text — an unresolved discrepancy inside a single primary source.
Evidence: protocols/uniswap.json, citations.md, findings.md

### C-08 — Uniswap governance contracts are Timelock 0x1a9C…35BC and GovernorBravo 0x408E…24C3
Statement: The official Uniswap technical reference lists Timelock 0x1a9C8182C09F50C8318d769245beA52c32BE35BC and GovernorBravo 0x408ED6354d4973f66138C91495F2f2FCbd8724C3 as the active Ethereum mainnet governance contracts.
Evidence: protocols/uniswap.json, citations.md

### C-09 — Uniswap UNIfication proposal passed 125,342,017 for vs 742 against
Statement: The UNIfication proposal was put on-chain 2025-12-18, voted 2025-12-19 to 2025-12-25, and passed with 125,342,017 UNI for vs 742 against (above the 40M quorum); it activates the protocol fee switch and a one-time burn of 100M UNI after the 2-day timelock.
Evidence: protocols/uniswap.json, citations.md

### C-10 — Aave Level 1 is 1-day delay, 3-day vote, 1-day timelock, 7-day grace
Statement: Aave Governance V3 Short Executor (Level 1) proposals run a 1-day voting delay, a 3-day voting period, a 1-day timelock, and a 7-day grace period.
Evidence: protocols/aave.json, citations.md

### C-11 — Aave quorum is 320,000 votes and the differential is 80,000
Statement: An Aave proposal succeeds only if at least 320,000 AAVE/stkAAVE/aAAVE participate AND the winning option receives at least 320,000 votes; per the ARFC framework, YAE votes must exceed the second-largest option by at least 80,000.
Evidence: protocols/aave.json, citations.md

### C-12 — Aave Level 2 is a 10-day vote and 7-day timelock with unstated exact quorum
Statement: Aave Long Executor (Level 2) proposals run a 10-day voting period and a 7-day timelock with a higher quorum and vote differential, but the current official docs do not state the exact quorum or differential values.
Evidence: protocols/aave.json, citations.md, findings.md

### C-13 — Aave has a 4-of-7 Protocol Emergency Guardian and a 5-of-9 Governance Emergency Guardian
Statement: The Protocol Emergency Guardian is a 4-of-7 multisig (signers published in the docs) that can pause markets; the Governance Emergency Guardian is a 5-of-9 multisig (signers published) that can cancel malicious or erroneous proposals.
Evidence: protocols/aave.json, citations.md

### C-14 — Aave Level 2 update was approved on Snapshot with 325,000 AAVE
Statement: The 2022 Level 2 requirements update was approved on Snapshot with 325,000 AAVE votes and implemented via on-chain proposals created 2022-10-04 through an Autonomous Proposal contract requiring 320,000 AAVE proposition delegation.
Evidence: protocols/aave.json, citations.md

## Engine results

### C-15 — Engine scores are Aave 92.50, Compound 86.13, Uniswap 75.88
Statement: The audit engine scores Aave 92.50, Compound 86.13, and Uniswap 75.88 out of 100 across the six weighted control areas.
Evidence: outputs/run1/run.log:2, outputs/run1/run.log:3, outputs/run1/run.log:4, outputs/run1/aave.score.json, outputs/run1/compound.score.json, outputs/run1/uniswap.score.json

### C-16 — The engine emits 17 findings: 1 High, 8 Medium, 8 Low
Statement: Across the three audits the engine emits 17 findings — 1 High (Compound F-01), 8 Medium, 8 Low — each tied to a rubric check outcome.
Evidence: outputs/run1/run.log:5, outputs/run1/findings.json, findings.md

### C-17 — A clean re-run from a fresh copy is byte-identical
Statement: Running `bash scripts/clean_reproduce.sh` re-runs the audit from a fresh copy of the pack into outputs/run2-clean and reports MATCH — outputs/run1 and outputs/run2-clean are byte-identical.
Evidence: scripts/clean_reproduce.sh, outputs/run1/run.log

### C-18 — Digest verification reports all OK
Statement: Running `bash scripts/verify_digests.sh` checks SHA256SUMS over every static pack file and reports all OK.
Evidence: scripts/verify_digests.sh, SHA256SUMS
