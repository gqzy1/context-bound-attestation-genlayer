# Deterministic V1 implementation notes

The unmodified `architecture-freeze-v1/02_ARCHITECTURE_FREEZE_V1.md` is
authoritative. This file documents concrete representation choices only.

## Storage and transitions

`Space`, `RootAttestation`, `AdmissionDecision` and `RoomNote` are
`@allow_storage` records. Counters and record IDs use `u256`. Persisted maps
are `TreeMap`; per-room note IDs use `TreeMap[u256, DynArray[u256]]`. Plain
Python dictionaries/lists are transient parsing, consensus or ABI values,
never persisted state. The constructor takes no arguments.

Root: absent → active → revoked. Only issuer revokes; repeated revocation
rejects `ALREADY_REVOKED`. Room requirements/trusted issuer and root contents
have no mutation or transfer methods.

Decision key: decimal space ID, colon, 40 lowercase hexadecimal characters
from the holder's raw address bytes. The key is independent of checksum case
and Python hashes. One decision per key, referencing only `roots`. A
decision is not an attestation and cannot widen or transfer the source scope.
Equal numeric values in different ID domains do not imply a derived root:
`root_attestation_id` always looks up only the original roots map.

The deterministic write path validates ownership, active root, trusted issuer
and absent prior decision, then calls the private semantic boundary. That
boundary now executes the frozen independent custom consensus. Only an
accepted canonical result can return for deterministic persistence; production
has no switch accepting client/test decisions. See CONSENSUS.md.

`ELIGIBLE` + exact room/holder/root binding + active root + trusted original
issuer yields active membership at read time. A revoked root yields false
without cascades or independent membership writes. Posting rechecks membership
inside the contract and historical notes persist after revocation.

## Input choices within frozen bounds

Leading/trailing Unicode whitespace is trimmed; no translation, autocorrection
or Unicode semantic normalization. Unicode `Cc` control characters, including
tabs, newlines, NUL, DEL and C1 controls, are rejected in the original input
before trimming. The normalized stored text must be nonempty and within the
UTF-8 byte limits: title/label 80; required/source scope 320; note 240.

Address parameters use the SDK `Address` type; zero/malformed values reject.
SDK addresses do not validate EIP-55 spelling; authorization compares raw
20-byte addresses. Positive integer IDs only; booleans are not IDs. Counters
reject exhaustion before a `u256` increment can overflow.

Pagination: offset nonnegative integer; limit 1–20 inclusive; boolean values
reject. Large offsets return an empty page with next_offset equal to total.
Each room permits at most 30 notes, in global note-ID order, without scans
over other rooms. Notes have only id, space_id, author and text.

## Read shapes

| Method | Found | Unknown valid positive ID |
|---|---|---|
| get_space | status=FOUND plus id, owner, title, required_scope, trusted_issuer | `{status: NOT_FOUND}` |
| get_attestation | status=FOUND plus id, issuer, holder, label, source_scope, revoked | `{status: NOT_FOUND}` |
| get_decision | status=FOUND plus space_id, holder, root_attestation_id, decision | `{status: NO_DECISION}` |
| is_active_member | boolean | false |
| get_room_notes | status=FOUND, notes, total, next_offset | status=NOT_FOUND, notes=[], total=0, next_offset=0 |
| get_counts | spaces, attestations, decisions, notes | Not applicable |

Responses use checksum hexadecimal address strings, integer IDs and bounded
JSON-compatible values. Invalid inputs raise stable `gl.vm.UserError` codes,
not fabricated semantic decisions. No method is payable.

