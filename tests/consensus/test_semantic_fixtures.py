"""S fixtures are frozen EXPECTATIONS and scripted model outputs, not LLM results."""
import json
from pathlib import Path

import pytest


PLAN = Path(__file__).parents[2] / "architecture-freeze-v1/04_TEST_ACCEPTANCE_PLAN.md"
FIXTURES = []
for line in PLAN.read_text().splitlines():
    if line.startswith("| S"):
        case, source, target, expected = [part.strip() for part in line.split("|")[1:-1]]
        FIXTURES.append((case, source, target, expected.split(" ", 1)[0]))
assert len(FIXTURES) == 20


@pytest.mark.parametrize("case,source,target,expected", FIXTURES, ids=[x[0] for x in FIXTURES])
@pytest.mark.parametrize("agree", [True, False], ids=["scripted-agreement", "scripted-disagreement"])
def test_S_original_data_transport_and_independent_mock_comparison(
    contract, direct_vm, actors, consensus_gate, storage_image, case, source, target, expected, agree
):
    from genlayer import gl
    direct_vm.sender = actors[0]
    sid = contract.create_space(case, target, actors[0])
    rid = contract.issue_attestation(actors[1], case, source)
    # Explicit fixture scripts: NOT predictions or measured model classification.
    other = expected if agree else ("NOT_ELIGIBLE" if expected == "ELIGIBLE" else "ELIGIBLE")
    consensus_gate.configure(
        source, target, json.dumps({"decision": expected}), json.dumps({"decision": other})
    )
    direct_vm.sender = actors[1]
    before = storage_image()
    if agree:
        assert contract.apply_and_join(sid, rid) == expected
        assert contract.is_active_member(sid, actors[1]) is (expected == "ELIGIBLE")
    else:
        with pytest.raises(gl.vm.UserError, match="SIMULATED_DISAGREEMENT"):
            contract.apply_and_join(sid, rid)
        assert storage_image() == before
        assert contract.get_decision(sid, actors[1]) == {"status": "NO_DECISION"}
    assert [x["role"] for x in consensus_gate.calls] == ["leader", "validator-1"]
    for call in consensus_gate.calls:
        prompt = call["prompt"]
        transported_source = json.loads(prompt.split("<SOURCE_SCOPE_DATA>\n", 1)[1].split("\n</SOURCE_SCOPE_DATA>", 1)[0])
        transported_target = json.loads(prompt.split("<TARGET_REQUIREMENT_DATA>\n", 1)[1].split("\n</TARGET_REQUIREMENT_DATA>", 1)[0])
        assert transported_source == source and transported_target == target
    assert not consensus_gate.outputs  # Both scripts consumed independently.
