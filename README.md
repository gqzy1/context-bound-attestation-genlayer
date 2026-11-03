# Context-bound admission

A reusable GenLayer contract for deriving room-local posting permission from an original issuer's scoped assertion. A room owner fixes its trusted issuer and requirements. Leader and Validators independently classify full scope coverage; a two-outcome decision is bound to the room, holder and root. It cannot become a transferable credential or a new attestation.

Root revocation immediately disables protected posting while retaining public notes and historical decisions. Trust in an issuer is an explicit owner choice, not proof of identity, skill or Sybil resistance.

## Deployment and observed behavior

Stable Studionet, chain ID **61999**, RPC **https://studio.genlayer.com/api**. Canonical contract: `0xDe9abfBe2E4A61d23e27b552e241f5Bb1d1821b8`. Source SHA-256: `e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d`.

[T01–T10 evidence](ONCHAIN_EVIDENCE_INDEX.md) covers positive/negative admission, posting, revocation and subsequent rejection. T07 required one Leader rotation. T08/T10 are expected business rollbacks, not successful posts. The separate [ContextPass application](https://gqzy1.github.io/contextpass-genlayer/) recorded one production create_space write, finalized as Space #3; its other four write paths do not have separate live frontend coverage.

Last recorded offline results: contract **240/240**, frontend **145/145**. Standard checks and build passed. Seven upstream Python Strict SDK diagnostics remain; missing original PNG/raw bundles, limited wallet/mobile QA, an Overview nested-Map display issue and a bundle warning are documented in [the historical audit](PHASE_4E_SUBMISSION_AUDIT.md). No explicit LICENSE file is present.

## Local verification

Python **3.12.14**, GenVM **v0.2.16**, `genlayer-test==0.29.2`,
`genvm-linter==0.11.0`. The contract pins the exact stable SDK runner in its
first two lines. Python's `genlayer-py==0.16.3` is a client dependency, not that
contract SDK. JavaScript's `genlayer-js==1.1.8` is used by the browser client.

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
pinned cloudpickle runner for callback serialization tests. It does not deploy, connect
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


## Technical references

- [State, inputs and public methods](SPEC.md)
- [Independent classification and equivalence](CONSENSUS.md)
- [Testing scope and recorded results](TESTING.md)
- [Deployment and source binding](DEPLOYMENT_STUDIONET.md)
- [Verification index](PROJECT_CHECKPOINT.md)

Historical reports describe their dated builds; original receipts and failed cases remain available at their existing evidence paths.
