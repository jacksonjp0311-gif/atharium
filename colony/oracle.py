"""Oracle kill rule.

Machine-checkable conditions that void a candidate keep.
Fitness alone never decides. These rules sit outside the mutation set.
"""

from __future__ import annotations

from typing import Any


def oracle_kill(trial: dict[str, Any], baseline: dict[str, Any]) -> str | None:
    """Return a reason string if the keep must be voided, else None."""
    if not trial.get("verifier_ok") or not baseline.get("verifier_ok"):
        return "verifier_failed"
    if not trial.get("residual_risk_visible"):
        return "residual_risk_hidden"
    # coverage must not drop
    if trial.get("load_bearing_coverage", 0) < baseline.get("load_bearing_coverage", 0) - 0.001:
        return "coverage_regressed"
    # false-positive proxy must not rise
    if trial.get("false_positive_rate", 0) > baseline.get("false_positive_rate", 0) + 0.001:
        return "false_positive_rose"
    # cost must not explode
    if trial.get("cost_usd", 0) > baseline.get("cost_usd", 0) * 1.5 + 0.01:
        return "cost_exploded"
    return None
