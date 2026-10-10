# Current verification navigation — Phase 4E

Fresh commands, exit codes and outputs are recorded in evidence/phase4e and PHASE_4E_SUBMISSION_AUDIT.md. Earlier test counts below belong to their stated phases, not fresh executions. Known raw Python Strict failures are retained. B scripts/verify-phase4c.py and scripts/verify-onchain-readonly.mjs referenced by earlier documentation are absent in audited main; do not instruct reviewers to run missing scripts. Use the existing commands and test/source files. Prior browser QA is partial; Phase 4D includes one live create_space only.

---

## Historical / Superseded — retained verbatim

# Phase 4C final verification

A240/240 offline PASS; B145/145 offline PASS (124 retained + 20 activation + 1 manifest). Seven test files: activation20,address8,journey1,packaging6,reliability57,transactions39,ui14. Real read-only SDK23/23 operations successful, including ten actual FINALIZED receipts and ten current-state reads. Studio transactions were user-manual, not executed through this frontend. Actual pinned SDK replay of genuine captured receipts is offline evidence only.

Run B `python scripts/verify-phase4c.py` for the full current offline harness; it records exact command arrays/cwd/UTC/exits and full logs/JUnit/frontend JSON in A/B evidence/phase4c. It never signs or transacts. TypeScript Strict/build/source/static/default types PASS. Raw Python Strict FAIL retains exactly seven upstream reportUnknownMemberType diagnostics with no suppression. See PHASE_4C_INTEGRATION_REPORT.md for commands and risks.

The optional separately authorized read-only snapshot tool is B scripts/verify-onchain-readonly.mjs; it rate-spaces reads, rejects writes and stops on429. Current original snapshots are gzip archived with SHA, not silently replaced with a rerun. Real browser/wallet/sign/submission/reload QA NOT RUN; normal Chrome local URL returned ERR_CONNECTION_REFUSED. RELEASE_READINESS_CHECKLIST.md contains manual QA. Pages not published.

Historical tests below accurately describe their earlier unexecuted network status; ONCHAIN_EVIDENCE_INDEX.md supersedes only current T/network facts. S01–S20 remain offline script classifications, not twenty new real model tests.

## Historical test documentation

# Phase 4B verification

Address suite: 77/77 PASS. A total: 240/240 PASS (163 existing + 77 new). B frontend: 124/124 PASS (116 existing + 8 new). All offline; scripted semantic outcomes are not real model/validator results. See Phase 4B report and evidence/phase4b for actual commands and the intentional pre-fix INVALID_ADDRESS failure. Python Strict retains upstream diagnostics; final status is recorded in the report. No suppression or SDK patch.

# Phase 2 offline verification

Results: **163/163 PASS**, 0 failures/errors/skips. Separate runs: D regression
54/54 PASS and consensus suite 109/109 PASS. Raw logs, commands, JUnit and
measured callback traces are in evidence/phase2/. Requirement coverage is
D01–D24, N01–N10 and 20 scripted S fixtures, not statement/branch coverage.

Tests use the actual canonical source and exact SDK v0.2.16. The integration
plugin is disabled; socket connection APIs are blocked. SDK artifacts must
already be cached. No Docker/node, LLM provider, signing or blockchain call
is used. The preparation script extracts the original Phase 0 cloudpickle
runner from the verified artifact, because Direct Mode omits that transitive
runner from its import path. No pip latest or dependency-version change.

## Deterministic regression coverage

Selected D tests still isolate the private boundary to verify deterministic
post-consensus behavior. D20 now models an unaccepted custom gate; the
Phase 1 fail-closed stub/source guard is adapted to the implemented Phase 2
gate. All 54 cases remain, with no removal of D requirements.

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
| D20 | Unaccepted custom gate fails closed; no client-supplied result |
| D21 | Invalid boundary result or exception leaves state unchanged |
| D22 | Same original root evaluated independently for separate rooms |
| D23 | Delimited keys separate 1/11 and normalize address casing |
| D24 | Unknown positive IDs return explicit stable shapes without writes |

## Independent callback acceptance coverage

| ID | Tested offline behavior |
|---|---|
| N01 | Separate Leader/Validator approval calls, canonical accepted membership |
| N02 | Independent agreed denial, immutable denial and blocked notes |
| N03 | Leader approval / Validator denial rejects without records |
| N04 | Leader denial / Validator approval rejects without records |
| N05 | 19 malformed raw Leader outputs and 8 corrupt result envelopes; no state changes |
| N06 | 19 malformed Validator outputs, timeout and model exception vote False |
| N07 | Data markers, placeholder/instruction injection preserved as escaped data; scripted denial |
| N08 | Unresolved execution, Leader error, unreturned transport failure leave all state unchanged |
| N09 | Three independent Validator calls, later disagreement, VM/User error envelopes, same original Prompt |
| N10 | Refusal/unaccepted gate remains NO_DECISION after fresh SDK storage read |

N tests expand into 61 cases. Two supplemental tests compare the exact frozen
template and inspect callback structure. The native SDK capture/rerun smoke
test plus five wrong-text-return guards add six cases.

S01–S20 each run two cases (40 total): frozen expected label supplied separately
as a Leader and Validator SCRIPT, and an opposite-label Validator SCRIPT.
Tests verify original data transport, canonical parser, both model invocations,
exact comparison, membership or unchanged state. **No real model result is
measured.** The expected classifications are design expectations only. Real
S-model accuracy, prompt-injection resistance and network convergence NOT RUN.

## Executor limits and measured traces

The pinned Direct Mode shim executes Leader immediately and only captures the
Validator. The TEST-ONLY synchronous executor replaces that shim, runs actual
production callbacks through the pinned SDK exec_prompt/WASI route, and returns
only after its configured offline votes accept. It is not the real network
majority/finality/rotation implementation. A separate native Direct Mode test
captures and reruns the actual Validator without storing an admission.

Callbacks capture only the immutable original-input Prompt and serialize using
the pinned cloudpickle runner. Before and after every callback, tests compare
persistent storage; no snapshot restoration masks a mutation. Each model call
records its role and prompt hash. N09 proves independent repeated classification,
including a later opposing vote; shape-valid but opposite labels reject.

genlayer-test 0.29.2 automatically JSON-decodes mocked responses even with text
mode. Tests encode the raw output once as a JSON string to pass it unchanged to
the production raw parser. Duplicate keys and markdown remain raw and reject.
Neither production SDK nor contract contains this transport workaround.

Storage comparisons canonicalize implicit zero slots/trailing zero bytes that
Direct Mode materializes on reads. Fresh-object readback attaches the original
SDK storage descriptor without rerunning the constructor. This verifies local
serialization, not live persistence or finalized transactions.

## Commands

```bash
.venv/bin/python scripts/prepare_direct_sdk.py
.venv/bin/python -m pytest tests/direct -q
.venv/bin/python -m pytest tests/consensus -q
.venv/bin/python -m pytest tests/direct tests/consensus -q --junitxml=evidence/phase2/all-results.xml
.venv/bin/genvm-lint check contracts/context_bound_attestation.py --json
PATH="$PWD/.venv/bin:$PATH" .venv/bin/genvm-lint typecheck contracts/context_bound_attestation.py --json
PATH="$PWD/.venv/bin:$PATH" .venv/bin/genvm-lint typecheck contracts/context_bound_attestation.py --strict --json
.venv/bin/python -m pip check
```

For measured traces, set CONTEXTPASS_TRACE_FILE to an evidence path before the
combined run. Actual absolute commands/PATH and trace setting are recorded in
evidence/phase2/command-results.json. Phase 1 logs are preserved unchanged.

## Strict diagnostics — FAIL, not all green

Lint/schema pass (5 writes, 6 views). Default typecheck passes with no diagnostics.
Raw strict exits 1 / ok=false with **7 reportUnknownMemberType diagnostics**:
the existing 6 public.view missing annotations and 1 SDK run_nondet_unsafe
signature using an unparameterized Result generic. The upstream implementation
and signature are recorded in SDK evidence; no SDK patch or global suppression
is applied. Other implementation diagnostics discovered during development
were fixed rather than hidden. JSON summary.errors=0 is inconsistent with the
diagnostics; exit/ok and diagnostic list determine FAIL.

These SDK type metadata limitations do not change runtime authorization,
serialization or the custom comparator. Offline tests verify those separately.
They remain unresolved upstream; no production convergence claim follows.

F01–F10 and T01–T10: NOT RUN. No real AI/network result, deployment, transaction,
frontend, Repository B, merge or Phase 3 execution. STOP pending authorization.
