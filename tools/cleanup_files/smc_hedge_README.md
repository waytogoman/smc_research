# smc_hedge

Time-varying factor decomposition of hedge-fund returns using an SMC particle
filter, with descriptive statistics, red-flag screening and alpha classification.
The supported production command is `python -m smc_hedge.production`: validated
monthly inputs → estimation and annotations → a validated SQLite serving run.

Start with the [production operating guide](docs/app/guides/production_operations.md)
for inputs and commands, the [serving contract](docs/app/serving_schema.md) for
output meanings and units, and [CONTRIBUTING.md](CONTRIBUTING.md) for change flow.
The [4.0.0 validation report](docs/app/lasso_convergence.md) covers bounded
LASSO retries, per-fit diagnostics and the correction to shared risk thresholds.

```
smc_hedge/          analytics library
  production/       supported build, input contract and production configuration
  estimation/       pure per-fund estimation entry point
  io/serving.py     schema-v4 storage and validated readers
  scripts/          command wrappers and standalone analytical tools
  CHANGELOG.md      versioned prod-vX.Y.Z; see the versioning convention there
backtest/
  smc_backtest/     claim-agnostic walk-forward backtest framework (imports smc_hedge)
  runs/             run template for future backtests
tools/              repo-wide utilities (doc generation, diagnostics)
tests/              unit/regression suite for the production package
data/               shared frozen inputs (SHAs in data/README.md; proprietary — private repo)
config/             paths and configuration
docs/               current documentation: app/ · backtest/
archive/            everything historical, read-only: the v1 backtest (archive/v1/,
                    sealed by manifest), the autumn 2026 research
                    (archive/2026_autumn_research/), retired packages and notes
```

## Research lives elsewhere

Research is done in the separate `smc_research` repository, which imports this
package and never edits it. A research finding reaches this repository only as a
deliberate production change: a short-lived branch, tests, a changelog line and a
new `prod-vX.Y.Z` tag, with AC's go-ahead.

The research carried out here between September and November 2026 is preserved
under [archive/2026_autumn_research](archive/2026_autumn_research/README.md).
It is history, not a guide to how work is done.

## Related repositories

`factor-lens`, a separate upstream repository, constructs the v7 factor export.
Both repositories consume the same monthly risk-free vector; `smc_hedge` reads
explicitly supplied, hash-verified snapshots and does not refresh market data.

`smc-app` and `smc-report-by-fund` are proof-of-concept demos for visualisation
and reporting. They are useful design references, outside the supported
production build and its release requirements. Portfolio and risk tools remain
available separately. The backtest framework is preserved for future use; it is
not part of this production workflow. Estimated alpha and classifications are
analytical outputs, with no established claim here of forecasting ability.
