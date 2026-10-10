# DEPLOYMENT_MANIFEST_STUDIONET — Phase 4C

| Field | Verified value |
|---|---|
| Network / Chain / RPC | Stable Studionet / 61999 / https://studio.genlayer.com/api |
| Canonical contract | `0xDe9abfBe2E4A61d23e27b552e241f5Bb1d1821b8` |
| Deployment transaction | `0x26282c539033879705d9a8dea18c8676dae46c0cd09df9f91cb20d740f9be994` |
| Source SHA256 | `e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d` |
| A canonical baseline | phase4b-address-compatibility / c7c6e50620602d03ad4e3c116ad1532097feab8a |
| Source path / B copy | contracts/context_bound_attestation.py / intelligent-contract/contracts/context_bound_attestation.py |
| Source blob | 10edfd3d23672789b4b600360750f5041c040f6d |
| GenVM / JS SDK | v0.2.16 header and original Depends / genlayer-js 1.1.8 |
| Constructor / methods | no args / unchanged five writes + six reads |
| Deployment / T01–T10 | User manual Studio execution; all FINALIZED rechecked read-only; expected T08/T10 rollback |
| Frontend write policy | Activated in independent Draft branch; canonical target only, manual wallet signature, two independent guards |
| Frontend real wallet / visual QA | NOT RUN / NOT RUN |
| Pages / Portal | NOT PUBLISHED / NOT SUBMITTED |

Deployed code was fetched and compared **byte-for-byte** with both repository copies. Header/Depends prove the packaged SDK selection, not each hosted Validator's binary inventory. Old deployment 0x97B9003a17A8EDBD1b5E3379AA659753791497d9 is superseded and is not the frontend target. Main in A remains bootstrap and is not canonical. Immutable historical reports retain their then-correct undeployed status; current evidence supersedes it.

Root 1 is revoked; historical Room 1 ELIGIBLE remains, active=false. No migration, upgrade or new deployment occurred in Phase 4C. See ONCHAIN_EVIDENCE_INDEX.md. No transaction was sent in this phase. STOP awaiting manual acceptance and later publication authorization.
