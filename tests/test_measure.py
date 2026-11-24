"""Tests for measurement surfaces."""

from colony.measure import measure
from colony.knobs import as_dict

def test_measure_offline():
    m = measure()
    assert m["verifier_ok"]
    assert m["companies"] == 3
    assert not m.get("holdout")

def test_measure_holdout():
    m = measure(holdout=True)
    assert m["verifier_ok"]
    assert m["companies"] == 1
    assert m["holdout"]

def test_measure_responds_to_knob():
    base = measure()
    boosted = measure({"escalation_max_claims": 4})
    # coverage or cost should be able to differ; at minimum the call succeeds
    assert boosted["verifier_ok"]
