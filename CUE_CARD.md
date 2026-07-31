# simple_viz — recording cue card

One page. Glance, don't read. Full wording is in `VIDEO_SCRIPT.md`.
**Before recording:** venv active, inside `Comms_Data_Science`, story GIF
already open in a browser tab, PyPI page open in another tab
(https://pypi.org/project/simple-viz-prashasti/), `pip install -e ".[dev]"` done once.

| # | Cue | Show / run |
| --- | --- | --- |
| 1 | **Motion hook** — "global audience, not global revenue" | play `simple_viz_story.gif` (browser) |
| 2 | **Whole story** — "all on one page" | `open examples/simple_viz_poster.png` |
| 3 | **Real package** — src / data / tests / README | `ls src/simple_viz data tests examples` |
| 4 | **Code + data** — small funcs, real CSVs | `open src/simple_viz/core.py` · `open data/pinterest_revenue.csv` |
| 5 | **Published on PyPI** — show live page, then install | browser: pypi.org/project/simple-viz-prashasti · `pip install simple-viz-prashasti` · `python -c "import simple_viz; print(simple_viz.__all__)"` |
| 6 | **Tested** — "9 tests, all pass" | `python -m pytest -q` |
| 7 | **README** — install / usage / function table | scroll `README.md` |
| 8 | **Fav chart 1: growth_line** — zero base, takeaway title, 2021 annotation | `open examples/simple_viz_02_growth_line.png` |
| 9 | **Fav chart 2: share_gap** — 58% users / 7% revenue, one red bar, direct labels | `open examples/simple_viz_04_share_gap.png` |
| 10 | **Meaning** — revenue ~4× vs users <2×; US user ≈ 35× RoW; grow Europe | `open examples/simple_viz_05_revenue_per_user.png` |
| 11 | **Problem 1** — `twine upload` → **403 Forbidden**; typed `__token__` instead of the real `pypi-` token → made a real token → upload succeeded | show terminal error + `View at:` success |
| 12 | **Problem 2** — `ModuleNotFoundError` / "not a Python project"; wrong folder + env → `cd` in, activate venv, `pip install -e .` | show error, then the fix works |
| 13 | **Close** — "global users, domestic revenue" | (optional) `git log --oneline -8` |

**Numbers:** users 335M→619M (+12%); revenue $1.14B→$4.22B (+16%);
Q4 by region — US&Canada 105M/$979M · Europe 158M/$245M · RoW 356M/$96M.

**After recording:** Zoom cloud → passcode OFF → test link in incognito →
paste in Website URL. Due Fri Jul 31, 11:59 PM PDT.
