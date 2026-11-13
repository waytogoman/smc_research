# Test design: technical notes

13 November 2026. Companion to `test_design_notes.md`. Method names and arithmetic only; nothing here has been run.

## Timing and eligibility

- Review dates `t` are month ends. Scores use returns through `t - 1` (one-month reporting delay).
- Eligible at `t`: `Date_Added_to_DB <= t`, at least 36 monthly returns through `t - 1`, still reporting at `t - 1`, passes the universe filters and any size floor measured at or before `t - 1`.
- Two score variants: (a) full visible history, including months before `Date_Added_to_DB`; (b) post-addition months only. Variant (a) is primary because it matches what a database user saw at `t`. It uses today's vintage of those returns, since per-return vintages are not available.
- Outcome window: months `t + 1` to `t + 12`.
- Development review dates end 12 months before the first final review date, so no development outcome month falls in the final period.

## Factor history

- Production lens (`macro_sec_nocrypto`, 18 factors): 163 complete months, October 2012 to April 2026, per `smc_hedge/data/README.md`. The committed older panel shows level 0 from 2008-09, level 1 from 2010-09, level 2 from 2012-09. The cause of the two-year steps (residualisation warm-up or instrument start dates) has not been checked in `factor-lens`.
- Production estimation: expanding window, 12 leading observations dropped after the factor floor, at least 36 remaining (`make_production_config`). Earliest production estimate on the 18-factor lens is therefore October 2016.
- Long-history set (proposed, to be confirmed in plan step 3): about eight raw, non-residualised factors with monthly history from the mid-1990s. Candidate exposures: equity market, size, value, momentum, government bond duration, credit spread, commodities, US dollar, emerging equities. Sources to be confirmed; no hierarchy, no LASSO selection in the simple scores.

## Outcome definitions

1. Factor-adjusted: `r_fund - rf - sum(beta * factor)` per month in the outcome window, with betas either fixed at `t` or fitted fresh on the outcome window. Never the continuing filter state from the selection date (October rolling-pilot finding). Compounded over 12 months.
2. Peer-relative: `r_fund - mean(r of eligible funds in the same HFR main strategy)` per month, compounded over 12 months. No factor model.
3. Returns in the share-class currency, less cash in that currency, or one class per fund in a single currency. To be fixed on the design page.
4. Disappearing funds: use reported returns to the last month, then one stated assumption for the remainder (for example peer average) and one harsher alternative (for example a fixed loss in the exit month).

## Dealing with dependence

- **Calendar-time portfolios.** At each month `t` form the top group; hold each cohort for 12 months; the strategy return in calendar month `m` is the average over the 12 live cohorts. Analyse the monthly series of (top group minus universe). The test statistic is the mean of that series with a heteroskedasticity- and autocorrelation-consistent standard error (Newey-West, a few lags, to allow for smoothed returns). No overlapping 12-month sums enter the inference.
- **Strategy neutrality.** Rank within HFR main strategy and form the top group as the union of within-strategy top groups, so the spread carries no strategy tilt.
- **Whole cross-section.** Monthly Spearman rank correlation between score at `t` and the later outcome, averaged over time, with a time-series standard error on the monthly correlations (Fama-MacBeth style).
- **Placebo inference.** Replace the score with random draws within strategy, 1,000 times, and run the identical pipeline. The placebo distribution gives a p-value that inherits all cross-sectional and time dependence, and its spread gives the precision of the design before any real score is examined.
- **Multiplicity.** Seven or so scores in development; one or two carried to the final period with the outcome, horizon and comparison fixed in writing first.

## Rough precision arithmetic

Derived from the earlier backtest's reported figures, not recomputed.

- Reported 90% half-width of the monthly spread mean: 0.003728. Standard error = 0.003728 / 1.645 = 0.00227 a month, or 2.72% a year, over 6.75 years of dates.
- Implied effective volatility of the spread: 2.72% x sqrt(6.75) = about 7.1% a year.
- Over `T` years, standard error = volatility / sqrt(T). Smallest effect detectable at 90% two-sided confidence with 80% power = (1.645 + 0.84) x standard error.

| Spread volatility | Years | Standard error | Detectable effect |
| --- | --- | --- | --- |
| 7.1% | 6.75 | 2.7% | 6.8% a year |
| 7.1% | 20 | 1.6% | 3.9% a year |
| 2.0% | 20 | 0.45% | 1.1% a year |
| 2.0% | 9 | 0.67% | 1.7% a year |

The last row is roughly the final period (review dates from 2017). The placebo run in plan step 5 replaces these guesses with a measured figure.

## Alpha-to-error ratio

- Score: estimated alpha divided by the residual standard deviation over the same window (appraisal ratio), with a floor on alpha.
- Link to the outcome: for monthly ratio `k` and horizon `T` months, the chance that cumulative alpha is positive is about `Phi(k * sqrt(T))`. Example: alpha 20 bp, residual 2% a month, `k` = 0.1; 12 months gives 64%, 24 months gives 69%.
- Compounding drag from residual noise is about half the monthly variance: 2% a month costs about 2 bp a month.
