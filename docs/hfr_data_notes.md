# HFR data: what is in it

13 November 2026. From a first look at the table layouts, fund descriptions and return dates of the ASCII files. No return values were read. Counts are before any cleaning.

## Where it is

- Raw files: `C:\Users\aldoc\My Drive\30_dev_data\hfr_data\raw` (six zip files: live and dead databases, each in ASCII, Access and Excel). Delivered 10 November 2026.
- Licensed to Hagakure Ltd. AC has confirmed the intended use with HFR and that cloud storage is allowed.
- Working source: the two ASCII zips. Access is kept as a reference for how tables link. Excel is for looking by eye only.
- The data never goes into git.

## What is in it

| | Live | Dead |
| --- | --- | --- |
| Fund records | 6,220 | 25,321 (15,128 liquidated, 10,193 stopped reporting) |
| Monthly return rows | 893,438 | 1,965,454 |
| Asset rows | 499,146 | 1,320,261 |
| Equity Hedge | 2,451 | 9,512 |
| Relative Value | 1,406 | 3,711 |
| Macro | 942 | 4,657 |
| Event-Driven | 392 | 1,827 |
| Fund of Funds | 402 | 5,312 |

Each database has six tables: fund details, returns (monthly return and NAV), assets, instruments, regions, and HFR index constituents.

- **Date added to the database** is filled for all but one fund in each file. It starts in May 1996.
- **Returns** for live funds run into 2026.
- **Reporting basis:** almost all records are net of all fees.

## What the intake step must handle

1. **Records that are not single hedge funds.** About 275 HFR index records in the live file, plus funds of funds, crypto funds, risk-premia products and long-only products. Each needs an in-or-out rule.
2. **Share classes.** A family identifier links classes of one fund: 917 live families have more than one record. In the dead file it is blank for 23,604 of 25,321 records, so duplicates there must be found another way, such as same firm and near-identical returns.
3. **Currencies.** 61% of live records report in US dollars. One class per fund, with cash subtracted in the matching currency.
4. **Fees.** Drop the few records that are gross of fees or net of management fee only.
5. **Funds that stopped reporting.** Their last months are missing. The test design needs a stated assumption for them.
6. **Personal details.** The fund table has names, phone numbers and emails. The derived panel leaves those columns out.

## What the date-added field does and does not give

- It tells us when a fund entered the database, so funds can be included only from that date and backfilled history can be identified.
- It does not tell us when each monthly return was reported or revised. A fixed one-month reporting delay covers that.
