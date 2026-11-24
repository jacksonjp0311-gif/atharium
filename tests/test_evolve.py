"""Basic test that the evolve loop runs and records outcomes."""

from colony.evolve import evolve_once

def test_evolve_once_runs():
    state = {"overrides": {}, "outcomes": []}
    result = evolve_once(state)
    assert "outcomes" in result
    assert len(result["outcomes"]) >= 1
