"""Atharium evolve — recursive learning under twin control + Oracle.

Sleep/awake cycle entry point. Measures current knobs against the claim map
on a fixed seed set, proposes one closed-set mutation, re-measures, keeps only
when trial is strictly better, twin does not lead, and Oracle does not kill.
Outcomes are append-only. Verifier stays outside the mutation set.

Not AGI. Human authorize still required for durable accepts.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .knobs import KNOBS, as_dict
from .measure import measure
from .oracle import oracle_kill

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SOCIETY = ROOT / "society"


def _ensure() -> None:
    for p in (DATA, SOCIETY):
        p.mkdir(parents=True, exist_ok=True)


def run_seed(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    """Real seed-set measurement against the claim map."""
    m = measure(overrides)
    m["knobs"] = as_dict(overrides)
    m["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return m


def propose(current: dict[str, Any]) -> tuple[str, Any] | None:
    """Closed-set proposal. Cycles through safe knobs."""
    order = ["escalation_max_claims", "single_source_penalty", "coverage_priority_boost"]
    for name in order:
        knob = KNOBS[name]
        val = current.get(name, knob.default)
        if isinstance(val, (int, float)) and val < (knob.max_val or val):
            return name, val + 1
    return None


def better(trial: dict[str, Any], baseline: dict[str, Any]) -> bool:
    if not trial.get("verifier_ok") or not baseline.get("verifier_ok"):
        return False
    if trial["load_bearing_coverage"] > baseline["load_bearing_coverage"] and trial["cost_usd"] <= baseline["cost_usd"] + 0.001:
        return True
    if trial["false_positive_rate"] < baseline["false_positive_rate"] and trial["load_bearing_coverage"] >= baseline["load_bearing_coverage"] - 0.001:
        return True
    return False


def evolve_once(state: dict[str, Any]) -> dict[str, Any]:
    baseline = run_seed(state.get("overrides"))
    proposal = propose(baseline["knobs"])
    if not proposal:
        state.setdefault("outcomes", []).append({"result": "no_proposal", "ts": baseline["timestamp"]})
        return state

    name, new_val = proposal
    trial_ov = dict(state.get("overrides") or {})
    trial_ov[name] = new_val
    trial = run_seed(trial_ov)
    control = run_seed({})  # twin: frozen defaults

    kill = oracle_kill(trial, baseline)
    kept = better(trial, baseline) and not better(control, trial) and kill is None
    outcome = {
        "ts": baseline["timestamp"],
        "knob": name,
        "from": baseline["knobs"].get(name),
        "to": new_val,
        "kept": kept,
        "oracle_kill": kill,
        "baseline_coverage": baseline["load_bearing_coverage"],
        "trial_coverage": trial["load_bearing_coverage"],
        "control_coverage": control["load_bearing_coverage"],
        "baseline_fp": baseline["false_positive_rate"],
        "trial_fp": trial["false_positive_rate"],
    }
    state.setdefault("outcomes", []).append(outcome)
    if kept:
        state.setdefault("overrides", {})[name] = new_val
        state.setdefault("keeps", []).append(name)
    else:
        state.setdefault("reverts", []).append(name)
    return state


def write_learning(state: dict[str, Any]) -> None:
    outcomes = state.get("outcomes", [])
    keeps = sum(1 for o in outcomes if o.get("kept"))
    reverts = sum(1 for o in outcomes if o.get("kept") is False and "knob" in o)
    lines = [
        "# Atharium learning loop",
        "",
        "Recursive: each cycle proposes one closed-set mutation, measures against the claim map on a fixed seed set, and keeps only when trial beats baseline *and* twin control does not lead *and* Oracle does not kill.",
        "",
        f"- Outcomes recorded: **{len(outcomes)}**",
        f"- Kept: **{keeps}**",
        f"- Reverted: **{reverts}**",
        "",
        "Fitness alone never decides. Verifier stays outside the mutation set. Human authorize still required for durable accepts.",
        "",
        "Not AGI. Not novel theorem discovery.",
        "",
        "## Recent",
    ]
    for o in outcomes[-8:]:
        if "knob" in o:
            status = "kept" if o.get("kept") else "reverted"
            kill = f" oracle:{o.get('oracle_kill')}" if o.get("oracle_kill") else ""
            lines.append(f"- `{status}` · `{o['knob']}` {o.get('from')} → {o.get('to')} · cov {o.get('baseline_coverage')} → {o.get('trial_coverage')}{kill}")
        else:
            lines.append(f"- {o.get('result')}")
    (SOCIETY / "LEARNING.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    p = argparse.ArgumentParser(description="Atharium evolve — sleep/awake recursive learning")
    p.add_argument("--cycles", type=int, default=1)
    p.add_argument("--offline", default="true")
    p.add_argument("--status", action="store_true")
    args = p.parse_args()

    _ensure()
    path = DATA / "evolve_state.json"
    state: dict[str, Any] = json.loads(path.read_text()) if path.exists() else {"overrides": {}, "outcomes": []}

    if args.status:
        print(json.dumps({
            "overrides": state.get("overrides"),
            "keeps": len(state.get("keeps", [])),
            "reverts": len(state.get("reverts", [])),
            "last_outcomes": state.get("outcomes", [])[-5:],
        }, indent=2))
        return

    for _ in range(max(1, args.cycles)):
        state = evolve_once(state)

    path.write_text(json.dumps(state, indent=2))
    write_learning(state)
    print(json.dumps({
        "cycles": args.cycles,
        "overrides": state.get("overrides"),
        "outcomes": len(state.get("outcomes", [])),
        "keeps": len(state.get("keeps", [])),
        "reverts": len(state.get("reverts", [])),
    }, indent=2))


if __name__ == "__main__":
    main()
