# ContextPass protocol reference

ContextPass derives room-local admission from an original issuer assertion. The room fixes its trusted issuer and requirements. Independent Leader and Validator executions check whether the original scope covers every requirement; deterministic guards bind the result to one holder, room and root.

The admission is non-transferable and cannot issue another credential. Root revocation disables future protected posts without deleting historical decisions or notes. Issuer trust remains a room-owner choice; the protocol does not authenticate real-world skill, prevent collusion or make public content private.

## Reference map

- [State and interface](02_ARCHITECTURE_FREEZE_V1.md)
- [Canonical classification prompt](03_CANONICAL_CONSENSUS_PROMPT.md)
- [Verification cases](04_TEST_ACCEPTANCE_PLAN.md)
- [Implementation layers](05_WORK_MASTER_AND_PHASE_COMMANDS.md)
- [Evidence requirements](06_DEPLOYMENT_EVIDENCE_SUBMISSION.md)

Stable Studionet: chain ID 61999, RPC https://studio.genlayer.com/api. The repository README describes the deployed version and measured test coverage; these reference specifications do not establish a live result by themselves.
