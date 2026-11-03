# Implementation layers

The contract separates persistent records, deterministic guards and one custom nondeterministic admission boundary. Storage uses the pinned SDK containers. Root revocation and active-membership checks remain deterministic; storage mutation follows accepted semantic consensus.

The browser client uses the same complete contract source, source-hash binding, Stable Studionet chain checks and explicit wallet signatures. A transaction is confirmed only after finality, successful execution, call binding and method-specific finalized readback. Unknown submission outcomes retain the original intent rather than creating another write.

Local deterministic tests, scripted Leader/Validator tests, SDK compatibility checks and live receipts answer different verification questions. Their measured coverage is recorded in the repository testing documents. The canonical model prompt is specified in [03_CANONICAL_CONSENSUS_PROMPT.md](03_CANONICAL_CONSENSUS_PROMPT.md).
