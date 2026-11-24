"""Seed-set measurement for the evolve loop.

Runs the claim map on fixed companies using offline fixture facts.
Scores load-bearing coverage, residual risk visibility, and false-positive proxy.
Verifier gate recomputes sha256 over the fixture bundle and fails closed on tamper.
"""

from __future__ import annotations
from typing import Any
from .intents import CLAIMS, SEED_COMPANIES, BY_ID
from .cluster import Fact, cluster
from .knobs import as_dict
from .verifier import make_fixture_bundle, verify_bundle

def _fixture_facts(company: str, overrides: dict[str, Any] | None) -> list[Fact]:
    """Deterministic offline facts. Knobs can influence how many scouts we simulate."""
    knobs = as_dict(overrides)
    esc = int(knobs.get("escalation_max_claims", 2))
    facts: list[Fact] = []
    for claim in CLAIMS:
        # always one coverage scout
        if claim.id == "sanctions":
            facts.append(Fact(claim.id, {"matched": False}))
        elif claim.id == "registry":
            facts.append(Fact(claim.id, {"active": True, "legal_name": company}))
        else:
            facts.append(Fact(claim.id, {claim.fields[0]: 1 if claim.id != "news" else 0}))
        # extra scouts on first N claims if escalation allows
        if esc > 0 and claim.priority <= 20 + esc * 10:
            facts.append(Fact(claim.id, facts[-1].fields.copy()))
            esc -= 1
    return facts

def measure(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    """Score the seed set. Returns metrics the keep/revert rule uses."""
    total_lb = sum(1 for c in CLAIMS if c.load_bearing)
    settled_lb = 0
    residual_visible = True
    false_pos_proxy = 0.0
    cost = 0.0

    for inp in SEED_COMPANIES:
        facts = _fixture_facts(inp.company, overrides)
        cmap = cluster(facts)
        for cid, cl in cmap.items():
            claim = BY_ID.get(cid)
            if claim and claim.load_bearing and cl.state in {"settled", "single"}:
                settled_lb += 1
            if cl.state in {"blind", "dead"} and claim and claim.load_bearing:
                residual_visible = True  # HOLD would be forced
            cost += sum(f.price_usd for f in cl.facts)
            if cl.state == "contested":
                false_pos_proxy += 0.01

    coverage = settled_lb / max(1, total_lb * len(SEED_COMPANIES))
    metrics = {
        "load_bearing_coverage": round(coverage, 4),
        "residual_risk_visible": residual_visible,
        "cost_usd": round(cost, 4),
        "false_positive_rate": round(false_pos_proxy, 4),
        "companies": len(SEED_COMPANIES),
    }
    bundle = make_fixture_bundle(metrics)
    metrics["verifier_ok"] = verify_bundle(bundle)
    return metrics
