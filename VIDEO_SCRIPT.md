# simple_viz — 2-minute demo script

Punchy on purpose: short lines, show more than you say. **[DO]** = action on
screen · **[SAY]** = say it out loud. Terminal open (venv active, inside
`Comms_Data_Science`), plus your editor/GitHub for the README.

---

**0:00 — Intro**
**[SAY]** "Hi, I'm Prashasti. This is `simple_viz` — a small Python library
that turns Pinterest's 2025 numbers into charts that make a point."

**0:10 — Install + import**
**[DO]**
```bash
python -m pip install -e .
python -c "import simple_viz; print(simple_viz.__all__)"
```
**[SAY]** "Install it, import it — five functions."

**0:25 — Where the data came from**
**[SAY]** "The numbers are real. I took Pinterest's 2025 users and revenue
from their earnings release and their SEC filing, put them in small CSV files,
and the library reads them with pandas — no scraping, no API."

**0:40 — README**
**[DO]** Scroll `README.md`.
**[SAY]** "The README has install, usage, and each function next to the
question it answers."

**0:52 — Favorite chart #1: growth_line**
**[DO]** `open examples/simple_viz_02_growth_line.png` (⌘9 to fit).
**[SAY]** "First favorite — the growth line. Users hit a record 619 million.
It starts at zero so the rise is honest, and I annotated the 2021 dip so the
chart explains itself."

**1:12 — Favorite chart #2: share_gap**
**[DO]** `open examples/simple_viz_04_share_gap.png`.
**[SAY]** "Second favorite — the split. Rest of World is 58% of the users but
7% of the revenue. One red bar carries the eye; the gap is the whole story."

**1:30 — The story: how revenue grew**
**[DO]** `open examples/simple_viz_poster.png`.
**[SAY]** "The big picture: revenue nearly quadrupled to 4.2 billion while
users didn't even double — so Pinterest is earning far more *per user*. But
it's lopsided: a US user is worth about 35 times a Rest-of-World user. My
take — the growth lever now is monetizing that huge international audience,
especially Europe, not squeezing the saturated US."

**1:52 — Two problems I hit**
**[SAY]** "Two problems. One: `import` failed until I installed from the
project root with `pip install -e .` — I hit that again today. Two: dollar
signs rendered as math until I turned off matplotlib's math parsing."

**2:08 — Close**
**[SAY]** "That's `simple_viz` — built on matplotlib and pandas, one clear
story: Pinterest's audience is global, its revenue isn't. Thanks."

---

### Trim to land at exactly 2:00
Shorten the story line to: **"Revenue nearly quadrupled while users didn't
double — so it's about earning more per user, and a US user is worth ~35× a
Rest-of-World one. The opportunity is monetizing internationally, especially
Europe."**

### Optional 5-second flourish (only if under time)
**[DO]** `open -a "Google Chrome" examples/simple_viz_story.gif`
**[SAY]** "…and the whole story, animated." (Use a browser — Preview won't
animate a GIF.)

### On-screen commands
```bash
python -m pip install -e .
python -c "import simple_viz; print(simple_viz.__all__)"
open examples/simple_viz_02_growth_line.png
open examples/simple_viz_04_share_gap.png
open examples/simple_viz_poster.png
```

### Numbers for reference
- Users 335M (2019) → 619M (2025), +12% YoY.
- Revenue $1.14B → $4.22B, +16% YoY (grew ~4×; users grew <2×).
- Q4 2025 by region — US & Canada 105M / $979M · Europe 158M / $245M ·
  Rest of World 356M / $96M.
