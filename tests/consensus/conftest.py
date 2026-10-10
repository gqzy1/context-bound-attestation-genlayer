"""Test-only synchronous executor, never shipped as contract consensus.

The pinned Direct Mode shim returns immediately after Leader. This fixture
replaces ONLY that shim and executes actual production callbacks before return.
It never changes/restores storage to hide mutations. LLM calls traverse the
real pinned SDK and WASI mock with strictly scripted offline outputs.
"""
import json
import hashlib
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def module(contract):
    return sys.modules[type(contract._instance).__module__]


@pytest.fixture
def consensus_gate(contract, module, direct_vm, monkeypatch, storage_image, request):
    from genlayer import gl
    from gltest.direct import wasi_mock
    # Direct Mode omits this transitive runner from sys.path. Use the exact
    # Phase 0 locked runner, extracted by prepare_direct_sdk.py, not pip latest.
    pinned = Path.home() / ".cache/gltest-direct/extracted/v0.2.16/py-lib-cloudpickle/1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd/src"
    assert (pinned / "cloudpickle/__init__.py").is_file(), "Run scripts/prepare_direct_sdk.py first"
    monkeypatch.syspath_prepend(str(pinned))
    import cloudpickle
    assert Path(cloudpickle.__file__).is_relative_to(pinned)
    control = SimpleNamespace(
        outputs=[], calls=[], validators=1, votes=[], stage="", prompts=[],
        unresolved=False, leader_override=None, envelope=None, callbacks=None,
        source=None, target=None, serializable_callbacks=0,
    )
    original_handler = wasi_mock._handle_llm_request

    def handle(vm, data):
        assert data["response_format"] == "text"
        assert data.get("images", []) == []
        control.calls.append({"role": control.stage, "prompt": data["prompt"]})
        return original_handler(vm, data)

    def scripted(prompt):
        assert control.outputs, "Unexpected or unmocked model invocation"
        assert prompt == control.prompts[0], "Not the exact frozen original-input prompt"
        output = control.outputs.pop(0)
        if isinstance(output, Exception):
            raise output
        # Work around genlayer-test 0.29.2 auto-JSON parsing even in text mode:
        # wrapping the raw text as a JSON string returns the original raw bytes.
        # The production raw JSON parser remains exercised (including duplicates).
        return json.dumps(output, ensure_ascii=False)

    def run(leader, validator, /):
        before = storage_image()
        control.callbacks = (leader, validator)
        # Exact production callbacks capture only the prompt, not self/storage.
        for callback in (leader, validator):
            assert [cell.cell_contents for cell in callback.__closure__] == control.prompts
            assert cloudpickle.dumps(callback)
            control.serializable_callbacks += 1
        direct_vm._in_nondet = True
        try:
            control.stage = "leader"
            result = leader()
            assert storage_image() == before, "Leader mutated persistent state"
            candidate = result if control.leader_override is None else control.leader_override
            wrapped = gl.vm.Return(candidate) if control.envelope is None else control.envelope
            direct_vm._captured_validators.append((candidate, leader, validator))
            for index in range(control.validators):
                control.stage = "validator-" + str(index + 1)
                vote = validator(wrapped)
                assert type(vote) is bool
                control.votes.append(vote)
                assert storage_image() == before, "Validator mutated persistent state"
                if not vote:
                    raise gl.vm.UserError("SIMULATED_DISAGREEMENT")
            if control.unresolved:
                raise gl.vm.UserError("SIMULATED_UNDETERMINED")
            assert not control.outputs, "A scripted independent evaluation was skipped"
            return candidate
        finally:
            direct_vm._in_nondet = False

    monkeypatch.setattr(wasi_mock, "_handle_llm_request", handle)
    monkeypatch.setattr(direct_vm, "_match_llm_mock", scripted)
    monkeypatch.setattr(gl.vm, "run_nondet_unsafe", run)
    direct_vm._strict_mock_mode = True

    def configure(source, target, *outputs, validators=1):
        control.source, control.target = source, target
        control.prompts[:] = [module._render_prompt(source, target)]
        control.outputs[:] = list(outputs)
        control.validators = validators
        return control

    control.configure = configure
    yield control
    # Optional evidence recording, all measured from actual offline callbacks.
    # No real-model classification or real-network vote is claimed.
    if destination := os.environ.get("CONTEXTPASS_TRACE_FILE"):
        path = Path(destination)
        trace = json.loads(path.read_text()) if path.exists() else []
        trace.append({
            "test": request.node.nodeid, "mode": "offline_scripted_only",
            "source": control.source, "target": control.target,
            "model_calls": [
                {"role": call["role"], "prompt_sha256": hashlib.sha256(call["prompt"].encode()).hexdigest()}
                for call in control.calls
            ],
            "votes": control.votes, "serializable_callbacks": control.serializable_callbacks,
        })
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(trace, ensure_ascii=False, indent=2) + "\n")


@pytest.fixture
def petition(contract, direct_vm, actors, setup_room, consensus_gate):
    sid, rid = setup_room
    consensus_gate.configure(
        contract.get_attestation(rid)["source_scope"],
        contract.get_space(sid)["required_scope"],
        '{"decision":"ELIGIBLE"}', '{"decision":"ELIGIBLE"}',
    )
    direct_vm.sender = actors[1]
    return sid, rid
