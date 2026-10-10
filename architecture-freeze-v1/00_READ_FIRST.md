# CONTEXTPASS — WORK HANDOFF PACKAGE V1

**Status:** DESIGN FROZEN V1 (conditional implementation readiness; no code, repository, deployment, transaction, or real network tests performed).
**Freeze date:** 2026-10-10. **Owner GitHub account:** `gqzy1` ONLY.
**Tracks:** A = standalone Intelligent Contract primitive; B = complete Projects app built on A's exact canonical source.

## Read order (mandatory)
1. `01_DUPLICATION_AND_GATE.md` — what was checked, what is *not* proven, hard stops.
2. `02_ARCHITECTURE_FREEZE_V1.md` — authoritative protocol and app design; do not reinterpret.
3. `03_CANONICAL_CONSENSUS_PROMPT.md` — exact classification and Equivalence Principle.
4. `04_TEST_ACCEPTANCE_PLAN.md` — executable acceptance criteria (not execution evidence).
5. `05_WORK_MASTER_AND_PHASE_COMMANDS.md` — bounded Work stages and copy-ready instructions.
6. `06_DEPLOYMENT_EVIDENCE_SUBMISSION.md` — manually signed Studionet E2E and both submissions.
7. `07_PROJECT_CHECKPOINT_TEMPLATE.md` — stage handoff format.

## One-sentence product definition
A community workspace can grant **real on-chain write access** based on a *trusted issuer's existing scope-limited attestation* only if independent GenLayer validators agree that the attestation's wording covers all requirements of that workspace. A successful derived **admission is tied to exactly one room, wallet and root attestation**; it cannot be converted into a new attestation or transferred, and root revocation immediately disables protected writes.

## The one central trust decision
Does the **original issuer's explicitly stated endorsement scope** semantically cover **every essential requirement of the destination room** *without assuming extra abilities*? `ELIGIBLE` only if clearly yes; otherwise `NOT_ELIGIBLE`. Consensus must happen **inside the contract** (custom independently rerun Leader/Validator).

## Project classification
Primary: **Identity & Trust** (Portal label screenshot: 身份与信誉). Specific tags only after checking the actual portal options; do not invent a label.

## Locked network/cost boundaries
- **Only Stable GenLayer Studionet**, chain ID **61999**, RPC `https://studio.genlayer.com/api`, Explorer `https://explorer-studio.genlayer.com/`.
- No Bradbury, Asimov, Studio-dev, local private GenLayer node, production chain, or paid LLM API without new authorization.
- Free hosted Studio and faucet test GEN; GitHub repositories + GitHub Pages free static site. No assumption that GenLayer execution consumes zero *test* GEN. No paid infrastructure.
- Signing is manual by the user. Never request, read, write, print, store or transmit a private key/seed phrase. No write transactions until the user authorizes the deployment stage.

## Immediate next step
Work Phase 0: discover and verify stable SDK/GenVM/genlayer-test versions and `studionet` client binding against official docs and public read-only APIs. **Stop after Phase 0 report.** No repo creation, commits, deployment or transaction unless explicitly approved in a separate phase.

## Important honesty limitations
- A credential is an **issuer assertion**, not GenLayer verification of real-world skill/identity.
- Trusting an issuer is a choice made by the space creator. Sybil/collusion is **not** prevented.
- Contract-protected *posting* is genuine on-chain gating; a static GitHub Pages site cannot keep public data secret. Do not market this as confidentiality or privacy-preserving identity.
- The public duplicate scan did not identify an exact deployed GenLayer clone; it was **not an exhaustive Portal-wide audit**. Passing a design review is **not** evidence of Validator convergence or Portal acceptance.

## Change control
FROZEN: primitive semantics, role/authority, source vs derived grants, one semantic consensus entry, two-outcome conservative policy, key state invariants, single-contract architecture, independent A/B submissions, Stable Studionet only, manual signing. SDK syntax may adapt to officially supported stable API without changing semantics. Feature growth / design redesign requires explicit user approval.
