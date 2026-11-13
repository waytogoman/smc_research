# Cleaning up smc_hedge

13 November 2026. Based on a scan of the whole `C:\dev\projects\smc_hedge` folder and of what git tracks there. Nothing has been changed yet. The script `tools/cleanup_smc_hedge.py` in this repository carries out the plan; it reports first and changes things only with `--apply`.

## The picture today

Git tracks 5,910 files, 657 MB. Production is about 1% of that.

| Part | Files | Size | What it is |
| --- | ---: | ---: | --- |
| `research/` | 3,079 | 482 MB | 87 dated study folders from September to November |
| `archive/v1/` | 1,893 | 123 MB | The withdrawn backtest, sealed |
| `docs/research/` | 460 | 28 MB | Plans, results, handoffs, decisions log |
| `data/` | 12 | 17 MB | Fund and factor input files |
| `docs/app/`, `docs/backtest/` | 54 | 3 MB | Production documentation |
| `smc_hedge/`, `tests/`, `backtest/`, `tools/`, `config/` | 277 | 3 MB | The production package, its tests, the backtest framework, utilities |
| Other archive folders and root files | 135 | 2 MB | Earlier retired code and notes; README and rules files |

On top of this, the study folders hold run outputs that git ignores. The repository's own record put them at 176 GB on 24 October, 155 GB of it in one study. The dry run measures the current figure.

## What happens to every item

Tracked items move with `git mv` into one folder, `archive/2026_autumn_research/`, at the same relative path they have now. That keeps the links between the archived pages and study folders working, and keeps the full history.

| Item | What it is | Action |
| --- | --- | --- |
| `smc_hedge/` | Production package, 98 files | Stays |
| `tests/` | 47 files | Stays, except the process-supervisor test, which is archived |
| `backtest/smc_backtest/` | Backtest framework, 98 files | Stays |
| `backtest/runs/_template/` | Template for future backtests | Stays |
| `backtest/runs/alpha_rankings/` | September draft of a real-fund test for Recent24, never run, 15 files | Archived |
| `config/` | Paths and constraints | Stays |
| `data/` | See the next table | Untouched in this pass |
| `docs/app/`, `docs/backtest/` | Production documentation | Stays |
| `docs/README.md` | An index that is now mostly about research | Replaced by a short index |
| `docs/SESSION_SYNC.md` | The two-machine procedure | Archived; replaced by one line |
| `docs/research/` | All research pages, including the September factor review | Archived |
| `research/` | All 87 study folders | Tracked files archived; run outputs to the holding folder |
| `tools/` | 13 files | Nine production utilities stay. Four autumn tools are archived: programme-map builder, evidence restore, process supervisor, session-sync check |
| `archive/v1/` and the other existing archive folders | Earlier history | Untouched |
| `archive/research/` | Page versions replaced in the October reorganisation, 38 files | Moved inside the autumn archive |
| `work/` | Scratch: 14 folders and 24 loose scripts and logs, not in git | Holding folder |
| `~archived_code/` | Four zip snapshots of the code from May, 8.5 MB, not in git | Holding folder |
| `scripts/` | Only stale cache files, not in git | Holding folder |
| `AGENTS.md` | The autumn working rules | Archived; replaced by seven lines for production |
| `README.md` | Front page | Replaced: research removed, pointer to `smc_research` added |
| `CONTRIBUTING.md`, `CLAUDE.md` | Rules for production changes | Stay, with five small wording changes |
| `.gitattributes` | Line-ending and byte-preservation rules | Replaced: one rule covers the new archive |
| `.gitignore`, `pyproject.toml`, `requirements.txt` | | Stay |
| `.venv`, `.idea`, `.vscode`, `.pytest_cache`, `.env`, `smc_hedge.egg-info` | Local, not in git | Untouched |

After the cleanup the top level is: `smc_hedge`, `tests`, `backtest`, `tools`, `config`, `data`, `docs`, `archive`, and the root files.

## The data folder

Left alone in this pass, because moving input files is a production change that needs a search of the code and a test run. This is what is there.

| File | Status |
| --- | --- |
| `active_returns.csv`, `active_reference.csv`, `graveyard_returns.csv`, `graveyard_reference.csv` | Current production inputs. Their fingerprints are fixed in `smc_hedge/production/pinned_inputs.json` |
| `rf/GS3M_20260614.csv` | Source for the cash rate |
| `README.md` | Inventory of the files and their sources |
| `active_returns_v7universe.csv`, `active_returns_v7excess.csv` | The frozen subset from the old backtest. The inventory says production no longer uses it |
| `factor_returns_extended.csv` | An older factor panel. The inventory says it is not a substitute for the current one, but `config/paths.py` still points at it |
| `correlation_raw_extended.csv`, `correlation_residualized_extended.csv` | Factor diagnostics from May |
| `data_ror_carthesio.csv` | One small file whose purpose I do not know |

The last four rows are candidates for the archive. That should be a separate half-hour job on a branch: search for each file name in the code, move what nothing reads, run the tests.

## What is not in git

Everything git does not track in the folders above goes to a holding folder next to the repository, `C:\dev\projects\_cold\smc_hedge_2026_autumn`, under the same relative paths. It is on the same drive, so the move is immediate. Nothing is deleted.

My recommendation is to delete the simulation run outputs after a month if nothing has been needed from them. Every study is closed, its conclusions are in its result page, and the outputs can be produced again from the code. That decision is AC's and the script does not make it.

## How to run it

Close anything that has files open in `research` or `work` first.

```
cd C:\dev\projects\smc_research
python tools\cleanup_smc_hedge.py --repo C:\dev\projects\smc_hedge
python tools\cleanup_smc_hedge.py --repo C:\dev\projects\smc_hedge --apply
cd C:\dev\projects\smc_hedge
git status
python -m pytest -q
git commit -m "Archive autumn 2026 research; keep production tree only"
git push --follow-tags
```

The first run only reports. The second tags the current state as `pre-cleanup-2026-11-13`, makes the moves and stages them. It does not commit. The full test run takes about 18 minutes.

On the Mac, afterwards:

```
git pull
python tools/cleanup_smc_hedge.py --repo <path to smc_hedge> --bulk-only --apply
```

To undo before committing: `git reset --hard pre-cleanup-2026-11-13` puts every tracked file back, and the untracked content is in the holding folder.

The script was tested on a copy of the repository's file layout with placeholder contents, on Linux. It has not been run on Windows or on the real files, which is why the dry run comes first.

## Things found along the way

1. **The corrected factor build from September is not in production and its files are not on this machine.** The pages refer to `work/factor_basis_2026-09-10/` (the selected 18-factor panel and its manifest) and `work/etf_mapping_2026-09-10/`. `work/` is not in git, and neither folder is in the Windows `work` folder. Look for them on the Mac or the data drive before cleaning the Mac.
2. **Recent24's code is in three archived study folders:** `research/2026-09_alpha_representation/`, `2026-09_alpha_dynamics/` and `2026-09_alpha_calibration/`. Plan step 1 copies what is needed into this repository.
3. **The note on the earlier backtest's defects** (`backtest/runs/alpha_rankings/2026-09_recent24_predictive/PRIOR_DEFECTS.md`) is worth reading when the design page is written.
4. **An old branch on GitHub,** `estimator-event-e2-candidate`, is not part of this cleanup. Delete it or keep it as AC prefers.
5. **The data drive folder `30_dev_data\smc_hedge`** has 24 folders that, going by their names only, mix current production outputs with material from the old backtest and the autumn research (`f9`, `pre_f9_scratch`, `vms1`, `withdrawn`, `bundles`, `pc_transfer`, `alpha_research_evidence`). I have not looked inside. A later pass could gather the historical ones under one `_archive` folder.
