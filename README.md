# ContextPass: NonTransitiveContextAdmissionV1

**Phase 1 deterministic core — NOT DEPLOYABLE.** The semantic consensus entry
always raises `CONSENSUS_NOT_IMPLEMENTED`. No production admission can be
approved or denied until the separately authorized Phase 2 implementation.

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
- D01–D24 Direct Mode acceptance tests; test doubles exist only in test files.

**Not implemented:** real Leader/Validator evaluation, frontend, deployment,
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
.venv/bin/python -m pytest tests/direct -q
.venv/bin/genvm-lint check contracts/context_bound_attestation.py --json
PATH="$PWD/.venv/bin:$PATH" .venv/bin/genvm-lint typecheck contracts/context_bound_attestation.py --json
```

The preparation script only copies the downloaded official SDK artifact into
the Direct Mode cache after verifying its digest. It does not deploy, connect
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
| `apply_and_join(space_id, root_attestation_id)` | All deterministic prechecks; Phase 1 stops at unimplemented consensus |
| `post_room_note(space_id, text)` | Active membership checked inside contract immediately before append |

Reads: `get_space`, `get_attestation`, `get_decision`, `is_active_member`,
`get_room_notes(space_id, offset, limit)`, `get_counts`. Unknown positive IDs
return explicit not-found/empty status or false. Invalid IDs and pagination
reject. See [SPEC.md](SPEC.md) for exact read shapes and limits.

## Review material

- [Frozen architecture](architecture-freeze-v1/02_ARCHITECTURE_FREEZE_V1.md)
- [Canonical consensus specification — not executed in Phase 1](architecture-freeze-v1/03_CANONICAL_CONSENSUS_PROMPT.md)
- [TESTING.md](TESTING.md): D01–D24 mapping, test isolation and type-check limitation
- [CONSENSUS.md](CONSENSUS.md): fail-closed Phase 1 boundary
- [PROJECT_CHECKPOINT.md](PROJECT_CHECKPOINT.md): actual status and recovery instructions
- [PHASE_0_ENVIRONMENT_REPORT.md](PHASE_0_ENVIRONMENT_REPORT.md): original environment evidence
- [PHASE_1_IMPLEMENTATION_REPORT.md](PHASE_1_IMPLEMENTATION_REPORT.md): actual execution results

Network reserved for later authorized stages: **Stable Studionet only**,
chain ID **61999**, RPC `https://studio.genlayer.com/api`, explorer
`https://explorer-studio.genlayer.com/`. No key/seed is needed for these tests.
**Do not deploy this Phase 1 draft. Do not enter Phase 2 without user approval.**

