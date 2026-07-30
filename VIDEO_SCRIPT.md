# pinviz — demo script (~2 to 2.5 min)

`[SCREEN]` = what to show; **spoken** = read aloud. Lines marked _(trim)_ are
the ones to drop if you need to land exactly at 2:00. Have a terminal open
(venv active, inside `Comms_Data_Science`) plus your editor/GitHub for the
README.

---

## 0 · Intro (0:00–0:12)

**"Hi, I'm Prashasti. This is `pinviz` — a small Python visualization library
I built this term. It turns Pinterest's 2025 results into a set of
communication-first charts, each a deliberate design choice. Let me install
it, import it, and walk through what it shows."**

---

## 1 · Install, import, README (0:12–0:40)

`[SCREEN]` Terminal:
```bash
python -m pip install -e .
python -c "import pinviz; print(pinviz.__all__)"
```
**"I install it in editable mode from the project root, import it, and here's
the public API — five functions: big_number, growth_line, revenue_bar,
share_gap, and arpu_bar."**

`[SCREEN]` Open `README.md`, scroll to the function table.
**"The README has install and usage, and this table maps every function to a
family in the Quantitative Chart Chooser and follows the Evergreen checklist —
that framework is the whole point of the library."**

---

## 2 · Two favorite charts + aesthetic choices (0:40–1:20)

`[SCREEN]` `open examples/pinviz_02_growth_line.png` (press ⌘9 to fit).
**"My first favorite is `growth_line` — Pinterest's users from 2019 to 2025,
hitting a record 619 million. Aesthetic choices: the y-axis starts at zero so
the growth is honest, not exaggerated; the 2021 dip is annotated in plain
language; and the endpoint is labeled directly so the takeaway is unmissable."**

`[SCREEN]` `open examples/pinviz_04_share_gap.png`.
**"My second favorite is `share_gap` — the library's signature chart. It says
the 'so what' right in the title: Rest of World is 58% of users but only 7% of
revenue. Both bars are normalized to 100% for an honest comparison, only Rest
of World is in Pinterest red so color points instead of decorating, and every
value is labeled in place — no legend needed."**

---

## 3 · The story: how Pinterest grew its revenue (1:20–2:00)

`[SCREEN]` `open examples/pinviz_poster.png` (or show revenue_bar + arpu_bar).

**"Here's what the data actually says. Revenue went from about 1.1 billion
dollars in 2019 to 4.2 billion in 2025 — roughly four times bigger. But users
only grew about 1.8 times. So most of the growth didn't come from *more*
users; it came from earning *more per user* — Pinterest's revenue-per-user
roughly doubled."**

**"What changed: Pinterest improved its ad products and added shopping and
commerce features, so advertisers spend more per user, and it started
monetizing internationally — Rest-of-World revenue grew fastest last quarter,
though from a tiny base."** _(trim)_

**"But the growth is lopsided. US and Canada is only 17% of users yet about
74% of revenue — each of those users is worth roughly 35 times a
Rest-of-World user. So the audience is global, but the money is still almost
entirely domestic."**

**"My recommendation from this: the biggest opportunity now is monetizing the
international base — especially Europe, which is more mature — rather than
chasing more users in the already-saturated US. In other words, manage to
revenue-per-user by region, not just total users. The honest caveat is that
the Rest-of-World gap is partly structural, so closing it is a multi-year
effort."** _(trim to one sentence if over time)_

---

## 4 · Two problems and how I solved them (2:00–2:20)

**"Two problems I ran into. First, importing failed with a
ModuleNotFoundError — because the package uses a `src/` layout and I was
running from the wrong folder. The fix was `pip install -e .` from the project
root, which links the package so imports resolve. I actually hit this again
setting up the demo, so it's a real one."**

**"Second, dollar-sign labels like '$4.2B' rendered garbled, because
matplotlib reads text between two dollar signs as LaTeX math. I fixed it with
`text.parse_math = False`, so currency shows literally."**

---

## 5 · Close (2:20–2:30)

**"So that's `pinviz` — installable, importable, built on matplotlib and
pandas, and every chart is a deliberate communication choice that adds up to
one story: Pinterest's audience is global, but its revenue isn't — yet.
Thanks for watching."**

---

### If you need exactly 2:00
Cut the two _(trim)_ lines in §3 and shorten the recommendation to: **"The
opportunity now is monetizing the huge international user base, especially
Europe, rather than chasing more saturated US users."** That keeps the core
story and lands on time.

### Optional flourish (only if under time)
`[SCREEN]` `open -a "Google Chrome" examples/pinviz_story.gif`
**"And here's the whole story animated."** (Open the GIF in a browser so it
plays; Preview won't animate it.)

### On-screen command cheat-sheet
```bash
python -m pip install -e .                          # install
python -c "import pinviz; print(pinviz.__all__)"    # import + API
open examples/pinviz_02_growth_line.png             # favorite chart 1
open examples/pinviz_04_share_gap.png               # favorite chart 2
open examples/pinviz_poster.png                     # the full story
```

### The numbers, for reference (all in data/SOURCES.md)
- Users: 335M (2019) → 619M (2025), +12% YoY.
- Revenue: $1.14B → $4.22B, +16% YoY; global revenue-per-user ~doubled.
- Q4 2025 by region — US & Canada: 105M users / $979M; Europe: 158M / $245M;
  Rest of World: 356M / $96M.
