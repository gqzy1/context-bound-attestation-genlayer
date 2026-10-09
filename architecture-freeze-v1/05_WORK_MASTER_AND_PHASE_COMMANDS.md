# Work Master Plan and Copy-Ready Phase Commands

## Objective / economy
Build one original reusable GenLayer Intelligent Contract + one complete app with the exact same contract. Keep **one** nondeterministic semantic evaluation call per admission, use Direct Mode for rapid tests, and perform minimal manually signed real Studionet writes. Limit desired Work consumption to ~2–4 five-hour quota windows as a non-guaranteed *planning target*. Stop at each phase checkpoint to avoid unattended redesign and quota waste.

## Repo ownership and intended paths (NOT CREATED)
- **A:** `gqzy1/context-bound-attestation-genlayer`
- **B:** `gqzy1/contextpass-genlayer`
- Both under the **gqzy1 connector account**; never use `halihalibt` or previously built repo as a source/template of project mechanism. Official generic tooling/examples may be consulted for SDK syntax only, with original implementation.

Proposed repository A structure:
- `contracts/context_bound_attestation.py` (authoritative canonical source)
- `tests/direct/*`, `tests/consensus/*`
- `README.md`, `SPEC.md`, `CONSENSUS.md`, `TESTING.md`, `DEPLOYMENT_STUDIONET.md`, `PROJECT_CHECKPOINT.md`

Proposed repository B structure:
- `intelligent-contract/contracts/context_bound_attestation.py` (byte-identical official A source)
- `intelligent-contract/SOURCE_PROVENANCE.md`, `intelligent-contract/DEPLOYMENT_MANIFEST_STUDIONET.md`
- `src/*`, `public/*`, `tests/*`, `index.html`, `package.json`
- `README.md`, `DEMO.md`, `EVIDENCE_INDEX.md`, `SUBMISSION_PROJECTS.md`, `PROJECT_CHECKPOINT.md`

## PHASE 0 — Environment readiness ONLY, no writes to GitHub, no deployment
**Copy-ready Work message:**

> Work on ContextPass under **GitHub account gqzy1**. Read `00_READ_FIRST.md`, `01_DUPLICATION_AND_GATE.md`, `02_ARCHITECTURE_FREEZE_V1.md`, `03_CANONICAL_CONSENSUS_PROMPT.md`, `04_TEST_ACCEPTANCE_PLAN.md` in full. Execute **PHASE 0 only**: verify current stable Studionet (61999, https://studio.genlayer.com/api), usable stable GenVM/GenLayer Python SDK, genlayer-test Direct Mode, genlayer-js with studionet wallet read/write APIs, GitHub authorization for gqzy1, and zero additional paid dependency. Produce `PHASE_0_ENVIRONMENT_REPORT.md` with exact installed versions, references, blockers, and a pass/fail matrix. Use read-only public network checks if useful. Do not create or change repos, do not write contract/frontend code, do not deploy or send transactions, do not ask for private keys or seeds, do not enter next phase. STOP and await approval.

**Phase 0 PASS:** stable compatible version set and docs identified, Direct Mode available, gqzy1 identifiable, no need for paid services/new network. Pin the specific stable versions discovered; NEVER assume old project versions apply.

## PHASE 1 — Repository A skeleton + deterministic core ONLY
**Copy-ready Work message:**

> Phase 0 passed and is authoritative. Operate only on `gqzy1/context-bound-attestation-genlayer` after verifying account identity and checking that user has authorized repository creation. Implement only the frozen deterministic state, public methods except semantic call, access control, source/decision references, active member gate and protected room notes; use SDK-compatible state containers. Add Direct Mode tests for D01–D24. No nondet LLM or frontend, no real network calls/transactions. Run lint/tests, provide coverage and a draft PR if authorized. Update `PROJECT_CHECKPOINT.md`, STOP after Phase 1.

**PASS:** no scope changes, no security bypass, all deterministic D-tests pass.

## PHASE 2 — Actual independent Leader/Validator consensus ONLY
**Copy-ready Work message:**

> Continue frozen ContextPass in Repository A, Phase 2 only. Implement the exact `03_CANONICAL_CONSENSUS_PROMPT.md` with one custom `run_nondet_unsafe` block on `apply_and_join`. Leader and Validator must each independently classify original on-chain scope against immutable room requirement. Compare exact decision enum deterministically, NEVER only check leader JSON shape; malformed/conflicting output fails safely. Never write contract state inside nondet block. Run N01–N10 and D regression tests with mocked LLM using Direct Mode, lint, report passing counts, update checkpoint and open draft PR if authorized. No real deployment, network tx or frontend. STOP.

**PASS:** actual independent validator execution demonstrated, conservative failure behavior, deterministic post-consensus state transition.

## PHASE 3 — Repository B complete minimal frontend ONLY
**Copy-ready Work message:**

> Continue locked ContextPass, Phase 3 only. Use account gqzy1 and establish Repository B once authorized. Build React+Vite+TypeScript+genlayer-js+plain CSS GitHub Pages site. Four simple panels: public verified demo/overview, rooms, root attestations, admission and room notes. All writes are real SDK contract calls, but DO NOT send any network transaction in this phase. Implement read-only simulation/mocks for tests, real wallet connectors, 61999 chain guard, tx pending/finality/readback, readable errors, 429 backoff/single flight, read-only observer mode. Copy A canonical source byte-for-byte into B and verify SHA256. Run frontend tests F* where possible and production build. No protocol/contract modifications; any mismatch STOP. Update checkpoint, draft PR if authorized. STOP.

**PASS:** static build/test pass, no fake confirmed transactions, canonical source identical, no backend needed.

## PHASE 4 — Pre-deployment manual Studio package, then signed real E2E by USER
**Copy-ready Work message:**

> Continue ContextPass Phase 4 pre-deployment preparation ONLY. Re-run all A/B tests and build. Generate exact Studio execution guide using pinned stable SDK: source file path, constructor args, wallet A/B roles, exact string inputs for two rooms and one root, method argument values, required receipts, tx IDs, explorer links, consensus/finality fields and expected readback. Do not generate or request private keys. Do not send transactions, deploy, or navigate a signing action. STOP and wait for user to manually run in Stable Studionet and supply real receipts.

**After user supplies receipts (separate approval):**

> Verify submitted actual Studionet contract and transactions read-only. Reconcile T01–T10 evidence with state and frontend. Fix only demonstrated UI/documentation/integration errors (no protocol redesign) with regression tests, draft PRs, update checkpoint. STOP before Portal submission.

## PHASE 5 — Submission QA, not submission
**Copy-ready Work message:**

> Read final ContextPass A/B main and recorded on-chain E2E. Verify both public repos, canonical hash match, chain ID/address/tx receipts, stable website, independent A reviewer instructions, B hands-on user flow, accurate evidence index and no misleading claims. Prepare two independent Portal submission packets, suggested tags only if actually present, screenshots and exact public links; flag duplicates/risks. No Portal submission, no write transaction. Update checkpoint. STOP.

## Global execution constraints
1. NEVER combine phases without specific new authorization. No auto next-phase.
2. Before any write, verify selected GitHub link/account is `gqzy1`. Do not touch `halihalibt`.
3. No private key/seed handling; do not store or output credentials.
4. Freeze protocol semantic decisions. Change only syntax compatibility with evidence of necessity. Hard blocker = STOP and report.
5. No 'tests pass' without command evidence. No 'consensus finalized' until verified explorer state/receipt.
6. Prefer one PR per phase, test-only preliminary steps, no aggressive retry on rate-limited Studio RPC.
7. No ordinary paid API, no private local node, no other GenLayer network.
