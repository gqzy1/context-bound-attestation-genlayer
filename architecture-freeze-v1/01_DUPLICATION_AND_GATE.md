# Trust model and related standards

ContextPass uses issuer assertions, holder identity and destination trust as distinct inputs. Its admission decision asks whether the original assertion covers one room's full requirements. A positive result is local to that room and root; it is not a new attestation or a proof of the asserted skill.

Established references include the [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model-2.0/) for issuer/holder/verifier terminology and [EAS revocation](https://docs.attest.org/docs/core--concepts/revocation) for attestation lifecycle concepts. ContextPass does not claim standards interoperability.

## Conservative semantic boundary

Only explicit coverage of every essential requirement permits ELIGIBLE. Missing scope, ambiguity or unsupported assumptions cannot enlarge the issuer's assertion. Deterministic checks enforce issuer trust, holder identity, revocation and the one-decision rule before protected access.

Independent model executions can still share errors. Real convergence, finality and access-control behavior require the separately recorded Studionet evidence; local fixtures establish code behavior only. A room owner and issuer may collude, and separate wallets do not establish unique people.
