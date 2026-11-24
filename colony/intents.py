"""Claim registry — Athar geometry, preserved.

Seven claims. Load-bearing flags fixed. Queen only reads the map built from these.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Inputs:
    company: str
    jurisdiction: str = "Denmark"
    domain: str | None = None
    country: str | None = None
    year: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "domain", self.domain or "")
        object.__setattr__(self, "country", self.country or self.jurisdiction)
        object.__setattr__(self, "year", self.year or 2025)

@dataclass(frozen=True)
class Claim:
    id: str
    question: str
    fields: tuple[str, ...]
    load_bearing: bool = False
    priority: int = 50

CLAIMS: tuple[Claim, ...] = (
    Claim("sanctions", "Is the entity on a sanctions list?", ("matched",), load_bearing=True, priority=10),
    Claim("registry", "Is the legal entity real and active?", ("active", "legal_name"), load_bearing=True, priority=20),
    Claim("filings", "Has it filed recently?", ("filing_count",), priority=30),
    Claim("identity", "Does the operating profile match?", ("industry",), priority=40),
    Claim("news", "Adverse coverage?", ("result_count",), priority=50),
    Claim("macro", "Home market stable?", ("rate_pct",), priority=60),
    Claim("fx", "Settlement risk?", ("converted_amount",), priority=70),
)

BY_ID = {c.id: c for c in CLAIMS}

# Measurement set used during evolve cycles. Hold-out set reserved for accept-time check.
MEASURE_COMPANIES = (
    Inputs(company="A.P. Moller-Maersk A/S", domain="maersk.com"),
    Inputs(company="Example Corp", domain="example.com", jurisdiction="US"),
    Inputs(company="Gap Co", domain="gap.example", jurisdiction="US"),
)
HOLD_OUT_COMPANIES = (
    Inputs(company="Contested Ltd", domain="contested.example"),
)

# Backward-compatible alias
SEED_COMPANIES = MEASURE_COMPANIES
