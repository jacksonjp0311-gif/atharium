"""Cluster map — the only thing the queen reads.

States: settled / contested / single / blind / dead.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Fact:
    claim_id: str
    fields: dict[str, Any]
    ok: bool = True
    empty: bool = False
    price_usd: float = 0.01

    def as_dict(self) -> dict[str, Any]:
        return {"claim_id": self.claim_id, "fields": self.fields, "ok": self.ok, "empty": self.empty}

@dataclass
class Cluster:
    claim_id: str
    facts: list[Fact] = field(default_factory=list)

    @property
    def solid(self) -> list[Fact]:
        return [f for f in self.facts if f.ok and not f.empty]

    @property
    def state(self) -> str:
        solid = self.solid
        if not solid:
            return "dead" if not any(f.ok for f in self.facts) else "blind"
        if len(solid) == 1:
            return "single"
        # simple agreement on first field
        vals = [str(next(iter(f.fields.values()), "")) for f in solid]
        if len(set(vals)) > 1:
            return "contested"
        return "settled"

    def as_dict(self) -> dict[str, Any]:
        return {"claim_id": self.claim_id, "state": self.state, "scouts": len(self.facts)}

def cluster(facts: list[Fact]) -> dict[str, Cluster]:
    out: dict[str, Cluster] = {}
    for f in facts:
        out.setdefault(f.claim_id, Cluster(claim_id=f.claim_id)).facts.append(f)
    return out
