# Independent custom consensus — Phase 2

The production contract uses the Phase 0 pinned v0.2.16 SDK's custom
gl.vm.run_nondet_unsafe API once per apply_and_join. Deterministic issuer,
holder, revoked-root and one-decision-ever checks run first. Every other
write method remains deterministic.

The exact frozen blockquote template from
architecture-freeze-v1/03_CANONICAL_CONSENSUS_PROMPT.md is embedded as
CANONICAL_PROMPT, including all seven rules and marker names. Only Markdown
quote prefixes are removed. Original persisted source/requirement strings
are encoded as JSON string literals inside their fixed data markers; angle
brackets and ampersands are escaped to prevent closing-tag injection.
Template slots are substituted once in static pieces, so a placeholder
inside user data cannot expand another value. Tests recover the originals
and compare the entire static template to the authoritative document.

Leader independently calls _classify(prompt) and returns exactly one
decision field. Each Validator first calls _classify(prompt) itself, from
the same original-input prompt. It neither calls the Leader callback nor
uses Leader output/analysis in its prompt. Only after its independent
classification does it inspect the SDK Return envelope, validate the
Leader's one-key object and compare the exact ELIGIBLE / NOT_ELIGIBLE labels.
The callbacks capture only an immutable prompt string, contain no state
object, and serialize with the original pinned cloudpickle runner.

_classify uses SDK exec_prompt in text mode and parses the raw JSON with
duplicate-key detection. Missing/extra/duplicate keys, invalid JSON,
markdown fences, unsupported or non-string decisions, arrays and scalar
roots are rejected. No JSON extraction, output correction or approval
fallback exists. Both sides choosing NOT_ELIGIBLE is a meaningful accepted
denial. Ambiguity is classified conservatively by the unchanged Prompt.

Validator model/parser errors and VMError/UserError envelopes vote False.
Leader errors propagate. Unaccepted/undetermined custom execution cannot
return a business denial by fallback. The accepted return is schema-checked
again in deterministic code; only then may apply_and_join store its exact
root-bound decision. The node/network manages committee votes and leader
rotation; the contract does not implement an alternative network threshold.

No convenience equivalence wrapper, format-only Validator, frontend result,
cached eligibility, scope widening or mutable trust policy is introduced.

## What offline tests prove

Actual production callbacks execute through the pinned SDK exec_prompt/WASI
mock route, with separately scripted Leader/Validator outputs. Prompt hashes,
role-specific call counts, malformed results, failed votes and unchanged
storage are tested. Three separately invoked mock Validators each classify;
a later disagreeing mock blocks the test executor's accepted return.

Pinned Direct Mode normally returns after Leader and captures Validator for
manual invocation. For state tests, a TEST-ONLY synchronous executor invokes
the actual callbacks and returns only if its configured mock votes accept;
it never restores storage to hide mutations. This is a conservative offline
gate, not a simulation of actual network majority/finality/rotation. A
separate native Direct Mode smoke test captures and reruns the actual
Validator without writing an admission.

genlayer-test 0.29.2 auto-parses mock JSON even in text mode. The test transport
therefore JSON-encodes the raw text once to preserve the original raw response
for the production parser. This workaround exists only in tests; the contract
and SDK are not patched.

S01–S20 expected labels come from the frozen plan and are explicitly scripted
mock inputs. The tests prove prompt/data transport and independent comparison
for each fixture, including opposite-label disagreement. They do not measure
real LLM accuracy, prompt-injection resistance or multi-Validator convergence.
Real model/network outcomes and T01–T10 are NOT RUN.

## Type-check boundary

Default typecheck passes. Raw strict still fails: six original untyped
public.view diagnostics plus one newly exercised SDK run_nondet_unsafe
signature diagnostic (its Validator Result generic is unparameterized).
No rule is globally suppressed and no SDK source is modified. The original
diagnostics and exits are retained. See TESTING.md and the Phase 2 report.

STOP after Phase 2. No frontend, deployment or transactions are authorized.
