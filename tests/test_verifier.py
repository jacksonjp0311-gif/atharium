"""Verifier fails closed."""

from colony.verifier import make_fixture_bundle, verify_bundle


def test_verifier_ok_on_fixture():
    m = {"companies": 2, "load_bearing_coverage": 1.0, "residual_risk_visible": True, "cost_usd": 0.1, "false_positive_rate": 0.0}
    bundle = make_fixture_bundle(m)
    assert verify_bundle(bundle)


def test_verifier_fails_on_tamper():
    m = {"companies": 2, "load_bearing_coverage": 1.0, "residual_risk_visible": True, "cost_usd": 0.1, "false_positive_rate": 0.0}
    bundle = make_fixture_bundle(m)
    bundle["load_bearing_coverage"] = 0.5  # tamper
    assert not verify_bundle(bundle)
