# CONTEXTPASS — ARCHITECTURE FREEZE V1 (AUTHORITATIVE)

## A. Definition, users, trust assumption
**Primitive**: `NonTransitiveContextAdmissionV1`, a context-conditional attestation-use gate.
**Product**: `ContextPass`, a lightweight community room where an owner fixes the room's entry requirement and one *trusted original issuer*. That issuer may attest to a holder's claimed scope. The holder petitions to enter using one original attestation. GenLayer performs a one-time independent semantic scope coverage decision, then records a **non-transferable, non-transitive, root-bound** admission. Members can post a short room note only while the root attestation remains valid.

Actors: `Issuer` (signed wallet creating a primary attestation); `Holder` (address claimed in the primary attestation); `SpaceOwner` (wallet creating a room and choosing its own issuer to trust); `Observer` (anyone with public reads); `Validator` (network consensus actor, never a privileged app issuer). The issuer is **not** presumed objectively credible; a room owner opts in to trust them. No identity verification beyond wallet ownership and explicit wallet-signaled action.

## B. Locked system architecture
- **One Intelligent Contract** (Python/GenVM), no separate EVM or escrow contract, no indexer/backend/database, no paid AI service.
- **One non-deterministic consensus entry**: `apply_and_join(space_id, root_attestation_id)`; all other write methods are deterministic.
- The same complete canonical Python contract source appears byte-for-byte in repo A `contracts/context_bound_attestation.py` and repo B `intelligent-contract/contracts/context_bound_attestation.py`; verify SHA-256 equality at packaging.
- Frontend: React + Vite + TypeScript + genlayer-js + plain CSS; GitHub Pages; no game engine/Next.js requirement.
- Studionet only: Chain ID 61999, RPC `https://studio.genlayer.com/api`; stable SDK/runner versions to be verified and pinned in Phase 0.

## C. Immutable V1 parameters and format
Use deterministic monotonic integer IDs starting at **1** for spaces, root attestations, and room notes; no user-supplied primary keys. Use address types supported by stable SDK. UTF-8 byte length limits, applied deterministically at entry:
- `space_title` 80 bytes; `required_scope` 320 bytes; `attestation_label` 80 bytes; `source_scope` 320 bytes; `room_note` 240 bytes.
- No empty, all-whitespace, or control-character inputs; normalize only safe leading/trailing whitespace. Do not rewrite semantics, autocorrect text or silently translate on chain.
- No personal health records, secrets, personal IDs or real financial data in publicly visible input.
- No expiry/versioned dynamic rule updating, optional tags, external evidence, nested credential chains, rewards, payable methods or tokenized credentials in V1.

## D. State schema (conceptual fields; use SDK-compatible TreeMap/DynArray, do not use ordinary Python dict/list for persisted GenVM state)

### `Space`
`id`, `owner:Address`, `title:str`, `required_scope:str`, `trusted_issuer:Address`. Requirement and issuer immutable. One trusted issuer per space. Space is public and persistent.

### `RootAttestation`
`id`, `issuer:Address`, `holder:Address`, `label:str`, `source_scope:str`, `revoked:bool`. Issuer and holder different addresses. Scope immutable. Revoked never becomes false.

### `AdmissionDecision`
Key `(space_id,holder)` encoded deterministically with stable unambiguous serialization. Fields: `space_id`, `holder`, `root_attestation_id`, `decision: ELIGIBLE | NOT_ELIGIBLE`. **One decision ever** per `(space_id,holder)` in v1, including denial; do not permit retry by submitting another root or re-issuing the same claim. This prevents shopping for a favorable LLM run. Root ID referenced is always a primary attestation, never an admission record. No derived attestation is issued.

### `RoomNote`
`id`, `space_id`, `author`, `text` and nothing privileged. Stored in per-space bounded index for read pagination. Notes are publicly readable. Admission permits **posting**, not confidential reading.

Indexes: next space/attestation/note ID counters, `spaces`, `roots`, `decisions_by_space_holder`, `notes`, `note_ids_by_space`; apply realistic page bounds (e.g. 20) and maximum 30 notes per space in first MVP to cap storage and RPC.

## E. Frozen public API (logical signature, actual SDK annotation types may adapt in implementation)
### Writes
1. `create_space(title, required_scope, trusted_issuer) -> space_id` — sender owns space; precheck valid issuer address; no editable requirement/issuer in v1.
2. `issue_attestation(holder, label, source_scope) -> attestation_id` — sender is issuer; holder != issuer; create original non-transferable claim. No claims of external truth.
3. `revoke_attestation(attestation_id)` — sender must equal issuer; irreversible; idempotent second call should safely reject or no-op with no new receipt effects, fixed and tested consistently (freeze choice: **reject** with `ALREADY_REVOKED`).
4. `apply_and_join(space_id, root_attestation_id) -> decision` — sender must be the root's holder; root not revoked; issuer equals space's trusted issuer; `(space_id, holder)` has no prior decision. Then run ONE custom nondeterministic result and **only after consensus** store exactly one admission decision. `ELIGIBLE` records member eligibility; `NOT_ELIGIBLE` records explicit denial. Return bounded decision. No membership writes before consensus.
5. `post_room_note(space_id, text) -> note_id` — deterministic on-chain write; checks `is_active_member(space_id, sender) == true` **inside the contract** immediately before appending. This write MUST fail after root revocation, even if user bypasses frontend.

### Reads
`get_space(space_id)`, `get_attestation(root_id)`, `get_decision(space_id,holder)`, `is_active_member(space_id,holder)`, `get_room_notes(space_id,offset,limit)`, `get_counts()`. Provide standard not-found/empty responses with explicit status. Pagination must have bounded page size; no unbounded scans.

## F. State transitions
`NO_ROOT → ROOT_ACTIVE → ROOT_REVOKED` (issuer only; irreversible).
`NO_DECISION → ELIGIBLE` OR `NO_DECISION → NOT_ELIGIBLE` (once only; consensus accepted, both final decisions).
`ELIGIBLE + ROOT_ACTIVE + correct exact owner/space/issuer link → ACTIVE_MEMBERSHIP` (derived view, **not stored as independent transferable claim**).
`ELIGIBLE + ROOT_REVOKED → INACTIVE_MEMBERSHIP` immediately as determined by read-time source lookup; no cascade loop or extra write required. Posts already written persist as historical records (public log).
`NOT_ELIGIBLE` never grants admission; no appeal/retry/override in v1. With failed/undetermined consensus, retain `NO_DECISION` because no state write should finalize.

## G. Invariants / authorization
- No wallet other than root issuer may revoke its root; no self-issuance; no holder may change scope, issuer, root content, or decision fields.
- A room trusts **only the one issuer** fixed by its owner at room creation; no automatic global whitelist or delegation.
- All decisions link `(room, holder, exactly one root)`; a root's approval in Room X does not allow entry into Room Y without new independent evaluation.
- An admission is **never** a new credential and never an input to `issue_attestation` or `apply_and_join`. No derived trust chain, composability or scope widening.
- `is_active_member()` checks stored `ELIGIBLE`, holder+room, root still active, original issuer matches room's fixed trusted issuer. Never rely on frontend caches as authority.
- `post_room_note()` does not consult frontend state or old cached eligibility.
- Deterministic checks precede the expensive nondet call. Zero on-chain side effects on invalid authorization, malformed input, failure/undetermined consensus.
- Explicit `NOT_ELIGIBLE` is an accepted negative semantic decision, not the same as a network consensus failure; the former creates an immutable denial record, the latter changes no state.
- External URLs/LLM opinions are neither required nor authoritative; issuer's text is an assertion, not a proven fact.
- Duplicate request with same or different root for a decided `(space,holder)` fails; re-issuing a credential does not override prior room decision.
- No arbitrary users can edit spaces' requirements after establishment or change issuer allowlist.
- On-chain room notes and credential scopes are public; not a privacy system.

## H. One fixed independent Leader/Validator consensus
Authoritative prompt and equivalence are in `03_CANONICAL_CONSENSUS_PROMPT.md`. Leader independently classifies `(source_scope, required_scope)`. Validator independently runs the **same classification from the original fixed inputs, without being shown Leader reasoning**, then performs deterministic exact comparison of `decision` only (`ELIGIBLE` or `NOT_ELIGIBLE`); both may agree on rejection. Business result contains ONE key `decision`. All ambiguity maps to `NOT_ELIGIBLE`. Leader error/malformed output never becomes approval. Validators reject malformed result, unrelated keys, unsupported outputs, or inconsistent decision. Use supported stable SDK's custom `run_nondet_unsafe` semantic pattern; prohibit replacing it with output-only schema checks, `strict_eq`, `prompt_comparative`, `prompt_non_comparative` or trusting the frontend's answer. No additional semantic comparison or special external source needed.

## I. Real user journey (Projects acceptance)
1. Wallet A acts as issuer and creates a credential for Wallet B endorsing narrow React UI component authorship.
2. Wallet A or Wallet C creates Room 1 requiring React UI component authorship, trusting A.
3. B connects wallet, selects original credential, invokes `apply_and_join` → finalized independent consensus `ELIGIBLE` → `is_active_member=true`.
4. B posts an on-chain room note; the contract allows it.
5. Create Room 2 requiring security audit skill but trusting A. B applies same root → finalized `NOT_ELIGIBLE`; B cannot post to Room 2.
6. A revokes the original attestation. B's active admission in Room 1 becomes inactive and B can no longer post there.
7. Reviewer can load room/credential IDs without owning A/B wallets; history, source link and read checks persist across reloads. All proof is real transaction hashes and actual chain reads.

## J. UX constraints
Four routes/panels are sufficient: `Overview/Verified Demo`, `Spaces`, `Credentials`, `My Admissions & Room Notes`. Clear wallet/network status; read-only visitor mode; exact failure classification (wallet refusal, wrong chain, 429 with Retry-After, tx pending/undetermined, rejected decision, revoked root). Single-flight reads; respect RPC rate limits, no polling storms or infinite retries. Only update UI state on finalized receipt + successful on-chain readback. Show no fake demo tx or mocked Finalized labels. Responsive visual hierarchy and copy human-reviewed for GenLayer Portal.

## K. Out of scope / rejected
NFTs, balances and payments, automatic expertise grading, issuer KYC, Sybil resistance guarantee, privacy-preserving membership, external API scraping, import arbitrary offchain VCs, multi-hop derivation, reward incentives, chats with a database, ranking engine, dynamic rule editing, long-lived backend agent. This is deliberate MVP scope control.
