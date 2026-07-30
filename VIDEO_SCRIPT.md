# simple_viz — demo script (~2:30–3:00)

Video-only submission, so **show the real work**, not just the charts. Keep it
moving — show while you talk, don't read code line by line. **[DO]** = on
screen · **[SAY]** = say it. Terminal open (venv active, inside
`Comms_Data_Science`) + your editor with the project open.

---

**0:00 — Hook**
**[DO]** `simple_viz_04_share_gap.png` full-screen.
**[SAY]** "Pinterest has a global audience — but its revenue is not global.
That's the story my Python library, `simple_viz`, makes clear."

**0:12 — This is a real package (structure)**
**[DO]** Show the file tree in your editor sidebar (or run `ls src/simple_viz data tests examples`).
**[SAY]** "It's a proper package. `src/simple_viz` holds the code —
`core.py` has the five chart functions, `theme.py` has the shared colours and
styling. There's a `data` folder with the real numbers as CSVs, a `tests`
folder, a README, and packaging in `pyproject.toml`."

**0:32 — The code + the data**
**[DO]** Open `src/simple_viz/core.py`, scroll once; then open one CSV, e.g. `data/pinterest_revenue.csv`.
**[SAY]** "Each function is small — takes a pandas DataFrame, returns a
matplotlib figure, one job each. And the data is real: I took Pinterest's 2025
users and revenue from their earnings release and SEC filing and stored them
in these CSVs — no scraping, no API."

**0:50 — Install + import**
**[DO]**
```bash
python -m pip install -e .
python -c "import simple_viz; print(simple_viz.__all__)"
```
**[SAY]** "I install it in editable mode from the project root, import it, and
there are the five functions — built with pandas and matplotlib."

**1:02 — Tests pass**
**[DO]**
```bash
python -m pytest -q
```
**[SAY]** "It's tested too — nine tests confirm every function runs on the real
data and returns a figure, plus the two calculations the library does itself.
All passing."

**1:14 — README**
**[DO]** Scroll `README.md` to the function table.
**[SAY]** "The README has install, usage, and each function next to the
question it answers."

**1:12 — Favorite chart #1: growth_line**
**[DO]** `open examples/simple_viz_02_growth_line.png`.
**[SAY]** "First favorite — the growth line, the right chart for change over
time. Users reach a record 619 million. It starts at zero so the growth is
honest, the title states the takeaway, and I annotated the 2021 dip so viewers
don't have to guess."

**1:32 — Favorite chart #2: share_gap**
**[DO]** `open examples/simple_viz_04_share_gap.png`.
**[SAY]** "Second favorite — the split. Rest of World is 58% of users but only
7% of revenue. One category is in Pinterest red and everything else is grey,
so colour points to the mismatch, and the values are labelled directly."

**1:52 — What it means**
**[DO]** `open examples/simple_viz_poster.png`.
**[SAY]** "Together: revenue nearly quadrupled while users didn't double — so
Pinterest earns far more per user, but unevenly. A US user is worth about 35
times a Rest-of-World user. The opportunity is international monetisation,
especially Europe."

**2:08 — Two problems I solved**
**[SAY]** "Two problems. One: Python couldn't find the package because of the
`src` layout — installing with `pip install -e .` from the project root fixed
it. Two: matplotlib read dollar signs as math, so I disabled math parsing once
in the shared theme."

**2:24 — Close**
**[DO]** (optional) `git log --oneline -8` to show the build history.
**[SAY]** "And the git history shows it came together step by step. That's
`simple_viz` — one clear story: Pinterest's audience is global, its revenue
isn't. Thanks."

---

### If you need to cut time
Drop the git-history line at the end, and shorten the "what it means" beat to:
**"Revenue nearly quadrupled while users didn't double, and a US user is worth
~35× a Rest-of-World user — so the opportunity is monetizing internationally,
especially Europe."** Keep the structure, code, data, and test beats — those
are your proof-of-work and worth the extra seconds in a video-only submission.

### On-screen commands (in order)
```bash
ls src/simple_viz data tests examples           # structure
open src/simple_viz/core.py                      # (or show in editor) the code
python -m pip install -e ".[dev]"                # install (with test deps)
python -c "import simple_viz; print(simple_viz.__all__)"   # import + API
python -m pytest -q                              # tests → 9 passed
open examples/simple_viz_02_growth_line.png      # favorite chart 1
open examples/simple_viz_04_share_gap.png        # favorite chart 2
open examples/simple_viz_poster.png              # the full story
git log --oneline -8                             # build history (optional)
```
Note: install with `".[dev]"` (quotes matter in zsh) so `pytest` is available.

### Numbers for reference
- Users 335M (2019) → 619M (2025), +12% YoY.
- Revenue $1.14B → $4.22B, +16% YoY (grew ~4×; users grew <2×).
- Q4 2025 by region — US & Canada 105M / $979M · Europe 158M / $245M ·
  Rest of World 356M / $96M.
