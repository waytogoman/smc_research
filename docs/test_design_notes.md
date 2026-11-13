# Notes for the test design

13 November 2026. Plain-English notes on the two issues AC raised before the design page is written (plan step 4). Formulas and method names are in `test_design_technical.md`.

## 1. How far back can we go

In the earlier backtest this was muddled: AC understood the rule as 12 + 36 months, and the analysis actually required 12 + 60. Three separate clocks decide the answer. They should be stated separately and never merged.

### The three clocks

| Clock | What it is | Where it stands today |
| --- | --- | --- |
| Market data | The first month for which every market factor exists | The 18-factor production set is complete from **October 2012**. Its levels start two years apart (2008, 2010, 2012). |
| Fund history | How many months a fund must have before it gets a score | Production drops a fund's first 12 months and then needs 36 more. The earlier backtest needed 12 + 60. |
| Outcome | How long after the review date we wait to see the result | 12 months, plus a one-month reporting delay. |

Put together, the earlier backtest could not start before autumn 2018: factor start plus 72 months. That left 27 quarterly dates. The same factors with the production rule would start in October 2016.

HFR itself is not the limit. Its date-added field starts in May 1996 and fund returns go back further.

### What to do about each clock

**Market data: build a small long-history set of factors.** A fixed list of about eight broad exposures (equities, small against large, value, momentum, government bonds, credit, commodities, the dollar, emerging markets) exists from the mid-1990s in public sources. This lets review dates start in the late 1990s. All scores use the same factors, so the comparison is about the scoring method and not about the factor set. From 2017 the 18-factor set is also available and can be compared with the small set directly.

This must not become another factor project. The guard is a fixed list, public data, three days at most, and any factor that takes more than a day to source is dropped.

**Market data, second route: compare each fund with its strategy peers.** HFR gives every fund a strategy. Return beyond the average of funds in the same strategy needs no factors at all and is available for the whole history. It is a rougher measure of return beyond markets, and it answers the ranking question directly. The test should report the outcome both ways.

**Fund history: let the date-added field replace the 12-month drop.** The production code describes the 12-month drop as a guard against backfilled track records. HFR's date-added field does that job exactly, fund by fund:

- A fund can be scored only at review dates after it was added to the database.
- Its earlier history, including the backfilled part, may be used to compute the score, because an allocator looking at the database on that date would have seen it. A second version of each score, using only returns after the fund was added, shows how much this matters.
- The outcome is always measured on months after the review date, so it never contains backfilled returns.

**Fund history: one minimum for every score.** Proposed: 36 months. Every score is computed on the same funds at each date. A score that cannot produce a number for a fund is shown as missing and counted, not quietly dropped.

**Outcome: decide what a disappearing fund is worth.** A fund that stops reporting during the 12 months has no final returns, and they were probably poor. The design page needs one stated assumption and one harsher alternative.

## 2. Too few independent observations

The earlier backtest had 27 quarterly dates with 12-month outcomes. Neighbouring outcomes shared nine months, so there were only six or seven independent years. Its top-minus-bottom spread also moved around a lot from period to period: about 7% a year, by my rough reading of its reported figures. With that much movement, even 20 years could reliably detect only a spread of about 4% a year.

So a longer history helps but is not enough on its own. Six changes address the problem, in rough order of importance.

1. **Make the comparison quieter.** Rank funds within their strategy and compare the top group with peers in the same strategy. Most of the period-to-period movement in the old spread came from the top and bottom groups holding different kinds of funds. Removing that is the largest gain available. With movement of 2% a year instead of 7%, 20 years can detect a spread of about 1% a year.
2. **Use many more funds.** HFR has about 31,000 fund records before duplicates are removed, against under 2,000 in the old universe. A group average over hundreds of funds is far steadier.
3. **Count every month once.** Hold each top group for 12 months and record, month by month, what the held funds earned beyond markets against the universe. This gives one monthly series with no double counting, and every month of history is used.
4. **Use all the funds, not only the extremes.** Each month, measure how well the score ranking agrees with the later ranking across the whole universe. This uses far more information than the difference between two groups.
5. **Ask how often chance would do as well.** Run the same test with random scores a thousand times. The share of random runs that beat the real score is the answer, and it needs no assumption about independence. Random scores also tell us, before any real score is looked at, how small an advantage the test can see. That is plan step 5.
6. **Ask one main question.** One outcome, one horizon, one main comparison. Every extra score or horizon examined makes a lucky result more likely. The development period is for choosing; the final period tests one or two choices only.

What cannot be fixed: years are years. A crisis is one event however many funds lived through it. The honest statement of the final result will include how small an effect the test was able to see.

## 3. Assets under management

HFR includes a history of each fund's assets. It is reported for a little over half of live fund-months and about two thirds of dead fund-months, so it is useful but incomplete.

Two uses belong in the test itself:

- **A size floor at each review date,** so the universe contains funds an allocator could actually have bought.
- **Results weighted by assets as well as equally weighted,** to see whether the finding lives only in very small funds.

The wider lines of inquiry are parked in `PARKED.md` until the ranking test is done: whether alpha fades as a fund grows, whether money chases past performance, what investors earned in money-weighted terms, and whether falling assets warn of a fund's closure.
