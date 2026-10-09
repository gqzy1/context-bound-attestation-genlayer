# Phase 1 verification

Direct Mode only, exact SDK v0.2.16. `pytest.ini` disables the integration
plugin (`-p no:gltest`) to avoid default localnet configuration. Tests block
socket connection APIs; SDK artifacts must be cached before running. No
integration fixtures, LLM providers, blockchain calls or signing are used.

The production consensus boundary raises `CONSENSUS_NOT_IMPLEMENTED`.
Selected tests monkeypatch only that private method, inside pytest; the
returned string is an explicit test double for an eventual accepted consensus
result. It is not AI classification and is not deployed. No production
override or decision setter exists. Scope comparisons and multi-validator
convergence remain Phase 2/4 work.

## Frozen requirement coverage

All tests below use the actual canonical source and SDK serialized state.
Parametrization expands 24 requirement IDs into multiple test cases. `D09`
and `D21` have additional functions, and supplementary tests cover serialization,
typed API shape, UTF-8 boundaries and binding corruption defenses.

| Requirement | Deterministic evidence |
|---|---|
| D01 | Monotonic IDs from 1 and sender-owned rooms |
| D02 | Empty, whitespace, UTF-8 overflow, raw controls and unchanged state |
| D03 | Issuer/holder attribution, immutable stored text, safe trim |
| D04 | Self-issuance, malformed/zero addresses, zero sender |
| D05 | Issuer-only revoke, irreversible state, repeat rejection |
| D06 | Untrusted issuer rejects before test boundary is reached |
| D07 | Other wallets reject before boundary |
| D08 | Revoked root rejects before boundary |
| D09 | Missing/invalid/boolean/overflow IDs; unchanged state |
| D10 | Exact 11-method ABI; no edit/grant API; detached read copies |
| D11 | Test-injected approval persists exact room/holder/root only |
| D12 | Test-injected denial persists and blocks posting |
| D13 | Both decisions reject repeated petitions, including new roots |
| D14 | Read-time root revocation deactivates membership, keeps decision |
| D15 | Holder-only protected post; direct attacker calls reject |
| D16 | Revocation blocks new notes and preserves public history |
| D17 | Nonmember/denied member cannot post or pass fake eligibility |
| D18 | Public reads, ordered pages, 20-page limit and 30-room-note cap |
| D19 | Admission records are not accepted as root input or issued as roots |
| D20 | Unpatched boundary fails closed; no client-supplied result |
| D21 | Invalid boundary result or exception leaves state unchanged |
| D22 | Same original root evaluated independently for separate rooms |
| D23 | Delimited keys separate 1/11 and normalize address casing |
| D24 | Unknown positive IDs return explicit stable shapes without writes |

State comparisons read the in-memory storage byte snapshot without restoring
it. Direct VM lazily materializes zero-filled slots on reads, so comparisons
discard implicit trailing zero bytes and entirely zero slots. They do not
simulate rollback to hide contract mutations. Tests that expect rejection
check the state immediately after the actual failing call.

The storage round-trip test constructs a fresh SDK object over the same byte
storage and attaches the SDK descriptor without rerunning the constructor.
This validates serialization, not live chain persistence.

## Commands

```bash
.venv/bin/python scripts/prepare_direct_sdk.py
.venv/bin/python -m pytest tests/direct -q --junitxml=evidence/phase1/direct-results.xml
.venv/bin/genvm-lint check contracts/context_bound_attestation.py --json
PATH="$PWD/.venv/bin:$PATH" .venv/bin/genvm-lint typecheck contracts/context_bound_attestation.py --json
PATH="$PWD/.venv/bin:$PATH" .venv/bin/genvm-lint typecheck contracts/context_bound_attestation.py --strict --json
.venv/bin/python -m pip check
```

Actual results and exit codes are in `evidence/phase1/` and the implementation
report. Do not treat the optional strict command as passed if it exits 1.

## Phase 0 strict warning recheck

The pinned SDK implements `public.view(f)` without a type annotation; it only
sets public/readonly attributes and returns `f`. Raw strict Pyright reports
`reportUnknownMemberType` on each of the six view decorators. Default
typecheck and full SDK schema extraction pass. All methods retain explicit
argument/return types. Internal runtime validators accept `object` and narrow
it, retaining security checks without unnecessary-isinstance diagnostics.

No global suppression, SDK patch or type-check output filtering is used.
Raw strict output is retained as FAIL with exactly six SDK-decorator
diagnostics; this limitation does not execute code or alter authorization,
serialization, read responses or deterministic state transitions. Direct
Mode and ABI tests check those behaviors separately. Other strict diagnostic
rules must still be reviewed and fixed rather than hidden.

N01–N10, AI evaluation of S01–S20, F01–F10, T01–T10 and real validator
convergence are **NOT RUN**. Numerical statement/branch coverage is not
measured; requirement coverage is D01–D24, not a fabricated percentage of
production consensus code.
