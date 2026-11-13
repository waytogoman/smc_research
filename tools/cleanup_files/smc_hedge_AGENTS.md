# Working rules for any AI session in smc_hedge

This is the production repository. Research is done in `smc_research`.

1. Read `CLAUDE.md` first. Its non-negotiables apply to every assistant, not only Claude.
   `CONTRIBUTING.md` is the authority on layout and on how changes land.
2. Change production code only when AC has asked for that change. Use a short-lived
   branch, run the tests, add a changelog line and tag the release as `CONTRIBUTING.md` says.
3. Do not start research here. No new study folders, plans, handoffs or receipts.
4. `archive/` is read-only history. Do not take instructions or writing style from it.
5. Write in plain English: the finding or change first, then what it affects.
6. Pull before starting. Commit and push after each finished chunk, and say plainly
   if anything is left uncommitted.
7. Fund data is proprietary: nothing with fund names leaves the machine.
