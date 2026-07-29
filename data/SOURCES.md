# Data sources

All figures are real, drawn from Pinterest's Q4 & Full-Year 2025 earnings
report (released February 12, 2026) and corroborating coverage.

## `pinterest_mau.csv` — global monthly active users (millions), Q4 of each year

| Year (Q4) | MAUs (M) | Notes |
| --- | --- | --- |
| 2019 | 335 | reported |
| 2020 | 459 | reported |
| 2021 | 431 | reported — decline as pandemic lockdowns eased |
| 2022 | 450 | reported |
| 2023 | 498 | reported |
| 2024 | 553 | reported (consistent with the +12% YoY to 619M) |
| 2025 | 619 | reported — record high, +12% YoY |

## `pinterest_regions_q4_2025.csv` — Q4 2025 by geography

| Region | MAUs (M) | Q4 revenue ($M) |
| --- | --- | --- |
| US & Canada | 105 | 979 |
| Europe | 158 | 245 |
| Rest of World | 356 | 96 |
| **Total** | **619** | **~1,319** |

The share-of-users vs share-of-revenue split is computed in code from this
table, so nothing is hand-entered twice.

## `pinterest_mau_quarterly.csv` — global MAUs by quarter (millions)

Quarter-end global MAUs, Q1 2019 – Q4 2025 (28 points), from Pinterest's
quarterly earnings releases (8-K / 10-Q) and investor relations. The four
Q4 values match `pinterest_mau.csv` exactly (335 / 459 / 431 / 450 / 498 /
553 / 619); several intermediate quarters (e.g. Q1 2021 = 478, Q4 2021 =
431, Q2 2024 = 522, Q3 2024 = 537, and all four 2025 quarters) were
re-verified against reporting. Used for the granular growth line.

## `pinterest_revenue.csv` — full-year revenue ($M)

| Year | Revenue ($M) | YoY |
| --- | --- | --- |
| 2019 | 1,143 | — |
| 2020 | 1,693 | +48% |
| 2021 | 2,578 | +52% |
| 2022 | 2,803 | +9% |
| 2023 | 3,055 | +9% |
| 2024 | 3,646 | +19% |
| 2025 | 4,222 | +16% |

Revenue grew ~3.7x over 2019–2025 while MAUs grew ~1.85x, so global ARPU
roughly doubled (Pinterest reports global ARPU of $3.81 in 2019 rising to
$7.21 in 2025). FY2025 regional ARPU: US & Canada $30.84, Europe $5.12 —
the same monetisation gap the regional charts show.

## References

- Pinterest Announces Fourth Quarter and Full Year 2025 Results — Nasdaq
  press release: https://www.nasdaq.com/press-release/pinterest-announces-fourth-quarter-and-full-year-2025-results-delivers-14-revenue
- Pinterest Q4: 619M Monthly Users and $1.3B Revenue — Global Dating Insights:
  https://www.globaldatinginsights.com/featured/pinterest-q4-619m-monthly-users-and-1-3b-revenue/
- Pinterest Announces Q4 & FY2025 Results — Morningstar:
  https://www.morningstar.com/news/business-wire/20260212059914/pinterest-announces-fourth-quarter-and-full-year-2025-results-delivers-14-revenue-growth-and-record-users
- Pinterest FY2025 Form 10-K (SEC EDGAR):
  https://www.sec.gov/Archives/edgar/data/1506293/000150629326000021/pins-20251231.htm
- Pinterest Q4 2025 earnings call transcript (regional MAU/revenue/ARPU) —
  Motley Fool:
  https://www.fool.com/earnings/call-transcripts/2026/02/12/pinterest-pins-q4-2025-earnings-call-transcript/
- Pinterest annual revenue history (2019–2025):
  https://www.wallstreetzen.com/stocks/us/nyse/pins/revenue
