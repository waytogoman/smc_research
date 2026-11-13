# Working rules for any AI session

Draft replacement of 13 November 2026 for AC to edit. Applies to Codex and Claude Code alike.

## At the start of every session

1. Read `GOAL.md`, `PLAN.md` and the last five entries of `LOG.md`. Read nothing else unless the task needs it.
2. Say in two sentences what the goal is and which plan step is current.
3. Pull from GitHub before changing anything.

Do not read the archived autumn work or the old register for guidance. They are history, not instructions, and their style is not to be copied.

## What to work on

- Only the current plan step. A new idea goes into `PARKED.md` as one line.
- A detour longer than one session needs AC's yes.
- Every piece of work ends in a decision for AC: keep, drop or park.

## How to write

- Plain English. Lead with the finding, then what it changes, then what comes next.
- A few numbers, with units. No project shorthand, codes or invented labels.
- Each study has two pages: `RESULTS.md` (plain, one page) and `TECHNICAL.md` (method and detail).

## How to run things

- A study is one folder: `studies/<yyyy-mm>_<name>/` with `run.py`, `RESULTS.md`, `TECHNICAL.md`.
- Short runs on made-up or development data need no permission and no paperwork.
- No authorisation files, receipts, hash manifests, launch cards or audit counts.
- Use naive comparators in every comparison.

## Ask AC first

- Anything that reads outcomes from the final HFR period.
- Any change to the production package `smc_hedge`.
- Any run expected to take more than an hour.
- Any change to `GOAL.md` or to the steps in `PLAN.md`.

## Data

- Fund data is proprietary. It never goes into git, and no fund names leave the machine.
- HFR and Nilsson files live on the data drive. The repository holds code and pages only.
- At a review date, use only what was known at that date.

## Git

- Work on `master`. No branches for research.
- Commit and push after each finished chunk, with a one-line message saying what changed.
- End of session: add three lines to `LOG.md`, commit, push, and say plainly if anything is left uncommitted.
