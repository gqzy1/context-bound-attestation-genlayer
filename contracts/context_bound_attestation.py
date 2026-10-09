# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

"""ContextPass V1 deterministic core. Phase 1 only; DO NOT DEPLOY.

The production semantic boundary always raises CONSENSUS_NOT_IMPLEMENTED.
No test decision flag, admin admission override, or external result is accepted.
"""

from dataclasses import dataclass
import unicodedata

from genlayer import Address, DynArray, TreeMap, allow_storage, gl, u256


MAX_ID = (1 << 256) - 1
MAX_PAGE_SIZE = 20
MAX_NOTES_PER_SPACE = 30


@allow_storage
@dataclass
class Space:
    id: u256
    owner: Address
    title: str
    required_scope: str
    trusted_issuer: Address


@allow_storage
@dataclass
class RootAttestation:
    id: u256
    issuer: Address
    holder: Address
    label: str
    source_scope: str
    revoked: bool


@allow_storage
@dataclass
class AdmissionDecision:
    space_id: u256
    holder: Address
    root_attestation_id: u256
    decision: str


@allow_storage
@dataclass
class RoomNote:
    id: u256
    space_id: u256
    author: Address
    text: str


def _text(value: object, max_bytes: int) -> str:
    if not isinstance(value, str):
        raise gl.vm.UserError("INVALID_TEXT")
    # Check the original input before trim: a tab/newline must not disappear.
    # Cc includes ASCII and C1 controls. No semantic normalization is performed.
    if any(unicodedata.category(char) == "Cc" for char in value):
        raise gl.vm.UserError("CONTROL_CHARACTER")
    clean = value.strip()
    if not clean:
        raise gl.vm.UserError("EMPTY_TEXT")
    if len(clean.encode("utf-8")) > max_bytes:
        raise gl.vm.UserError("TEXT_TOO_LONG")
    return clean


def _address(value: object) -> Address:
    if not isinstance(value, Address) or value.as_bytes == bytes(20):
        raise gl.vm.UserError("INVALID_ADDRESS")
    return value


def _id(value: object) -> u256:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_ID:
        raise gl.vm.UserError("INVALID_ID")
    return u256(value)


def _pagination(offset: object, limit: object) -> tuple[int, int]:
    if (
        isinstance(offset, bool) or not isinstance(offset, int) or offset < 0
        or isinstance(limit, bool) or not isinstance(limit, int)
        or not 1 <= limit <= MAX_PAGE_SIZE
    ):
        raise gl.vm.UserError("INVALID_PAGINATION")
    return offset, limit


def _decision_key(space_id: u256, holder: Address) -> str:
    # Delimited decimal ID + fixed-length lowercase raw address; no ambiguity,
    # checksum/casing dependency, or Python process hash.
    return str(int(space_id)) + ":" + holder.as_bytes.hex()


class NonTransitiveContextAdmissionV1(gl.Contract):
    next_space_id: u256
    next_attestation_id: u256
    next_note_id: u256
    spaces: TreeMap[u256, Space]
    roots: TreeMap[u256, RootAttestation]
    decisions_by_space_holder: TreeMap[str, AdmissionDecision]
    notes: TreeMap[u256, RoomNote]
    note_ids_by_space: TreeMap[u256, DynArray[u256]]

    def __init__(self) -> None:
        self.next_space_id = u256(1)
        self.next_attestation_id = u256(1)
        self.next_note_id = u256(1)

    def _space(self, space_id: int) -> Space:
        space = self.spaces.get(_id(space_id))
        if space is None:
            raise gl.vm.UserError("SPACE_NOT_FOUND")
        return space

    def _root(self, root_id: int) -> RootAttestation:
        root = self.roots.get(_id(root_id))
        if root is None:
            raise gl.vm.UserError("ATTESTATION_NOT_FOUND")
        return root

    def _semantic_decision(self, source_scope: str, required_scope: str) -> str:
        """Phase 2 boundary; no fallback denial or approval in Phase 1."""
        raise gl.vm.UserError("CONSENSUS_NOT_IMPLEMENTED")

    @gl.public.write
    def create_space(self, title: str, required_scope: str, trusted_issuer: Address) -> int:
        title = _text(title, 80)
        required_scope = _text(required_scope, 320)
        trusted_issuer = _address(trusted_issuer)
        owner = _address(gl.message.sender_address)
        sid = self.next_space_id
        if sid == MAX_ID:
            raise gl.vm.UserError("ID_EXHAUSTED")
        self.spaces[sid] = Space(sid, owner, title, required_scope, trusted_issuer)
        self.next_space_id = u256(sid + 1)
        return int(sid)

    @gl.public.write
    def issue_attestation(self, holder: Address, label: str, source_scope: str) -> int:
        holder = _address(holder)
        issuer = _address(gl.message.sender_address)
        if holder == issuer:
            raise gl.vm.UserError("SELF_ISSUANCE")
        label = _text(label, 80)
        source_scope = _text(source_scope, 320)
        rid = self.next_attestation_id
        if rid == MAX_ID:
            raise gl.vm.UserError("ID_EXHAUSTED")
        self.roots[rid] = RootAttestation(rid, issuer, holder, label, source_scope, False)
        self.next_attestation_id = u256(rid + 1)
        return int(rid)

    @gl.public.write
    def revoke_attestation(self, attestation_id: int) -> None:
        root = self._root(attestation_id)
        if gl.message.sender_address != root.issuer:
            raise gl.vm.UserError("ISSUER_ONLY")
        if root.revoked:
            raise gl.vm.UserError("ALREADY_REVOKED")
        root.revoked = True

    @gl.public.write
    def apply_and_join(self, space_id: int, root_attestation_id: int) -> str:
        space = self._space(space_id)
        root = self._root(root_attestation_id)
        holder = _address(gl.message.sender_address)
        if holder != root.holder:
            raise gl.vm.UserError("HOLDER_ONLY")
        if root.revoked:
            raise gl.vm.UserError("ROOT_REVOKED")
        if root.issuer != space.trusted_issuer:
            raise gl.vm.UserError("UNTRUSTED_ISSUER")
        key = _decision_key(space.id, holder)
        if key in self.decisions_by_space_holder:
            raise gl.vm.UserError("DECISION_EXISTS")

        # No state writes before the semantic boundary. The shipped Phase 1
        # boundary raises. Only tests replace this PRIVATE function locally.
        decision = self._semantic_decision(root.source_scope, space.required_scope)
        if decision not in ("ELIGIBLE", "NOT_ELIGIBLE"):
            raise gl.vm.UserError("INVALID_CONSENSUS_RESULT")
        self.decisions_by_space_holder[key] = AdmissionDecision(
            space.id, holder, root.id, decision
        )
        return decision

    @gl.public.write
    def post_room_note(self, space_id: int, text: str) -> int:
        space = self._space(space_id)
        text = _text(text, 240)
        author = _address(gl.message.sender_address)
        ids = self.note_ids_by_space.get(space.id)
        if ids is not None and len(ids) >= MAX_NOTES_PER_SPACE:
            raise gl.vm.UserError("SPACE_NOTE_LIMIT")
        nid = self.next_note_id
        if nid == MAX_ID:
            raise gl.vm.UserError("ID_EXHAUSTED")
        # Re-read root validity INSIDE the contract immediately before append.
        if not self.is_active_member(int(space.id), author):
            raise gl.vm.UserError("ACTIVE_MEMBER_ONLY")
        self.notes[nid] = RoomNote(nid, space.id, author, text)
        self.note_ids_by_space.get_or_insert_default(space.id).append(nid)
        self.next_note_id = u256(nid + 1)
        return int(nid)

    @gl.public.view
    def get_space(self, space_id: int) -> dict[str, str | int | bool]:
        space = self.spaces.get(_id(space_id))
        if space is None:
            return {"status": "NOT_FOUND"}
        return {
            "status": "FOUND", "id": int(space.id), "owner": space.owner.as_hex,
            "title": space.title, "required_scope": space.required_scope,
            "trusted_issuer": space.trusted_issuer.as_hex,
        }

    @gl.public.view
    def get_attestation(self, root_id: int) -> dict[str, str | int | bool]:
        root = self.roots.get(_id(root_id))
        if root is None:
            return {"status": "NOT_FOUND"}
        return {
            "status": "FOUND", "id": int(root.id), "issuer": root.issuer.as_hex,
            "holder": root.holder.as_hex, "label": root.label,
            "source_scope": root.source_scope, "revoked": root.revoked,
        }

    @gl.public.view
    def get_decision(self, space_id: int, holder: Address) -> dict[str, str | int | bool]:
        key = _decision_key(_id(space_id), _address(holder))
        decision = self.decisions_by_space_holder.get(key)
        if decision is None:
            return {"status": "NO_DECISION"}
        return {
            "status": "FOUND", "space_id": int(decision.space_id),
            "holder": decision.holder.as_hex,
            "root_attestation_id": int(decision.root_attestation_id),
            "decision": decision.decision,
        }

    @gl.public.view
    def is_active_member(self, space_id: int, holder: Address) -> bool:
        sid = _id(space_id)
        holder = _address(holder)
        space = self.spaces.get(sid)
        if space is None:
            return False
        decision = self.decisions_by_space_holder.get(_decision_key(sid, holder))
        if decision is None or decision.decision != "ELIGIBLE":
            return False
        if decision.space_id != sid or decision.holder != holder:
            return False
        root = self.roots.get(decision.root_attestation_id)
        return (
            root is not None and root.id == decision.root_attestation_id
            and root.holder == holder and not root.revoked
            and root.issuer == space.trusted_issuer
        )

    @gl.public.view
    def get_room_notes(self, space_id: int, offset: int, limit: int) -> dict[str, str | int | list[dict[str, str | int]]]:
        sid = _id(space_id)
        offset, limit = _pagination(offset, limit)
        if sid not in self.spaces:
            return {"status": "NOT_FOUND", "notes": [], "total": 0, "next_offset": 0}
        ids = self.note_ids_by_space.get(sid)
        total = 0 if ids is None else len(ids)
        start = min(offset, total)
        end = min(start + limit, total)
        result: list[dict[str, str | int]] = []
        if ids is not None:
            for index in range(start, end):
                note = self.notes[ids[index]]
                result.append({
                    "id": int(note.id), "space_id": int(note.space_id),
                    "author": note.author.as_hex, "text": note.text,
                })
        return {"status": "FOUND", "notes": result, "total": total, "next_offset": end}

    @gl.public.view
    def get_counts(self) -> dict[str, int]:
        return {
            "spaces": int(self.next_space_id) - 1,
            "attestations": int(self.next_attestation_id) - 1,
            "decisions": len(self.decisions_by_space_holder),
            "notes": int(self.next_note_id) - 1,
        }
