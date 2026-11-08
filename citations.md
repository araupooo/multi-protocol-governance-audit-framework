# Citations — Primary Sources

Every parameter value in `protocols/*.json` cites one of the sources below.
"Primary" means the protocol's own documentation, governance forum, or
official contract reference. "Secondary" means an independent write-up that
quotes or reads the primary source; secondary sources are flagged as such in
the profiles and never used alone for a scored parameter, except where noted.

## Compound

### C-COMP-DOCS — Compound Governance documentation
URL: https://stage.compound.finance/docs/governance
Establishes: proposal threshold 25,000 COMP delegated; Autonomous Proposal
(lock 100 COMP, becomes a proposal after 25,000 COMP delegated); 2-day review
period; 3-day voting period; quorum of a majority plus at least 400,000
for-votes; 2-day timelock delay; 14-day grace period; max 10 actions per
proposal; Governor Bravo as governance module; Timelock admin held by Governor
Bravo; Pause Guardian role. Retrieved via search-result excerpts of the
official docs page; a direct fetch failed at audit time.

### C-COMP-P8 — Uniswap Governance Proposal 8 (Governor Bravo upgrade)
URL: https://gov.uniswap.org/t/governance-proposal-8-upgrade-governance-contract-to-compounds-governor-bravo/13835
Establishes: Compound uses a 13,140-block (~2-day) review period; the review
period delays the voting-power snapshot so holders can move and analyse
before voting begins. Retrieved via search-result excerpts of the forum post.

### C-COMP-289 — Proposal 289 governance-attack coverage
URL: https://beincrypto.com/compound-finance-proposal-289-governance-attack-claims/
Establishes: Proposal 289 passed 2024-07-28 with 682,191 for vs 633,636
against, moving 499,000 COMP (about $24–25M) from the treasury to a
yield-bearing vault controlled by the "Golden Boys" group; withdrawal
controlled by GoldenBoyzMultisig, so the DAO could not recall the funds at
its own discretion; Proposal 290 followed, proposing transfer of the Timelock
admin to a CommunityMultiSig. Retrieved via search-result excerpts.

### C-COMP-289-RESCIND — "Golden Boys" agree to rescind Proposal 289
URL: https://cointelegraph.com/news/golden-boys-behind-compound-governance-attack-agree-to-rescind-proposal
Establishes: on 2024-07-30 the Golden Boys agreed to rescind Proposal 289 in
favour of a new staking proposal (30% of market reserves to COMP stakers).
Retrieved via search-result excerpts.

### C-BRAVO-WINTERMUTE — Understanding Governor Bravo (Wintermute research)
URL: https://www.wintermute.com/insights/research/defi-research/understanding-governor-bravo-a-key-tool-for-on-chain-enforceability
Establishes: Governor Bravo's three functions (creation, voting, execution);
Compound's Pause Guardian is a community-elected multisig used during
unforeseen vulnerabilities; a typical Compound proposal takes up to 7 days.
Secondary source. Retrieved via search-result excerpts.

## Uniswap

### C-UNI-PROC-2023 — Community Governance Process Update [Jan 2023]
URL: https://gov.uniswap.org/t/community-governance-process-update-jan-2023/19976
Establishes: current process — Phase 3 on-chain proposal: 1M UNI proposing
threshold, 40M UNI quorum, 2-day waiting period, 2-day timelock; Temperature
Check 5 days with at least 10M UNI for; RFC minimum 7 days. Contains the
6-vs-7-day discrepancy: the Phase 3 timeframe line states a "6 day voting
period" while the body text states "a seven day voting period begins".
Retrieved via search-result excerpts of the forum post.

### C-UNI-PROC-ORIG — Proposed Revisions to the Uniswap Governance Process
URL: https://gov.uniswap.org/t/proposed-revisions-to-the-uniswap-governance-process/15906
Establishes: original process — 2.5M UNI delegated to submit, 40M UNI
yes-votes to pass, 2-day pending period, 7-day voting period, 2-day timelock.
Retrieved via search-result excerpts of the forum post.

### C-UNI-PROCESS-MIRROR — Uniswap Governance Process (docs mirror)
URL: https://docs.etcswap.org/concepts/governance/process
Establishes: max 10 actions per proposal; proposer must maintain vote weight
throughout voting or the proposal may be canceled by anyone; 2-day voting
delay, 7-day voting period, 2-day timelock; quorum 4% of UNI (40M) in the
affirmative. Secondary source (mirror of the Uniswap process docs).
Retrieved via search-result excerpts.

### C-UNI-TECHREF — Uniswap Technical Reference (official)
URL: https://developers.uniswap.org/docs/ecosystem/governance/technical-reference
Establishes: active mainnet governance contracts — Timelock
0x1a9C8182C09F50C8318d769245beA52c32BE35BC and GovernorBravo
0x408ED6354d4973f66138C91495F2f2FCbd8724C3; Governor Alpha contracts were
deprecated in 2021 via governance vote following the upgrade to Governor
Bravo. Retrieved via search-result excerpts.

### C-UNI-CONTRACT-READS — "How a DAO Vote Becomes a Treasury Transfer"
URL: https://cryptonews.net/news/altcoins/33648177/
Establishes (secondary, Oct 2026 contract reads): Uniswap Governor threshold
1M UNI, voting delay 13,140 blocks, voting period 40,320 blocks; timelock
admin is Governor Bravo with a 172,800-second (2-day) delay; Proposal 83
queued 2025-03-19 and executed 2025-03-21, transferring 20.32M UNI from the
treasury timelock. Retrieved via search-result excerpts.

### C-UNI-UNIF — UNIfication proposal
URL: https://gov.uniswap.org/t/unification-proposal/25881
Establishes: UNIfication proposal put on-chain 2025-12-18, voting
2025-12-19 to 2025-12-25, passed with 125,342,017 UNI for vs 742 against
(above the 40M quorum); activates the protocol fee switch and a one-time burn
of 100M UNI from the treasury after the 2-day timelock, plus a 20M UNI/year
growth budget. Retrieved via search-result excerpts of the forum post.

## Aave

### C-AAVE-DOCS — Aave Governance documentation
URL: https://aave.com/docs/ecosystem/governance
Establishes: Governance V3 structure (Core Network Ethereum Mainnet; voting
networks Polygon, Avalanche, Ethereum backup); Short Executor (Level 1):
1-day voting delay, 3-day voting period, 1-day timelock, 7-day grace period;
success requires at least 320,000 AAVE/stkAAVE/aAAVE participating and the
winning option receiving at least 320,000 votes; Long Executor (Level 2):
10-day voting period, 7-day timelock, higher quorum and vote differential;
Snapshot author gate (approved list or at least 80,000 AAVE proposition
power), 1-day delay, 3-day vote, 320,000 AAVE threshold, one reopen on quorum
failure; voting power is AAVE + stkAAVE + aAAVE validated by storage proofs;
payload registration, activation, voting, closure, queuing, and execution
flow; Protocol Emergency Guardian (4-of-7 multisig, signers published) and
Governance Emergency Guardian (5-of-9 multisig, signers published); GHO,
Risk, Freezing, and Finance Stewards and their bounds; Finance Committee
2-of-3 multisig 0x22740deBa78d5a0c24C58C740e3715ec29de1bFa. Fetched directly
2026-11-08 19:35 UTC.

### C-AAVE-ARFC — Updated Framework for ARFC and TEMP CHECK Proposals
URL: https://governance.aave.com/t/arfc-addendum-updated-framework-for-arfc-and-temp-check-proposals/18642
Establishes: ARFC voting guidelines — quorum 320,000 YAE votes; differential:
YAE votes must exceed the second-largest option (NAY or ABSTAIN) by at least
80,000; Snapshot vote starts 24h after publication; proposal thread at least
5 days old before voting. Retrieved via search-result excerpts.

### C-AAVE-L2RFC — Adjust Level 2 requirements (long-executor)
URL: https://governance.aave.com/t/rfc-aave-governance-adjust-level-2-requirements-long-executor/8693/6
Establishes: the 2022 Level 2 update was approved on Snapshot with 325,000
AAVE votes; implementation via on-chain proposals created 2022-10-04 through
an Autonomous Proposal contract (0x6E1A6728829BC0FcA82C1A39834c6212C250F1c1)
requiring 320,000 AAVE proposition delegation, maintained for the 17-day vote
+ queue period (dropping below opens cancellation by anyone); about 900,000
AAVE required to pass the Level 2 proposal. Retrieved via search-result
excerpts.

### C-AAVE-V2-CONFIG — Aave Governance V2 planned configuration
URL: https://socket.dev/npm/package/@aave/governance-v2
Establishes (secondary): planned V2 mainnet configuration — Short Executor:
proposition threshold 0.5%, vote differential 0.5%, quorum 2%; Long
Executor: proposition threshold 2%, voting duration 10 days, vote
differential 15%, quorum 20%. Used only to note what the V2 configuration
was; V3 exact Level 2 values are recorded as not stated in the current docs.
Retrieved via search-result excerpts.
