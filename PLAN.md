# Plan

Version of 13 November 2026, for AC to edit. One page. Time budgets are first guesses.

**Current step: 0**

| Step | What | Done when | Budget |
| --- | --- | --- | --- |
| 0 | Set up | Done: this repository is on GitHub and the pending `smc_hedge` commits are pushed. Still to do: archive the autumn work in `smc_hedge` by running `tools/cleanup_smc_hedge.py` (see `docs/smc_hedge_cleanup_plan.md`). | Half a day |
| 1 | Rehearse on the old database | The whole test runs end to end on the Nilsson data, which has already been seen. No conclusions are drawn from it. | 3 days |
| 2 | Bring in HFR | Point-in-time panel built from the date-added field, one record per fund. One table of fund counts by year and strategy, live and dead. | 3 days |
| 3 | Settle how far back we go | The first review date is fixed and written below, from the three clocks in `docs/test_design_notes.md`. Includes the small long-history set of market factors (agreed 13 November): fixed list, public data, three days at most. | 3 days |
| 4 | Design page | One page, agreed by AC: universe, review dates, scores, outcome, comparison. | 1 day |
| 5 | Precision check | Using random scores only, one number: the smallest top-group advantage the test can see. If it is too large, the design changes before any real score is looked at. | 2 days |
| 6 | Development run | Results page for the development period: every score against the outcome, plus the NAV split for a few funds. | 1 week |
| 7 | Decide, then final test | Each score is kept, dropped or parked. The final design is written down, then run once on the untouched period. | 1 week |

## The test in brief

Detail and reasons are in `docs/test_design_notes.md` (plain) and `docs/test_design_technical.md`.

- **At each review date:** score every eligible fund using only what was known then.
- **Scores to compare:** plain past return, a simple regression alpha, Recent24, the production estimate, its q05 version, the ratio of alpha to error with a minimum alpha level, and the spectral measure.
- **Outcome:** compounded return beyond markets over the following 12 months, measured from later data only. Measured two ways: against market factors, and against the average of funds in the same strategy.
- **Comparison:** the top group against the eligible universe, within strategy. Also the agreement between score ranks and later ranks across all funds.
- **Universe:** live and dead funds, as they stood at each review date.

## Provisional dates

| Item | Provisional value | Status |
| --- | --- | --- |
| Development period | Review dates up to the end of 2015 (outcomes run to the end of 2016) | Agreed in principle; depends on step 3 |
| Final period | Review dates from January 2017 | Not to be opened before step 7 |
| First review date | To be set in step 3 from fund counts and factor history | Open |
| Reporting delay | One month | AC's view |
| Main horizon | 12 months | Earlier choice |
| Minimum history to be scored | 36 months, the same for every score | Proposed |

## Decisions AC still owes

- [x] Build a small long-history set of market factors (step 3). Agreed 13 November.
- [ ] Which records are in the universe: funds of funds, crypto, risk-premia, long-only and UCITS products.
- [ ] What to assume for a fund that stops reporting during the 12-month outcome window.
- [ ] Whether to delete the simulation run outputs once they are in the holding folder (see `docs/smc_hedge_cleanup_plan.md`).

## Rules for this plan

- One step is current. Work that does not serve it goes to `PARKED.md`.
- A detour longer than one session needs AC's yes.
- If a step runs to twice its budget, stop and ask whether it is still worth it.
- The final period is not opened before step 7.
