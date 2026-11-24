"""Tests for closed knob set."""

from colony.knobs import KNOBS, as_dict, get_knob

def test_knobs_closed():
    assert "escalation_max_claims" in KNOBS
    assert "gap_escalation_boost" in KNOBS

def test_as_dict_defaults():
    d = as_dict()
    assert d["escalation_max_claims"] == 2

def test_override():
    d = as_dict({"escalation_max_claims": 3})
    assert d["escalation_max_claims"] == 3
