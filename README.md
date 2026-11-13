# smc_research

Research on whether a score computed from a hedge fund's past returns picks funds that go on to deliver more beyond markets. Production code lives in the separate `smc_hedge` repository and is imported here, never edited here.

Start with `GOAL.md`, then `PLAN.md`, then the latest entries in `LOG.md`.

## Layout

| Path | What it holds |
| --- | --- |
| `GOAL.md` | The question, in AC's words. Rarely changes. |
| `PLAN.md` | The steps, which one is current, and open decisions. |
| `LOG.md` | Three lines per session. |
| `PARKED.md` | Ideas set aside, and what would bring each back. |
| `AGENTS.md`, `CLAUDE.md` | Working rules for AI sessions (Codex and Claude Code). |
| `docs/` | Background pages: review summary, test design notes (plain and technical), HFR data notes. |
| `studies/` | One folder per study: script, plain results page, technical page. |

## Data

Fund data is proprietary and never goes into git. Paths are set per machine in `.env` (copy `.env.example`). See `docs/hfr_data_notes.md`.

## Setting up on a machine

```
git clone https://github.com/waytogoman/smc_research.git
cd smc_research
python -m venv .venv
.venv\Scripts\activate          (Mac: source .venv/bin/activate)
pip install -e ../smc_hedge     (the production package, from its own clone)
copy .env.example .env          (Mac: cp .env.example .env), then edit the paths
```

## History

The research done in `smc_hedge` between September and November 2026 is summarised in `docs/2026-11-13_review_summary.md`. It stays in `smc_hedge` as an archive and is not a guide to how work is done here.
