# Phase 1 consensus boundary

There is **no Leader/Validator implementation in this draft**. The private
`_semantic_decision(source_scope, required_scope)` unconditionally raises
`CONSENSUS_NOT_IMPLEMENTED`, after public `apply_and_join` prechecks and before
any decision write. An unimplemented or failed evaluation does not create a
denial record and never grants membership.

The only public semantic-entry inputs are `space_id` and
`root_attestation_id`. No external decision, score, AI flag, mock mode,
owner override, constructor switch or admission setter is exposed in ABI.

`tests/conftest.py` temporarily monkeypatches this private method for selected
tests. Outcomes exercise deterministic storage/gating only. They are neither
semantic fixtures evaluated by AI nor consensus convergence evidence. Other
tests run the unpatched source and prove the closed boundary leaves no state.

After explicit Phase 2 approval, implement the unchanged canonical prompt
using the fixed stable SDK custom `run_nondet_unsafe` pattern. Leader and each
Validator independently classify original stored inputs; Validator compares
only exact decision enum after validating the one-key result. Both canonical
labels are meaningful. State writes remain after accepted consensus. Do not
substitute strict_eq or comparative/non-comparative convenience wrappers.

The canonical prompt and N01–N10/S01–S20 expectations are preserved in the
frozen documents, but none is claimed as passed in Phase 1.

