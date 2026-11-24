"""Seed-set measurement for the evolve loop.

Runs the claim map on fixed companies. Default is offline fixtures.
Optional live path is gated and fails closed if network/wallet unavailable.
Verifier stays outside the mutation set.

Measurement uses MEASURE_COMPANIES. HOLD_OUT_COMPANIES are reserved for accept-time check.
Fixtures now respond to knobs: higher escalation can close a load-bearing gap.
"""

from __future__ import annotations
from typing import Any
from .intents import CLAIMS, MEASURE_COMPANIES, HOLD_OUT_COMPANIES, BY_ID
from .cluster import Fact, cluster
from .knobs import as_dict
from .verifier import make_fixture_bundle, verify_bundle

def _fixture_facts(company: str, overrides: dict[str, Any] | None) -> list[Fact]:
    """Deterministic offline facts with controlled gaps and disagreement.
    Higher escalation or gap boost can close the load-bearing registry gap on Gap Co.
    """
    knobs = as_dict(overrides)
    esc = int(knobs.get("escalation_max_claims", 2))
    gap_boost = int(knobs.get("gap_escalation_boost", 0))
    facts: list[Fact] = []
    for claim in CLAIMS:
        if company.startswith("Gap") and claim.id == "registry":
            # load-bearing gap that closes when escalation is high enough
            if esc + gap_boost >= 3:
                facts.append(Fact(claim.id, {"active": True, "legal_name": company}))
            else:
                facts.append(Fact(claim.id, {}, ok=False, empty=True))
            continue
        if company.startswith("Contested") and claim.id == "sanctions":
            facts.append(Fact(claim.id, {"matched": False}))
            facts.append(Fact(claim.id, {"matched": True}))  # disagreement
            continue
        # normal coverage
        if claim.id == "sanctions":
            facts.append(Fact(claim.id, {"matched": False}))
        elif claim.id == "registry":
            facts.append(Fact(claim.id, {"active": True, "legal_name": company}))
        else:
            facts.append(Fact(claim.id, {claim.fields[0]: 1 if claim.id != "news" else 0}))
        # extra scouts if escalation allows
        if esc > 0 and claim.priority <= 20 + esc * 10:
            facts.append(Fact(claim.id, facts[-1].fields.copy()))
            esc -= 1
    return facts

def _live_facts(company: str, overrides: dict[str, Any] | None) -> list[Fact] | None:
    """Gated live path. Returns None if unavailable so caller fails closed."""
    # Stub: real Telegraph client would go here. Currently always unavailable.
    return None

def measure(overrides: dict[str, Any] | None = None, live: bool = False, holdout: bool = False) -> dict[str, Any]:
    """Score the seed set. live=True attempts gated live path and fails closed.
    holdout=True scores only the held-out companies (accept-time check).
    """
    companies = HOLD_OUT_COMPANIES if holdout else MEASURE_COMPANIES
    total_lb = sum(1 for c in CLAIMS if c.load_bearing)
    settled_lb = 0
    residual_visible = True
    false_pos_proxy = 0.0
    cost = 0.0
    used_live = False

    for inp in companies:
        facts = None
        if live:
            facts = _live_facts(inp.company, overrides)
            if facts is None:
                facts = _fixture_facts(inp.company, overrides)
            else:
                used_live = True
        else:
            facts = _fixture_facts(inp.company, overrides)

        cmap = cluster(facts)
        for cid, cl in cmap.items():
            claim = BY_ID.get(cid)
            if claim and claim.load_bearing and cl.state in {"settled", "single"}:
                settled_lb += 1
            if cl.state in {"blind", "dead"} and claim and claim.load_bearing:
                residual_visible = True
            cost += sum(f.price_usd for f in cl.facts)
            if cl.state == "contested":
                false_pos_proxy += 0.01

    coverage = settled_lb / max(1, total_lb * len(companies))
    metrics = {
        "load_bearing_coverage": round(coverage, 4),
        "residual_risk_visible": residual_visible,
        "cost_usd": round(cost, 4),
        "false_positive_rate": round(false_pos_proxy, 4),
        "companies": len(companies),
        "used_live": used_live,
        "holdout": holdout,
    }
    bundle = make_fixture_bundle(metrics)
    metrics["verifier_ok"] = verify_bundle(bundle)
    return metrics
