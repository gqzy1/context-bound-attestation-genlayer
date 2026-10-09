"""Offline Phase 1/2 fixtures. No integration/network fixtures are used."""
import socket
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def forbid_network(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("Offline tests must not connect to any network")
    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)


@pytest.fixture
def contract(direct_deploy):
    return direct_deploy(
        str(Path(__file__).parents[1] / "contracts/context_bound_attestation.py"),
        sdk_version="v0.2.16",
    )


@pytest.fixture
def actors(contract):
    # SDK must be loaded before constructing typed addresses. gltest's address
    # factory may otherwise return bytes during first initialization.
    from genlayer import Address
    return tuple(Address(bytes([i]) * 20) for i in (1, 2, 3, 4))


@pytest.fixture
def setup_room(contract, direct_vm, actors):
    issuer, holder, _, _ = actors
    direct_vm.sender = issuer
    sid = contract.create_space("React room", "Build React components.", issuer)
    rid = contract.issue_attestation(holder, "React scope", "Can build React components.")
    return sid, rid


@pytest.fixture
def boundary(contract, monkeypatch):
    """TEST ONLY: isolate deterministic core from consensus, never public API.

    The production source contains no mock switch or admin grant method.
    This exercises prechecks and deterministic post-consensus persistence,
    without claiming semantic evaluation, validator consensus or live finality.
    """
    import sys
    cls = type(contract._instance)
    module = sys.modules[cls.__module__]
    calls = []
    response = {"decision": "ELIGIBLE", "error": None}

    def test_boundary(self, source_scope, required_scope):
        calls.append((source_scope, required_scope))
        if response["error"] is not None:
            raise response["error"]
        return response["decision"]

    monkeypatch.setattr(cls, "_semantic_decision", test_boundary)
    return response, calls, module


@pytest.fixture
def storage_image(direct_vm):
    """Byte-level state image. No artificial revert/rollback masks mutations."""
    def capture():
        # Direct VM materializes/zero-extends slots on reads. Canonicalize those
        # implicit zero bytes so reads are not confused with persistent writes.
        return {key: value.rstrip(b"\0") for key, value in direct_vm._storage.snapshot().items() if any(value)}
    return capture
