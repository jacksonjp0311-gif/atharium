"""Tests for Oracle kill rules."""

from colony.oracle import oracle_kill

def test_oracle_kill_coverage_drop():
    baseline = {"verifier_ok": True, "load_bearing_coverage": 0.8, "false_positive_rate": 0.0, "cost_usd": 0.1, "residual_risk_visible": True}
    trial = {"verifier_ok": True, "load_bearing_coverage": 0.6, "false_positive_rate": 0.0, "cost_usd": 0.1, "residual_risk_visible": True}
    assert oracle_kill(trial, baseline) == "coverage_regressed"

def test_oracle_no_kill_on_equal():
    m = {"verifier_ok": True, "load_bearing_coverage": 0.8, "false_positive_rate": 0.0, "cost_usd": 0.1, "residual_risk_visible": True}
    assert oracle_kill(m, m) is None

def test_oracle_kill_fp_rise():
    baseline = {"verifier_ok": True, "load_bearing_coverage": 0.8, "false_positive_rate": 0.0, "cost_usd": 0.1, "residual_risk_visible": True}
    trial = {"verifier_ok": True, "load_bearing_coverage": 0.8, "false_positive_rate": 0.02, "cost_usd": 0.1, "residual_risk_visible": True}
    assert oracle_kill(trial, baseline) == "false_positive_rose"
