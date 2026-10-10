# DEPLOYMENT, PROVENANCE, REVIEW & PORTAL PACKAGING V1

## Readiness status
No contract deployed. No transaction sent. No PR created. No Portal submission. No real SDK/tool or validator convergence test run as part of Freeze V1.

## Fixed environment
- Network: **Stable GenLayer Studionet**; Chain ID **61999**.
- RPC: https://studio.genlayer.com/api
- Explorer: https://explorer-studio.genlayer.com/
- Free test GEN: Studio built-in faucet (wallet/account selector water drop). Execution may spend test GEN; check before each operation.
- GitHub source: gqzy1 (exact repo addresses pending creation).
- Browser signing: Wallet A issuer and room owner; Wallet B credential holder, both controlled/signing manually by user.
- Pinned Python GenLayer SDK, GenVM runner, genlayer-test, genlayer-js versions and exact constructor shape are **TBD Phase 0**, not safe to fabricate now.

## Manual two-wallet verification package — supply actual values only after code exists
A. Upload `contracts/context_bound_attestation.py` from A's main; confirm B packaged hash identical. Deploy with the **actual constructor values discovered in code**, with no guessed args. Record deployment tx, address, chain/network, FINALIZED status, validator voting and consensus result.
B. As A `issue_attestation(B, "React UI components", "Can develop and maintain React UI components.")`; capture root ID and tx.
C. As A `create_space("React Components", "Contribute React UI components to this room.", A)`; capture Room 1 ID and tx.
D. As B `apply_and_join(Room1ID, RootID)`; independently check final `ELIGIBLE`, source binding and `is_active_member(Room1,B)`.
E. As B `post_room_note(Room1ID, "Hello from an approved member")`; read note back by view.
F. As A `create_space("Security Audit", "Perform security audits of production authentication systems.", A)`; Room 2.
G. As B `apply_and_join(Room2ID, RootID)`; independently check finalized `NOT_ELIGIBLE`, not a transport error, and `is_active_member(Room2,B)==false`.
H. Attempt as B `post_room_note(Room2ID, "should not pass")`; verify rejection and note count unchanged.
I. As A `revoke_attestation(RootID)`; check `is_active_member(Room1,B)==false` immediately.
J. Attempt posting to Room 1 from B; verify rejection and historical Room1 note remains readable.

Pre-bake final implementation-specific numeric IDs and arg types into `MANUAL_STUDIO_EXECUTION.md` after Phase 4 precheck. NEVER make up tx IDs/consensus state/contract address. If an LLM divergence prevents T04/T07 real FINALIZED, report; don't assume success due to a pending preview.

## What the user sends back after manual signature
- Canonical deployed contract address, chain ID, source hash and deployment tx URL.
- T02–T10 transaction IDs/Explorer links and explicit observed final statuses, validator votes/count where available, rounds/rotations if shown.
- Screen or text capture of `get_attestation`, `get_space`, `get_decision`, `is_active_member`, `get_room_notes` for approved, denied, revoked scenarios.
- Public GitHub Pages URL and mobile/desktop preview after frontend integration.
- No keys, seed phrases, wallet exports, auth tokens or secret local configuration.

## Repo A — Intelligent Contracts submission content
README: unique primitive, trust assumption, why GenLayer necessary, state diagrams, custom independent Validator/equivalence description, write/read API, 2-wallet usage, invariants, Direct Mode test run, compiler/linter success, real finalized consensus proof, deployment details and cross-language (Chinese/English input) behavior. Standalone review must not require frontend repo.

## Repo B — Projects submission content
README: real target audience/use case, screenshots, wallet support, every click-to-chain path, two-space genuine onchain walkthrough, protected posting and revocation, read-only explorer demo, failure handling, SDK/network build instructions, byte-exact contract copy, deployment provenance and proof index. No misleading 'privacy' or 'real skills verified' claims.

## Public evidence index
Each claim links to an exact explorer TX or read-only on-chain view with chain ID, method, wallet role, finalized consensus outcome, stored IDs. Screenshots supplemental only. Include negative gate attempts where tx may revert plus readback unchanged. Provide direct URL to verified real room and source credential for reviewers without seeded demo wallets. Display any validator disagreement or undetermined retry as such.

## Portal data hygiene
- Two DIFFERENT GitHub repository URLs (A and B).
- Two self-contained submissions, overlapping contract source as legitimate shared primitive; explain provenance.
- Avoid duplicated link entries within Portal fields; check site and receipt links if Portal validation rejects duplicates.
- Primary tag proposal for B: Identity & Trust (身份与信誉), specific tags chosen from real visible Portal categories only.
- IC and Project points/review eligibility are never guaranteed. No promise of award, high score or guaranteed approval.

## Explicit STOP before submitting
Work may prepare submission text and README but MUST NOT submit to Portal unless separately approved by user, and MUST NOT execute deployments or signed transactions.
