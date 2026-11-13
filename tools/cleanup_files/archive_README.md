# Autumn 2026 research archive

Everything in this folder is the research done in this repository between
September and November 2026. It was moved here on 13 November 2026 when research
moved to the separate `smc_research` repository.

**This is history. It is not a guide to how work is done, and its plans, handoffs
and rules are no longer in force.** The review of this work and what was kept from
it are in `smc_research/docs/2026-11-13_review_summary.md`.

## What is here

| Folder | Contents |
| --- | --- |
| `research/` | 87 dated study folders: code, result reports and receipts. Twelve September folders concern the factor rebuild; the rest concern alpha measurement. |
| `docs/research/alpha_programme/` | Plans, results in plain English, decisions log, session handoffs, programme map |
| `docs/research/factors_review/` | The September review of the factor construction |
| `docs/research/brainstorming/`, `organisation/`, `sync/` | Earlier notes and the October navigation records |
| `backtest/runs/alpha_rankings/` | The September draft of a real-fund test for Recent24, which never ran. Its note on the earlier backtest's defects is still useful. |
| `archive/research/` | Document versions replaced during the October reorganisation |
| `tools/`, `tests/` | The session-sync, evidence-restore, programme-map and process-supervisor utilities, with their test |
| `AGENTS_2026-11.md` | The working rules in force until 13 November |

## Things worth knowing

- **Layout is preserved.** Each item sits at the same relative path it had at the
  repository root, so links between these pages and study folders still work.
  Links that point to production code or to `archive/v1` were written relative
  to the old location; read them as starting from the repository root.
- **Bulk run output is not here.** Simulation outputs, scratch files and caches
  were never in git. On 13 November they were moved out of the working tree to a
  holding folder beside the repository on each machine.
- **Still relevant to production:** the September factor review proposed a
  corrected factor build that has not been adopted. See
  `docs/research/factors_review/2026-09-10_factor_engine_production_handoff.md`.
- **Recent24:** the candidate's code is in `research/2026-09_alpha_representation/`,
  `research/2026-09_alpha_dynamics/` and `research/2026-09_alpha_calibration/`,
  as listed in `docs/research/alpha_programme/candidates/recent24_mean_v1/README.md`.
- **Recovering the old layout:** the tag `pre-cleanup-2026-11-13` marks the last
  commit before the move.
