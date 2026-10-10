# ContextPass — current status (Phase 4D, 2026-10-10)

**Current authoritative project status.** Historical Phase 0–4C reports and the old README below describe their own points in time and are retained for traceability; they are **not** current claims that the product is undeployed, unpublished, or its PRs remain unmerged.

- **Intelligent Contract (Repository A):** [canonical Stable Studionet deployment](https://explorer-studio.genlayer.com/transactions/0x26282c539033879705d9a8dea18c8676dae46c0cd09df9f91cb20d740f9be994), contract `0xDe9abfBe2E4A61d23e27b552e241f5Bb1d1821b8`, Chain ID `61999`. Source SHA256 `e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d`; A/B source parity and deployed-source byte match were checked in Phase 4C. No source/protocol change in Phase 4D.
- **Product:** [live GitHub Pages demo](https://gqzy1.github.io/contextpass-genlayer/) operated by Repository B; desktop/mobile read-only smoke tests performed, desktop browser wallet connected successfully.
- **Real onchain evidence:** user-manual Studio T01–T10 plus 23/23 read-only SDK rechecks documented in [the canonical evidence index](ONCHAIN_EVIDENCE_INDEX.md); T07 first-round parse error/rotation and T08/T10 expected Rollback must not be omitted.
- **New Phase 4D live website write:** [`create_space` transaction](https://explorer-studio.genlayer.com/transactions/0x85c5037d3ac249faca70336a6760d4538dc26407181bf71d79da091e6457d02d), displayed by the real frontend as `confirmed`, `FINALIZED receipt and matching onchain readback verified`, returned Space ID `3`. This is **user screenshot evidence of frontend verification**, not an independent re-fetch of this transaction's full raw receipt. See [Phase 4D closure](PHASE_4D_CLOSURE_REPORT.md).
- **Tests:** prior A `240/240` offline PASS; prior B `145/145` offline PASS; the published Pages workflow also reported `145/145` PASS. No fresh full test rerun is claimed for this Phase 4D documentation branch. Python Strict **FAIL** with exactly seven previously recorded upstream SDK typing diagnostics, not waived or silently fixed.
- **GitHub:** earlier Phase 1/2/4B/4C PRs were user-merged into `main`. Phase 4D changes live in a separate review branch and must be merged explicitly. **Portal not submitted** by this closure.

## Review links

[Phase 4D closure](PHASE_4D_CLOSURE_REPORT.md) · [T01–T10 index](ONCHAIN_EVIDENCE_INDEX.md) · [Release readiness (historical Phase 4C checklist)](RELEASE_READINESS_CHECKLIST.md) · [Contract source](contracts/context_bound_attestation.py) · [Repository B](https://github.com/gqzy1/contextpass-genlayer)

---

## Historical README (superseded as a statement of current status)

# ContextPass — Phase 4C evidence closure

Canonical Stable Studionet61999 contract `0xDe9abfBe2E4A61d23e27b552e241f5Bb1d1821b8`, byte-identical deployed/A/B source SHA `e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d`. User manually completed T01–T10; this phase independently rechecked23read-only SDK operations, all10FINALIZED receipts and current revoked/activefalse state. No contract/source/freeze/consensus change. No chain transaction, deploy, merge or publication in this phase.

A new phase4c-evidence-closure Draft targets phase4b-address-compatibility (A_PHASE4C_DRAFT_PR_PENDING). A main remains bootstrap, not canonical. Source baseline c7c6e50620602d03ad4e3c116ad1532097feab8a. B new frontend integration Draft: B_PHASE4C_DRAFT_PR_PENDING.

[Actual evidence](ONCHAIN_EVIDENCE_INDEX.md) · [Phase4C report](PHASE_4C_INTEGRATION_REPORT.md) · [Release gate](RELEASE_READINESS_CHECKLIST.md) · [Deployment](DEPLOYMENT_STUDIONET.md). A240offline PASS, B145offline PASS, static/default/TSbuild PASS; PythonStrict original7FAIL. Real frontend wallet/browser QA NOT RUN. T07rotation1 and first-round parse error/disagree are retained; finalAccepted denial isn't a unanimity claim. Root1revoked, historicRoom1ELIGIBLE doesn't grant current access.

**STOP pending manual acceptance/further explicit release authorization.** No PR is merged, Pages not published, Portal not submitted. Earlier candidate-only documentation below is historical and superseded for deployment status by the links above.

## Historical README

# Phase 4B address compatibility candidate

This branch contains the minimum `_address` normalization fix. Patched SHA256: `e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d`. Review `PHASE_4B_ADDRESS_COMPATIBILITY_REPORT.md`. The previously reported deployment at `0x97B9003a17A8EDBD1b5E3379AA659753791497d9` uses the old source and is not patched by this PR. T02–T10 remain paused. No deployment, transaction, merge or frontend unlock was performed. Earlier phase reports below remain historical.

# ContextPass: NonTransitiveContextAdmissionV1

**Phase 2 independent custom consensus — offline verified only.** The pinned
SDK custom `run_nondet_unsafe` gate now runs complete independent Leader and
Validator classification. No real model/network consensus, deployment or
transaction has been executed; deployment remains unauthorized.

A space owner chooses one trusted original issuer and an immutable entry
requirement. An issuer creates a non-transferable root attestation for another
wallet. The planned GenLayer consensus evaluates whether that root's stated
scope covers the room's entire requirement; an admission is bound to one room,
holder and original root. Revoking the root immediately disables protected
posting, while historical notes remain public.

The issuer's text is an assertion, not verified real-world expertise or identity.
The owner chooses whom to trust. This does not prevent collusion or Sybil
identities and does not make public room content confidential.

## Implemented in this draft

- SDK-native persistent records, `TreeMap` and `DynArray`; IDs start at 1.
- Frozen five write methods and six read methods; no admin grant or edit API.
- Issuer-only irreversible revocation, holder/issuer prechecks and one decision
  ever per room/holder, including a denied decision.
- Deterministic persistence *after* the private semantic boundary and a
  revocation-aware `is_active_member` gate inside `post_room_note`.
- UTF-8 limits, control-character rejection, bounded public pagination and a
  30-note cap per space.
- D01–D24 Direct Mode regression and N01–N10 offline custom-gate tests;
  S01–S20 run with scripted agreement/disagreement, not actual model predictions.

**Not performed:** real network Leader/Validator evaluation, frontend, deployment,
live transaction evidence, Portal submissions or Repository B.

## Local verification

Python **3.12.14**, GenVM **v0.2.16**, `genlayer-test==0.29.2`,
`genvm-linter==0.11.0`. The contract pins the exact stable SDK runner in its
first two lines. Python's `genlayer-py==0.16.3` is a client dependency, not that
contract SDK. JavaScript's `genlayer-js==1.1.8` remains reserved for the later
frontend stage.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/genvm-lint download --version v0.2.16
.venv/bin/python scripts/prepare_direct_sdk.py
.venv/bin/python -m pytest tests/direct tests/consensus -q
.venv/bin/genvm-lint check contracts/context_bound_attestation.py --json
PATH="$PWD/.venv/bin:$PATH" .venv/bin/genvm-lint typecheck contracts/context_bound_attestation.py --json
```

The preparation script copies the downloaded official SDK artifact into
the Direct Mode cache after verifying its digest, then extracts the exact
Phase 0 cloudpickle runner for callback serialization tests. It does not deploy, connect
to a blockchain, invoke an LLM, or handle wallets. Tests block socket network
connections and explicitly select SDK v0.2.16. The integration pytest plugin
is disabled; only Direct Mode runs.

Windows PowerShell: create `.venv` with `py -3.12 -m venv .venv`, run tools
from `.venv\Scripts`, and add that directory to the process PATH for Pyright.
Do not substitute a different network to resolve local tooling issues.

## Public methods

| Write | Behavior |
|---|---|
| `create_space(title, required_scope, trusted_issuer)` | Sender owns immutable room; returns space ID |
| `issue_attestation(holder, label, source_scope)` | Sender is original issuer; no self-issuance; returns root ID |
| `revoke_attestation(attestation_id)` | Issuer only; repeat rejects `ALREADY_REVOKED` |
| `apply_and_join(space_id, root_attestation_id)` | Deterministic prechecks; independent custom consensus; persist only after accepted return |
| `post_room_note(space_id, text)` | Active membership checked inside contract immediately before append |

Reads: `get_space`, `get_attestation`, `get_decision`, `is_active_member`,
`get_room_notes(space_id, offset, limit)`, `get_counts`. Unknown positive IDs
return explicit not-found/empty status or false. Invalid IDs and pagination
reject. See [SPEC.md](SPEC.md) for exact read shapes and limits.

## Review material

- [Frozen architecture](architecture-freeze-v1/02_ARCHITECTURE_FREEZE_V1.md)
- [Canonical consensus specification](architecture-freeze-v1/03_CANONICAL_CONSENSUS_PROMPT.md)
- [TESTING.md](TESTING.md): D01–D24 mapping, test isolation and type-check limitation
- [CONSENSUS.md](CONSENSUS.md): independent classification and exact comparison
- [PROJECT_CHECKPOINT.md](PROJECT_CHECKPOINT.md): actual status and recovery instructions
- [PHASE_0_ENVIRONMENT_REPORT.md](PHASE_0_ENVIRONMENT_REPORT.md): original environment evidence
- [PHASE_1_IMPLEMENTATION_REPORT.md](PHASE_1_IMPLEMENTATION_REPORT.md): preserved Phase 1 results
- [PHASE_2_IMPLEMENTATION_REPORT.md](PHASE_2_IMPLEMENTATION_REPORT.md): current results, limits and Draft PR

Network reserved for later authorized stages: **Stable Studionet only**,
chain ID **61999**, RPC `https://studio.genlayer.com/api`, explorer
`https://explorer-studio.genlayer.com/`. No key/seed is needed for these tests.
**Do not deploy this offline draft. STOP pending explicit Phase 3 approval.**
