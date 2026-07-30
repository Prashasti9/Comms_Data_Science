# Pinterest's split screen — what the visualization is *for*

## The one question it answers

Pinterest has a huge, fast-growing global audience. **Is it turning that
audience into money evenly — and if not, where is the opportunity?**

Raw earnings numbers (619M users, $4.2B revenue) sound like an unqualified
success. The visualization reframes them into the real strategic story:
**strong top-line growth hides a severe geographic monetization imbalance.**

## What each chart contributes to the argument

| Chart | Chart type | What it establishes |
| --- | --- | --- |
| Users over time | Change over time | Scale & momentum — 619M MAU, +12% YoY, durable growth |
| Revenue over time | Change over time | Revenue grew ~3.7x since 2019 vs users ~1.85x → monetization is improving (global ARPU $3.81 → $7.21) |
| Users vs revenue by region | Part-to-whole | **The core tension:** Rest of World = 58% of users but 7% of revenue |
| Revenue by region | Comparison | US & Canada ($979M) dwarfs Rest of World ($96M) despite far fewer users |
| Revenue per user | Ratio | The mechanism: a US & Canada user is worth ~35x a Rest-of-World user |

The order matters: growth (good news) → the split (the twist) → the
per-user mechanism (the explanation). That arc *is* the communication.

## What stakeholders should infer

1. **The growth engine and the revenue engine are in different places.**
   New users are increasingly international; revenue is still overwhelmingly
   domestic (US & Canada = 17% of users but ~74% of revenue).
2. **The biggest opportunity is monetization, not acquisition.** 356M
   Rest-of-World users generate almost nothing today. Lifting their revenue
   per user even slightly outweighs squeezing more users out of the
   already-saturated, already-high-ARPU US market.
3. **Europe is the realistic near-term lever.** 26% of users, 19% of
   revenue, ARPU $5.12 — mature enough to close the gap faster than Rest of
   World, which faces structural ad-market limits.

## Business decisions this supports

- **Shift investment toward monetization infrastructure in Rest of World
  and Europe** (ad-sales presence, advertiser tooling, local ad demand,
  shopping/commerce features) rather than pure user-growth spend in the US.
- **Manage to ARPU-by-region targets, not just MAU.** Adding users in
  low-ARPU regions can *dilute* blended ARPU, so a MAU-only goal can mask
  weakening economics.
- **Investor framing:** "durable, increasingly international user growth +
  a multi-year monetization runway." The Rest-of-World gap is upside, not
  just a weakness.
- **Advertiser framing:** Rest of World offers cheap, uncontested reach for
  brands willing to be early.

## Honest caveats (say these out loud)

- The Rest-of-World ARPU gap is partly **structural** — weaker digital-ad
  markets and lower purchasing power — so closing it is a multi-year effort,
  not a quick win.
- The regional revenue-per-user figures on the poster are **implied**
  (Q4 revenue ÷ period MAU); Pinterest's officially reported full-year ARPU
  ($30.84 US & Canada, $5.12 Europe, $7.21 global) tells the same story and
  is cited in `data/SOURCES.md`.

## Data & provenance

All figures are real, from Pinterest's Q4 & Full-Year 2025 report (Feb 12,
2026) and its 10-K. Numbers were transcribed into CSVs under `data/` and
loaded with `pandas.read_csv` — no live API. Full source links are in
[`data/SOURCES.md`](data/SOURCES.md).
