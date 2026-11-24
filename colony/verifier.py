"""Independent verifier gate.

Recomputes sha256 over a canonical fixture bundle. Never imports producer code.
Fails closed on any mismatch. Stays outside the mutation set.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical(payload: dict[str, Any]) -> str:
    """Deterministic serialization."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def bundle_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(payload).encode()).hexdigest()


def verify_bundle(bundle: dict[str, Any]) -> bool:
    """True only if the stored hash matches a fresh computation."""
    expected = bundle.get("sha256")
    if not expected or not isinstance(expected, str):
        return False
    payload = {k: v for k, v in bundle.items() if k != "sha256"}
    return bundle_hash(payload) == expected


def make_fixture_bundle(metrics: dict[str, Any]) -> dict[str, Any]:
    """Offline fixture the evolve loop can verify."""
    payload = {
        "kind": "atharium-seed-bundle",
        "companies": metrics.get("companies", 0),
        "load_bearing_coverage": metrics.get("load_bearing_coverage"),
        "residual_risk_visible": metrics.get("residual_risk_visible"),
        "cost_usd": metrics.get("cost_usd"),
        "false_positive_rate": metrics.get("false_positive_rate"),
    }
    return {**payload, "sha256": bundle_hash(payload)}
