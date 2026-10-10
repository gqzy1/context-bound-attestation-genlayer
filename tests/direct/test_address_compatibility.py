"""Pinned SDK calldata regression; public addresses only, no chain calls."""
import sys

import pytest

A = "0xEB56F245EFEceD0899b7e23697FeE512a39DBdCc"
B = "0x5EDb6E65aaEA10A7B3CC34e8d5724e41D1f6da84"


def test_integer_issue_calldata(contract, direct_vm):
    from genlayer import Address, gl
    from genlayer.py import calldata
    direct_vm.sender = Address(A)
    envelope = calldata.decode(calldata.encode({"method": "issue_attestation", "args": [int(B, 16), "React", "Can build React components."]}))
    assert type(envelope["args"][0]) is int
    assert gl.message.sender_address == Address(A)
    assert isinstance(gl.message.sender_address, Address)
    rid = contract.issue_attestation(*envelope["args"])
    assert contract.get_attestation(rid)["holder"] == Address(B).as_hex
    assert contract.get_attestation(rid)["issuer"] == Address(A).as_hex


def module(contract):
    return sys.modules[type(contract._instance).__module__]


def represented(hex_address, kind):
    import base64
    from genlayer import Address
    raw = bytes.fromhex(hex_address[2:])
    return {
        "Address": lambda: Address(raw), "int": lambda: int(hex_address, 16),
        "bytes": lambda: raw, "str": lambda: hex_address,
        "lower": lambda: hex_address.lower(), "upper": lambda: "0x" + hex_address[2:].upper(),
        "base64": lambda: base64.b64encode(raw).decode("ascii"),
        "bytearray": lambda: bytearray(raw), "memoryview": lambda: memoryview(raw),
    }[kind]()


@pytest.mark.parametrize("hex_address", [A, B])
@pytest.mark.parametrize("kind", ["Address", "int", "bytes", "str", "lower", "upper", "base64", "bytearray", "memoryview"])
def test_safe_boundary_normalizes_sdk_representations(contract, hex_address, kind):
    from genlayer import Address
    normalized = module(contract)._address(represented(hex_address, kind))
    assert type(normalized) is Address
    assert normalized == Address(hex_address)


@pytest.mark.parametrize("bad", [
    0, -1, -(1 << 160), 1 << 160, (1 << 160) + 1, True, False,
    b"", bytes(19), bytes(21), bytes(20), bytearray(20), memoryview(bytes(20)),
    "0x" + "0" * 40, "0x" + "1" * 39, "0x" + "1" * 41,
    "0x" + "g" * 40, "0X" + "1" * 40, " " + A, A + " ",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAA=", "not-an-address", "é" * 28,
    "AQEBAQEBAQEBAQEBAQEBAQEBAQE=!", "AQEBAQEBAQEBAQEBAQEBAQEBAQE", 
    "AQEBAQEBAQEBAQEBAQEBAQEBAQF=", 1.0, None, [], {},
])
def test_safe_boundary_rejects_invalid(contract, bad):
    from genlayer import gl
    with pytest.raises(gl.vm.UserError, match="INVALID_ADDRESS"):
        module(contract)._address(bad)


@pytest.mark.parametrize("value", [1, (1 << 160) - 1])
def test_integer_range_endpoints(contract, value):
    assert module(contract)._address(value).as_bytes == value.to_bytes(20, "big")


@pytest.mark.parametrize("kind", ["Address", "int", "bytes", "str", "lower", "upper", "base64"])
def test_all_public_address_entries_and_authorization(contract, direct_vm, boundary, kind):
    from genlayer import Address, gl
    direct_vm.sender = Address(A)
    sid = contract.create_space("React room", "Build React components.", represented(A, kind))
    rid = contract.issue_attestation(represented(B, kind), "React", "Can build React components.")
    assert contract.get_decision(sid, represented(B, kind)) == {"status": "NO_DECISION"}
    assert not contract.is_active_member(sid, represented(B, kind))
    with pytest.raises(gl.vm.UserError, match="SELF_ISSUANCE"):
        contract.issue_attestation(represented(A, kind), "React", "scope")
    with pytest.raises(gl.vm.UserError, match="HOLDER_ONLY"):
        contract.apply_and_join(sid, rid)
    direct_vm.sender = Address(B)
    with pytest.raises(gl.vm.UserError, match="ISSUER_ONLY"):
        contract.revoke_attestation(rid)
    # TEST ONLY scripted deterministic boundary, not a real model/consensus.
    assert contract.apply_and_join(sid, rid) == "ELIGIBLE"
    assert contract.get_decision(sid, represented(B, kind))["decision"] == "ELIGIBLE"
    assert contract.is_active_member(sid, represented(B, kind))
    contract.post_room_note(sid, "Offline protected note")
    direct_vm.sender = Address(A)
    with pytest.raises(gl.vm.UserError, match="ACTIVE_MEMBER_ONLY"):
        contract.post_room_note(sid, "Unauthorized")
    contract.revoke_attestation(rid)
    assert not contract.is_active_member(sid, represented(B, kind))
    direct_vm.sender = Address(B)
    with pytest.raises(gl.vm.UserError, match="ACTIVE_MEMBER_ONLY"):
        contract.post_room_note(sid, "Revoked")
    assert contract.get_counts() == dict(spaces=1, attestations=1, decisions=1, notes=1)


@pytest.mark.parametrize("bad", [0, -1, 1 << 160, True, False, bytes(19), bytes(21), bytes(20), "0x1234", None])
def test_invalid_wire_values_all_public_entries_are_atomic(contract, direct_vm, storage_image, bad):
    from genlayer import Address, gl
    direct_vm.sender = Address(A)
    # get_decision validates the address even for an uncreated positive space ID.
    operations = [lambda: contract.issue_attestation(bad, "label", "scope"),
                  lambda: contract.create_space("room", "scope", bad),
                  lambda: contract.get_decision(1, bad),
                  lambda: contract.is_active_member(1, bad)]
    for operation in operations:
        before = storage_image()
        with pytest.raises(gl.vm.UserError, match="INVALID_ADDRESS"):
            operation()
        assert storage_image() == before
    assert contract.get_counts() == dict(spaces=0, attestations=0, decisions=0, notes=0)


@pytest.mark.parametrize("vector_index", range(8))
def test_real_javascript_to_python_calldata_vectors(contract, direct_vm, vector_index):
    import json
    from pathlib import Path
    from genlayer import Address
    from genlayer.py import calldata
    vectors = json.loads((Path(__file__).parents[2] / "evidence/phase4b/js-calldata.json").read_text())
    assert vectors["sdk"] == "genlayer-js 1.1.8"
    vector = vectors["cases"][vector_index]
    envelope = calldata.decode(bytes.fromhex(vector["calldataHex"]))
    value = envelope["args"][0]
    expected_type = {"Address": Address, "int": int, "bytes": bytes, "str": str}[vector["representation"]]
    assert type(value) is expected_type
    # Swap issuer to exercise both actual public wallets without self-issuance.
    issuer = B if vector["wallet"] == "A" else A
    direct_vm.sender = Address(issuer)
    rid = getattr(contract, envelope["method"])(*envelope["args"])
    assert contract.get_attestation(rid)["holder"] == Address(vector["hex"]).as_hex
    assert contract.get_attestation(rid)["issuer"] == Address(issuer).as_hex


def test_sdk_integer_byte_order_is_not_inferred(contract):
    from genlayer import Address
    addr = Address(B)
    assert addr.as_int == int.from_bytes(addr.as_bytes, "little")
    assert int(B, 16) != addr.as_int
    assert module(contract)._address(int(B, 16)) == addr
    # The boundary never guesses an account from a reversed numeric value.
    assert module(contract)._address(addr.as_int) != addr
