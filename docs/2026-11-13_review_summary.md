# Review of the work since September: summary

13 November 2026. One-page summary of the full review, which is a Claude document:
https://claude.ai/artifact/F9ApfqPQActNpz2gHc7yZM
(AC can export it to Markdown and save it next to this page.)

The review rests on the programme's written record in `smc_hedge`. Figures were not recomputed.

## Verdict

The September work was sound. From October the programme kept refining the estimator in simulation and never returned to real funds. Three forces drove that: over-correction after the withdrawn backtest, every question becoming a study, and working rules that rewarded adopting nothing.

## What we keep

- Corrected factor and cash inputs (September).
- Particle filter and exact Kalman calculation agree, so the choice of engine is not the issue.
- The cautious q05 estimate has no special status; reported uncertainty ranges are not reliable.
- The estimate reacts slowly when alpha changes.
- Recent24 as a candidate: better when alpha changes, a little worse when it is steady.
- A different equity response in rising and falling markets helps when present.
- Elaborate selectors did not beat simple ones in simulation, so naive comparators are always included.
- Carrying an estimate forward manufactures apparent persistence, so outcomes are measured from later data only.
- The simple estimator weights months unevenly when alpha changes (a known limit, not a reason for a new estimator).
- Identical returns can be skill or noise; returns alone cannot tell.
- Splitting NAV into markets, alpha and error, using production betas.

## What we dropped

The eleven-package plan, the timing and currency branch, the trend, shift and shock variants, the joint-history filter, calibration of error ranges on simulated histories, and the receipts, authorisations, hash manifests, mind map and decisions log.

## What we measure (AC's point)

The outcome is the compounded return a fund delivered beyond markets, not average alpha. The ratio of alpha to error decides how likely that is to end positive, and it replaces q05 as the cautious score, with a minimum alpha level beside it.

## Lessons from the withdrawn backtest

- It was positive and imprecise, not a failure: a spread of about 3.9% a year that could not be separated from zero. The 4.47% figure was the width of that range, not a power calculation.
- Check before running that a test can answer its question.
- Test what the allocator does (top group against the universe) and the number the product shows.
- Include dead funds.
- Rehearse on a development period before the one protected test.
- Record-keeping is not rigour.
