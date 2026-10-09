"""D01–D24: deterministic acceptance only. All consensus outcomes are test doubles."""
import ast
import inspect
from pathlib import Path

import pytest


SOURCE = Path(__file__).parents[2] / "contracts/context_bound_attestation.py"


def reject(code, function, *args):
    from genlayer import gl
    with pytest.raises(gl.vm.UserError, match=code):
        function(*args)


def join(contract, direct_vm, actors, sid, rid):
    direct_vm.sender = actors[1]
    return contract.apply_and_join(sid, rid)


def test_D01_monotonic_ids_and_owner(contract, direct_vm, actors):
    a, b, _, _ = actors
    direct_vm.sender = a
    assert contract.get_counts() == dict(spaces=0, attestations=0, decisions=0, notes=0)
    assert contract.create_space("One", "React", a) == 1
    direct_vm.sender = b
    assert contract.create_space("Two", "React", a) == 2
    assert contract.get_space(1)["owner"] == a.as_hex
    assert contract.get_space(2)["owner"] == b.as_hex


@pytest.mark.parametrize("field,bad", [
    ("title", ""), ("title", "   "), ("title", "a" * 81),
    ("title", "界" * 27), ("title", "\tRoom"), ("title", "Room\n"),
    ("required_scope", ""), ("required_scope", "\u3000"),
    ("required_scope", "a" * 321), ("required_scope", "界" * 107),
    ("required_scope", "scope\x00"), ("required_scope", "scope\x85"),
])
def test_D02_invalid_room_text_is_atomic(contract, direct_vm, actors, field, bad, storage_image):
    direct_vm.sender = actors[0]
    title, scope = (bad, "React") if field == "title" else ("Room", bad)
    before = storage_image()
    from genlayer import gl
    with pytest.raises(gl.vm.UserError):
        contract.create_space(title, scope, actors[0])
    assert storage_image() == before
    assert contract.get_counts()["spaces"] == 0


def test_D03_issuer_holder_and_scope(contract, direct_vm, actors):
    a, b, _, _ = actors
    direct_vm.sender = a
    assert contract.issue_attestation(b, "  React  ", "  熟悉 React 组件。  ") == 1
    assert contract.issue_attestation(b, "Other", "HTML") == 2
    assert contract.get_attestation(1) == {
        "status": "FOUND", "id": 1, "issuer": a.as_hex, "holder": b.as_hex,
        "label": "React", "source_scope": "熟悉 React 组件。", "revoked": False,
    }


def test_D04_self_issue_and_bad_addresses(contract, direct_vm, actors):
    from genlayer import Address
    a, b, _, _ = actors
    direct_vm.sender = a
    reject("SELF_ISSUANCE", contract.issue_attestation, a, "label", "scope")
    for bad in [Address(bytes(20)), "not-an-address", "0x1234", bytes(19)]:
        reject("INVALID_ADDRESS", contract.issue_attestation, bad, "label", "scope")
        reject("INVALID_ADDRESS", contract.create_space, "room", "scope", bad)
    direct_vm.sender = Address(bytes(20))
    reject("INVALID_ADDRESS", contract.issue_attestation, b, "label", "scope")
    assert contract.get_counts()["attestations"] == 0


def test_D05_revocation_issuer_only_irreversible(contract, direct_vm, actors, setup_room):
    _, rid = setup_room
    direct_vm.sender = actors[1]
    reject("ISSUER_ONLY", contract.revoke_attestation, rid)
    direct_vm.sender = actors[0]
    contract.revoke_attestation(rid)
    assert contract.get_attestation(rid)["revoked"] is True
    reject("ALREADY_REVOKED", contract.revoke_attestation, rid)
    assert not hasattr(contract, "unrevoke_attestation")


def test_D06_untrusted_issuer_before_boundary(contract, direct_vm, actors, setup_room, boundary):
    _, rid = setup_room
    sid = contract.create_space("Other", "React", actors[2])
    direct_vm.sender = actors[1]
    reject("UNTRUSTED_ISSUER", contract.apply_and_join, sid, rid)
    assert boundary[1] == []


def test_D07_wrong_holder_before_boundary(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    for actor in (actors[0], actors[2], actors[3]):
        direct_vm.sender = actor
        reject("HOLDER_ONLY", contract.apply_and_join, sid, rid)
    assert boundary[1] == []


def test_D08_revoked_root_before_boundary(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    contract.revoke_attestation(rid)
    direct_vm.sender = actors[1]
    reject("ROOT_REVOKED", contract.apply_and_join, sid, rid)
    assert boundary[1] == []


@pytest.mark.parametrize("bad", [0, -1, True, "1", 1 << 256])
def test_D09_invalid_ids(contract, direct_vm, actors, setup_room, boundary, bad, storage_image):
    sid, rid = setup_room
    direct_vm.sender = actors[1]
    before = storage_image()
    reject("INVALID_ID", contract.apply_and_join, bad, rid)
    reject("INVALID_ID", contract.apply_and_join, sid, bad)
    assert boundary[1] == []
    assert storage_image() == before


def test_D09_missing_ids(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    direct_vm.sender = actors[1]
    reject("SPACE_NOT_FOUND", contract.apply_and_join, 99, rid)
    reject("ATTESTATION_NOT_FOUND", contract.apply_and_join, sid, 99)
    reject("ATTESTATION_NOT_FOUND", contract.revoke_attestation, 99)
    assert boundary[1] == []


def test_D10_public_api_has_no_edit_or_grant_backdoor(contract, setup_room):
    from genlayer.py.get_schema import get_schema
    schema = get_schema(type(contract._instance))
    assert set(schema["methods"]) == {
        "create_space", "issue_attestation", "revoke_attestation", "apply_and_join",
        "post_room_note", "get_space", "get_attestation", "get_decision",
        "is_active_member", "get_room_notes", "get_counts",
    }
    assert "_semantic_decision" not in schema["methods"]
    before = contract.get_space(1)
    copy = contract.get_space(1)
    copy["required_scope"] = "anything"
    copy["trusted_issuer"] = "attacker"
    assert contract.get_space(1) == before


def test_D11_grant_bound_to_exact_holder_room_and_root(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    sid2 = contract.create_space("Two", "React", actors[0])
    assert join(contract, direct_vm, actors, sid, rid) == "ELIGIBLE"
    assert contract.get_decision(sid, actors[1]) == {
        "status": "FOUND", "space_id": sid, "holder": actors[1].as_hex,
        "root_attestation_id": rid, "decision": "ELIGIBLE",
    }
    assert contract.is_active_member(sid, actors[1]) is True
    assert not contract.is_active_member(sid2, actors[1])
    assert not contract.is_active_member(sid, actors[2])
    assert boundary[1] == [("Can build React components.", "Build React components.")]


def test_D12_explicit_denial_is_stored_without_posting(contract, direct_vm, actors, setup_room, boundary):
    boundary[0]["decision"] = "NOT_ELIGIBLE"
    sid, rid = setup_room
    assert join(contract, direct_vm, actors, sid, rid) == "NOT_ELIGIBLE"
    assert contract.get_decision(sid, actors[1])["decision"] == "NOT_ELIGIBLE"
    assert not contract.is_active_member(sid, actors[1])
    reject("ACTIVE_MEMBER_ONLY", contract.post_room_note, sid, "Denied")


@pytest.mark.parametrize("decision", ["ELIGIBLE", "NOT_ELIGIBLE"])
def test_D13_once_ever_even_new_root(contract, direct_vm, actors, setup_room, boundary, decision):
    sid, rid = setup_room
    rid2 = contract.issue_attestation(actors[1], "New", "React")
    boundary[0]["decision"] = decision
    join(contract, direct_vm, actors, sid, rid)
    for root in (rid, rid2):
        reject("DECISION_EXISTS", contract.apply_and_join, sid, root)
    assert len(boundary[1]) == 1
    assert contract.get_decision(sid, actors[1])["root_attestation_id"] == rid


def test_D14_revocation_changes_view_not_decision(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    join(contract, direct_vm, actors, sid, rid)
    before = contract.get_decision(sid, actors[1])
    direct_vm.sender = actors[0]
    contract.revoke_attestation(rid)
    assert not contract.is_active_member(sid, actors[1])
    assert contract.get_decision(sid, actors[1]) == before


def test_D15_active_member_and_attacker_posting(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    join(contract, direct_vm, actors, sid, rid)
    for attacker in (actors[0], actors[2]):
        direct_vm.sender = attacker
        reject("ACTIVE_MEMBER_ONLY", contract.post_room_note, sid, "Impersonation")
    direct_vm.sender = actors[1]
    assert contract.post_room_note(sid, "  Hello  ") == 1
    assert contract.get_room_notes(sid, 0, 20)["notes"] == [
        {"id": 1, "space_id": sid, "author": actors[1].as_hex, "text": "Hello"}
    ]


def test_D16_historical_notes_after_revocation(contract, direct_vm, actors, setup_room, boundary, storage_image):
    sid, rid = setup_room
    join(contract, direct_vm, actors, sid, rid)
    contract.post_room_note(sid, "History")
    history = contract.get_room_notes(sid, 0, 20)
    direct_vm.sender = actors[0]
    contract.revoke_attestation(rid)
    direct_vm.sender = actors[1]
    before = storage_image()
    reject("ACTIVE_MEMBER_ONLY", contract.post_room_note, sid, "New")
    assert storage_image() == before
    assert contract.get_room_notes(sid, 0, 20) == history


def test_D17_nonmember_denied_and_fake_flags(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    direct_vm.sender = actors[1]
    reject("ACTIVE_MEMBER_ONLY", contract.post_room_note, sid, "No decision")
    boundary[0]["decision"] = "NOT_ELIGIBLE"
    join(contract, direct_vm, actors, sid, rid)
    reject("ACTIVE_MEMBER_ONLY", contract.post_room_note, sid, "Denied")
    with pytest.raises(TypeError):
        contract.post_room_note(sid, "Override", eligible=True)


def test_D18_bounded_ordered_public_notes(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    join(contract, direct_vm, actors, sid, rid)
    for index in range(30):
        assert contract.post_room_note(sid, str(index)) == index + 1
    reject("SPACE_NOTE_LIMIT", contract.post_room_note, sid, "31st")
    direct_vm.sender = actors[3]  # Reads are public.
    first = contract.get_room_notes(sid, 0, 20)
    second = contract.get_room_notes(sid, first["next_offset"], 20)
    assert [n["id"] for n in first["notes"] + second["notes"]] == list(range(1, 31))
    assert first["total"] == 30 and second["next_offset"] == 30
    assert contract.get_room_notes(sid, 999999999, 20)["notes"] == []
    for offset, limit in [(-1, 20), (0, 0), (0, 21), (True, 1), (0, True)]:
        reject("INVALID_PAGINATION", contract.get_room_notes, sid, offset, limit)


def test_D19_admission_is_not_new_root(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    # Advance the room ID separately so a derived room/holder record has no
    # coincidentally corresponding root. Numeric root IDs refer ONLY to roots.
    sid2 = contract.create_space("Two", "React", actors[0])
    join(contract, direct_vm, actors, sid2, rid)
    decision = contract.get_decision(sid2, actors[1])
    assert contract.get_counts()["attestations"] == 1
    reject("INVALID_ID", contract.apply_and_join, sid, decision)
    reject("ATTESTATION_NOT_FOUND", contract.apply_and_join, sid, sid2)
    assert contract.get_decision(sid, actors[1])["status"] == "NO_DECISION"


def test_D20_unaccepted_consensus_and_no_frontend_result(contract, direct_vm, actors, setup_room, storage_image, monkeypatch):
    from genlayer import gl
    def unresolved(*args):
        raise gl.vm.UserError("UNACCEPTED_TEST_CONSENSUS")
    monkeypatch.setattr(gl.vm, "run_nondet_unsafe", unresolved)
    sid, rid = setup_room
    direct_vm.sender = actors[1]
    before = storage_image()
    reject("UNACCEPTED_TEST_CONSENSUS", contract.apply_and_join, sid, rid)
    with pytest.raises(TypeError):
        contract.apply_and_join(sid, rid, decision="ELIGIBLE")
    assert storage_image() == before
    assert not contract.is_active_member(sid, actors[1])
    assert contract.get_decision(sid, actors[1])["status"] == "NO_DECISION"


@pytest.mark.parametrize("result", ["", "UNKNOWN", "eligible", True, None, {"decision": "ELIGIBLE"}])
def test_D21_malformed_result_no_state_change(contract, direct_vm, actors, setup_room, boundary, storage_image, result):
    sid, rid = setup_room
    boundary[0]["decision"] = result
    direct_vm.sender = actors[1]
    before = storage_image()
    reject("INVALID_CONSENSUS_RESULT", contract.apply_and_join, sid, rid)
    assert storage_image() == before
    assert contract.get_counts()["decisions"] == 0


def test_D21_boundary_error_no_state_change(contract, direct_vm, actors, setup_room, boundary, storage_image):
    from genlayer import gl
    sid, rid = setup_room
    boundary[0]["error"] = gl.vm.UserError("UNDETERMINED_TEST_ONLY")
    direct_vm.sender = actors[1]
    before = storage_image()
    reject("UNDETERMINED_TEST_ONLY", contract.apply_and_join, sid, rid)
    assert storage_image() == before


def test_D22_same_root_new_room_independent_boundary(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    sid2 = contract.create_space("Security", "Audit authentication.", actors[0])
    join(contract, direct_vm, actors, sid, rid)
    boundary[0]["decision"] = "NOT_ELIGIBLE"
    assert join(contract, direct_vm, actors, sid2, rid) == "NOT_ELIGIBLE"
    assert contract.is_active_member(sid, actors[1])
    assert not contract.is_active_member(sid2, actors[1])
    assert boundary[1] == [
        ("Can build React components.", "Build React components."),
        ("Can build React components.", "Audit authentication."),
    ]


def test_D23_unambiguous_keys(contract, direct_vm, actors, setup_room, boundary):
    from genlayer import Address, u256
    _, rid = setup_room
    for index in range(2, 12):
        contract.create_space(str(index), "React", actors[0])
    join(contract, direct_vm, actors, 1, rid)
    boundary[0]["decision"] = "NOT_ELIGIBLE"
    join(contract, direct_vm, actors, 11, rid)
    assert contract.get_decision(1, actors[1])["decision"] == "ELIGIBLE"
    assert contract.get_decision(11, actors[1])["decision"] == "NOT_ELIGIBLE"
    assert contract.get_decision(1, actors[2])["status"] == "NO_DECISION"
    module = boundary[2]
    assert module._decision_key(u256(1), actors[1]) != module._decision_key(u256(11), actors[1])
    assert module._decision_key(u256(1), Address(actors[1].as_hex.lower())) == module._decision_key(u256(1), actors[1])


def test_D24_unknown_read_responses_do_not_write(contract, actors, storage_image):
    before = storage_image()
    assert contract.get_space(999) == {"status": "NOT_FOUND"}
    assert contract.get_attestation(999) == {"status": "NOT_FOUND"}
    assert contract.get_decision(999, actors[1]) == {"status": "NO_DECISION"}
    assert not contract.is_active_member(999, actors[1])
    assert contract.get_room_notes(999, 0, 20) == {
        "status": "NOT_FOUND", "notes": [], "total": 0, "next_offset": 0,
    }
    assert storage_image() == before


@pytest.mark.parametrize("method,field,max_bytes", [
    ("issue_attestation", "label", 80), ("issue_attestation", "source_scope", 320),
    ("post_room_note", "text", 240),
])
def test_text_limits_for_roots_and_notes(contract, direct_vm, actors, setup_room, boundary, method, field, max_bytes):
    sid, rid = setup_room
    join(contract, direct_vm, actors, sid, rid)
    for bad in ("", "  ", "\nValid", "\x7f", "a" * (max_bytes + 1)):
        if method == "issue_attestation":
            direct_vm.sender = actors[0]
            args = (actors[1], bad if field == "label" else "ok", bad if field == "source_scope" else "ok")
        else:
            direct_vm.sender = actors[1]
            args = (sid, bad)
        from genlayer import gl
        with pytest.raises(gl.vm.UserError):
            getattr(contract, method)(*args)


def test_exact_utf8_boundaries(contract, direct_vm, actors, boundary):
    direct_vm.sender = actors[0]
    sid = contract.create_space("界" * 26 + "aa", "界" * 106 + "aa", actors[0])
    rid = contract.issue_attestation(actors[1], "a" * 80, "a" * 320)
    join(contract, direct_vm, actors, sid, rid)
    assert contract.post_room_note(sid, "界" * 80) == 1
    reject("TEXT_TOO_LONG", contract.post_room_note, sid, "界" * 80 + "a")


def test_storage_roundtrip_new_instance(contract, direct_vm, actors, setup_room, boundary):
    sid, rid = setup_room
    join(contract, direct_vm, actors, sid, rid)
    contract.post_room_note(sid, "Persistent")
    cls = type(contract._instance)
    # Fresh SDK object over the same serialized storage; never rerun constructor.
    restored = cls.__new__(cls)
    restored._storage_slot = contract._instance._storage_slot
    restored._off = contract._instance._off
    restored.__type_desc__ = contract._instance.__type_desc__
    assert restored.get_space(sid) == contract.get_space(sid)
    assert restored.get_attestation(rid) == contract.get_attestation(rid)
    assert restored.get_decision(sid, actors[1]) == contract.get_decision(sid, actors[1])
    assert restored.get_room_notes(sid, 0, 20) == contract.get_room_notes(sid, 0, 20)
    assert restored.is_active_member(sid, actors[1])


def test_active_view_rechecks_every_binding(contract, direct_vm, actors, setup_room, boundary):
    from genlayer import u256
    sid, rid = setup_room
    join(contract, direct_vm, actors, sid, rid)
    key = boundary[2]._decision_key(u256(sid), actors[1])
    decision = contract.decisions_by_space_holder[key]
    decision.holder = actors[2]
    assert not contract.is_active_member(sid, actors[1])
    decision.holder = actors[1]
    decision.space_id = u256(2)
    assert not contract.is_active_member(sid, actors[1])
    decision.space_id = u256(sid)
    decision.root_attestation_id = u256(99)
    assert not contract.is_active_member(sid, actors[1])
    decision.root_attestation_id = u256(rid)
    root = contract.roots[u256(rid)]
    root.holder = actors[2]
    assert not contract.is_active_member(sid, actors[1])
    root.holder = actors[1]
    root.issuer = actors[3]
    assert not contract.is_active_member(sid, actors[1])


def test_production_custom_gate_has_no_test_flag(contract):
    tree = ast.parse(SOURCE.read_text())
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "NonTransitiveContextAdmissionV1")
    method = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "_semantic_decision")
    calls = [node for node in ast.walk(method) if isinstance(node, ast.Call)]
    assert sum(isinstance(node.func, ast.Attribute) and node.func.attr == "run_nondet_unsafe" for node in calls) == 1
    assert inspect.signature(contract.apply_and_join).parameters.keys() == {"space_id", "root_attestation_id"}
    assert "exec_prompt" in SOURCE.read_text()
    assert "CONSENSUS_NOT_IMPLEMENTED" not in SOURCE.read_text()
