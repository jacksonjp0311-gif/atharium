# Cross-surface lessons

Atharium ↔ Agent Colony. No repo coupling. Notes only.

## From Atharium measurement so far

- Closed-set knobs + twin control is sufficient to exercise keep/revert without opening the mutation surface.
- Offline fixtures with controlled gaps and disagreement make Oracle kills observable and calibratable.
- Fail-closed live path (return None → fixtures) keeps the schedule reliable while the gated scout is still a stub.

## Possibly useful back on Agent Colony

- Explicit "used_live" flag in the measurement dict makes fail-closed behavior visible in the outcome log.
- Oracle threshold for false-positive proxy can be tightened once the seed set contains disagreement; the same pattern may apply to novelty or residual-risk proxies.

## Open

- Real Telegraph scout wiring remains gated. When added, the same keep/revert rule should score it without code changes to the evolve driver.

Not AGI. Verifier stays outside.
