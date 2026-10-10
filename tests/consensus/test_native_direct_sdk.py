"""Separate native Direct Mode callback capture smoke; no admission persistence."""
import json
import re

import pytest


def test_native_sdk_captures_and_reruns_real_validator(contract, module, direct_vm):
    source, target = "Can build React components.", "Build React components."
    prompt = module._render_prompt(source, target)
    exact = "^" + re.escape(prompt) + "$"
    direct_vm.mock_llm(exact, json.dumps('{"decision":"ELIGIBLE"}'))
    assert contract._instance._semantic_decision(source, target) == "ELIGIBLE"
    assert len(direct_vm._captured_validators) == 1
    direct_vm.clear_mocks()
    direct_vm.mock_llm(exact, json.dumps('{"decision":"NOT_ELIGIBLE"}'))
    assert direct_vm.run_validator() is False
    direct_vm.clear_mocks()
    direct_vm.mock_llm(exact, json.dumps('{"decision":"ELIGIBLE"}'))
    assert direct_vm.run_validator() is True
    assert contract.get_counts()["decisions"] == 0


@pytest.mark.parametrize("raw", [None, True, 1, {}, {"decision": "ELIGIBLE"}])
def test_wrong_sdk_text_return_rejects(module, raw):
    from genlayer import gl
    with pytest.raises(gl.vm.UserError, match="INVALID_CONSENSUS_RESULT"):
        module._parse_output(raw)
