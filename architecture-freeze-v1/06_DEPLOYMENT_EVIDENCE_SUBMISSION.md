# Deployment and provenance reference

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

## Wallet execution evidence
- Canonical deployed contract address, chain ID, source hash and deployment tx URL.
- T02–T10 transaction IDs/Explorer links and explicit observed final statuses, validator votes/count where available, rounds/rotations if shown.
- Screen or text capture of `get_attestation`, `get_space`, `get_decision`, `is_active_member`, `get_room_notes` for approved, denied, revoked scenarios.
- Public GitHub Pages URL and mobile/desktop preview after frontend integration.
- No keys, seed phrases, wallet exports, auth tokens or secret local configuration.

## Public evidence index
Each claim links to an exact explorer TX or read-only on-chain view with chain ID, method, wallet role, finalized consensus outcome, stored IDs. Screenshots supplemental only. Include negative gate attempts where tx may revert plus readback unchanged. Provide direct URL to verified real room and source credential for reviewers without seeded demo wallets. Display any validator disagreement or undetermined retry as such.

