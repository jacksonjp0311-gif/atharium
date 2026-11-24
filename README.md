<div align="center">

![Atharium](docs/atharium-banner.jpg)

# Atharium

**Claim map under measurement.**

A governed hybrid. Athar's receipt-gated claim-map swarm, stitched to an evolving runner that can improve its own surfaces without ever touching the verifier.

[![License: MIT](https://img.shields.io/badge/License-MIT-8b949e?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Evolve](https://img.shields.io/badge/evolve-twin%20%2B%20oracle-b7c4b6?style=flat-square)](.github/workflows/atharium-evolve.yml)

</div>

---

Atharium is a Frankenstein baby with a hard ceiling.

It keeps the geometry that made Athar's Colony honest: a question is decomposed into fixed claims, scouts return facts not opinions, the queen reads only the cluster map, disagreement is shown rather than averaged, and a missing load-bearing claim returns HOLD. Every fact carries a receipt. An independent verifier recomputes the bundle hash and fails closed on tamper. That surface is load-bearing. It is not free for silent change.

On top of that geometry sits a cyclic runner. On a schedule it measures the current knobs, proposes one safe mutation from a closed set, re-measures, and keeps the change only when the trial window is strictly better *and* a frozen twin control does not lead. Fitness alone never decides. Human authorize remains required for durable accepts, new claims, or permanent rule changes. The independent verifier stays outside the mutation set.

This is not AGI. It is not novel theorem discovery. It is a measured, evidence-gated way for a claim map to improve its own allocation and judgment surfaces while remaining auditable.

---

## Lineage

| Source | What it contributed | Link |
|--------|---------------------|------|
| **Athar's Colony** | Claim registry, cluster map (settled / contested / single / blind / dead), coverage-first allocator, queen that never reads raw answers, independent bundle + sha256 verifier, HOLD on missing load-bearing, no averaging | [atharhive/colony](https://github.com/atharhive/colony) |
| **Agent Colony** | Hard ceiling (tribute, human authorize, append-only witness), twin control arm, keep/revert under measurement, closed-set knobs, scheduled evolve cycles, recommend-only promotion | [jacksonjp0311-gif/agent-colony](https://github.com/jacksonjp0311-gif/agent-colony) |
| **Atharium** | The hybrid. Original surfaces preserved. Evolve loop added under the same ceiling. | This repository |

Original commercial swarm by [Athar](https://github.com/atharhive). Evolving runner and hard ceiling by [James Paul Jackson](https://github.com/jacksonjp0311-gif).

---

## The geometry that stays

```
plan      claims, most load-bearing first, until budget is committed
scout     one claim, one fact, one receipt; failover on broken miner
map       settled / contested / single / blind / dead — queen reads only this
escalate  at most N claims, only contested or dead load-bearing
verdict   ALLOW / ALLOW WITH CONDITIONS / HOLD / BLOCK, from the map alone
bundle    every fact, every receipt, one sha256; independent verifier
```

- Queen never reads a raw answer.
- Disagreement is printed with both sides. No averaging path exists.
- Missing load-bearing claim → HOLD, never a soft ALLOW.
- Verifier does not import producer code. Tamper fails closed.

These rules are load-bearing. Mutations cannot rewrite them.

---

## The loop that can evolve

```
bench     hard checks + verifier
measure   current knobs on a fixed seed set
propose   one closed-set mutation (escalation cap, single-source penalty, priority boost)
trial     re-measure under the mutation
twin      frozen control arm, no mutation
keep      only if trial > baseline AND twin does not lead
witness   append-only record of keep / revert / void
```

Knobs live in `colony/knobs.py`. The evolve driver is `colony/evolve.py`. Scheduled via `.github/workflows/atharium-evolve.yml`.

A keep is a candidate until human authorize. Standing trust may selectively accept machine-checked keeps that improve coverage or residual risk without raising false-positive rate. Never accept-all.

---

## Quick start

```bash
git clone https://github.com/jacksonjp0311-gif/atharium
cd atharium
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# run the evolve skeleton
python -m colony.evolve --cycles 2
python -m colony.evolve --status
```

Offline, no wallet, no network required for the evolve skeleton. Real queen seed-set measurement is the next wiring step.

---

## Layout

```
colony/knobs.py          closed set of safe mutable parameters
colony/evolve.py         cycle driver, twin comparison, keep/revert
colony/__init__.py
CHARTER.md               hard ceiling
society/LEARNING.md      outcomes surface
data/                    evolve state (gitignored or slim-committed)
.github/workflows/       scheduled runner
docs/                    banner and future surfaces
```

---

## Hard ceiling

See [CHARTER.md](CHARTER.md).

1. Creator tribute — serve the active human ask.
2. Human authorize — durable accepts and new claims require it.
3. Append-only witness — the independent verifier stays outside any mutation.

Everything else is free for emergence under measurement.

---

## Status

Skeleton is live. Evolve runner, knobs, twin stub, workflow, and CHARTER are in place. Real measurement against Athar's queen/cluster surfaces (seed counterparties, actual maps, verifier gate) is the next mile. Not AGI. Not a production credit system. A measured hybrid.

---

<div align="center">

Original claim-map geometry by [Athar](https://github.com/atharhive)  
Evolving runner and hard ceiling by [James Paul Jackson](https://github.com/jacksonjp0311-gif)  

MIT

</div>
