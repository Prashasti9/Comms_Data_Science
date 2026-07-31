# simple_viz — demo script (~2:30–3:00)

Video-only submission, so **show the real work**. Show while you talk; don't
read code line by line. **[DO]** = on screen · **[SAY]** = say it. Terminal
open (venv active, inside `Comms_Data_Science`) + editor + a browser.

Published on PyPI: **https://pypi.org/project/simple-viz-prashasti/**

---

**0:00 — Hook (motion first)**
**[DO]** Play `examples/simple_viz_story.gif` in a browser (`open -a "Google Chrome" examples/simple_viz_story.gif`).
**[SAY]** "Pinterest has a global audience — but its revenue is not global.
That's the story my Python library, `simple_viz`, tells."

**0:08 — The whole story on one page**
**[DO]** `open examples/simple_viz_poster.png`.
**[SAY]** "Here's all of it on one page. Now let me show the library behind it."

**0:18 — This is a real package (structure)**
**[DO]** Show the editor sidebar (or `ls src/simple_viz data tests examples`).
**[SAY]** "It's a proper package — code in `src/simple_viz`, data as CSVs,
tests, a README, and packaging in `pyproject.toml`."

**0:32 — The code + the data**
**[DO]** `open src/simple_viz/core.py` (scroll once), then `open data/pinterest_revenue.csv`.
**[SAY]** "Small functions — DataFrame in, matplotlib figure out. The data's
real: I took Pinterest's 2025 users and revenue from their earnings release
and SEC filing and stored them in these CSVs."

**0:48 — It's published on PyPI**
**[DO]** Browser: open **https://pypi.org/project/simple-viz-prashasti/** (show the live page). Then terminal:
```bash
pip install simple-viz-prashasti
python -c "import simple_viz; print(simple_viz.__all__)"
```
**[SAY]** "I published it to PyPI — here's the live page. Anyone can install it
with `pip install simple-viz-prashasti` and then `import simple_viz`. Five
functions, built on pandas and matplotlib."
> Tip: it may say "already satisfied" since it's installed. For a clean
> download on camera, run it in a fresh venv:
> `python -m venv /tmp/demo && source /tmp/demo/bin/activate && pip install simple-viz-prashasti`,
> then `deactivate` and `source .venv/bin/activate` to continue.

**1:04 — Tests pass**
**[DO]** `python -m pytest -q`.
**[SAY]** "It's tested — nine tests confirm every function runs on the real
data and returns a figure. All passing."

**1:16 — README**
**[DO]** Scroll `README.md` to the function table.
**[SAY]** "The README has install, usage, and each function next to the
question it answers."

**1:26 — Favorite chart #1: growth_line**
**[DO]** `open examples/simple_viz_02_growth_line.png`.
**[SAY]** "First favorite — the growth line, the right chart for change over
time. Users reach a record 619 million. Zero baseline so the growth is honest,
a takeaway title, and the 2021 dip annotated."

**1:44 — Favorite chart #2: share_gap**
**[DO]** `open examples/simple_viz_04_share_gap.png`.
**[SAY]** "Second favorite — the split. Rest of World is 58% of users but 7%
of revenue. One category in red points to the mismatch; values labelled
directly."

**2:02 — What it means**
**[DO]** `open examples/simple_viz_05_revenue_per_user.png`.
**[SAY]** "Revenue nearly quadrupled while users didn't double — so Pinterest
earns more per user, but unevenly. A US user is worth about 35 times a
Rest-of-World user. The opportunity is monetising internationally, especially
Europe."

**2:18 — Two problems I hit (show the terminal)**
See the two problems below — show the error, then the fix.

**2:42 — Close**
**[SAY]** "That's `simple_viz` — published on PyPI, tested, and telling one
story: Pinterest's audience is global, its revenue isn't. Thanks."

---

## The two problems (genuine — you actually hit these; both have error text you can show)

### Problem 1 — PyPI upload rejected: `403 Forbidden`
**[DO]** Show the terminal where `twine upload` printed `ERROR HTTPError: 403 Forbidden`, then the successful retry ending in `View at: https://pypi.org/project/simple-viz-prashasti/0.1.0/`.
**[SAY]** "When I first ran `twine upload`, PyPI rejected it with a 403
Forbidden. The prompt said 'Enter your API token' and I typed `__token__` —
but newer twine wants the token *value* there, not the word `__token__`, which
is only the username in the old flow. Once I enabled two-factor auth, created
a real API token, and pasted the actual `pypi-` token, the upload went through
and the package went live."

### Problem 2 — `ModuleNotFoundError` / "not a Python project"
**[DO]** From your home folder run `pip install -e .` → show the error `does not appear to be a Python project`, and/or `import simple_viz` → `ModuleNotFoundError`. Then `cd Comms_Data_Science`, `source .venv/bin/activate`, run it again → works.
**[SAY]** "Early on, `pip install` failed with 'not a Python project,' and
import threw ModuleNotFoundError — because the package uses a `src` layout and
I was in the wrong folder, in the wrong environment. Fix: `cd` into the project
root, activate the virtual environment, and install with `pip install -e .` —
that links the package so imports resolve."

> **Alternative code problem** (swap in if you'd rather show a library bug):
> dollar-sign labels like `$4.2B` rendered as garbled LaTeX, because matplotlib
> reads text between two `$` as math. Fixed with `plt.rcParams["text.parse_math"] = False`
> set once in `theme.py`.

---

### On-screen commands (in order)
```bash
open -a "Google Chrome" examples/simple_viz_story.gif
open examples/simple_viz_poster.png
ls src/simple_viz data tests examples
open src/simple_viz/core.py
pip install simple-viz-prashasti
python -c "import simple_viz; print(simple_viz.__all__)"
python -m pytest -q
open examples/simple_viz_02_growth_line.png
open examples/simple_viz_04_share_gap.png
open examples/simple_viz_05_revenue_per_user.png
```

### Numbers for reference
- Users 335M (2019) → 619M (2025), +12% YoY.
- Revenue $1.14B → $4.22B, +16% YoY (grew ~4×; users grew <2×).
- Q4 2025 by region — US & Canada 105M / $979M · Europe 158M / $245M ·
  Rest of World 356M / $96M.
