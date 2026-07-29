# pinviz — 2-minute demo script

Target length ~2:00. `[SCREEN]` = what to show; **spoken** = read aloud.
Have a terminal and your editor open, cwd = project root.

---

## 0 · Intro (0:00–0:12)

**"Hi, I'm Prashasti. This is `pinviz` — a small Python visualization
library I built this term. It makes communication-first charts that tell one
data story: Pinterest's 2025 results. Let me install it, import it, and show
you around."**

---

## 1 · Install, import, README (0:12–0:45)

`[SCREEN]` Terminal — run:

```bash
python -m pip install -e .
python -c "import pinviz; print(pinviz.__all__)"
```

**"I install it in editable mode from the project root, then import it — and
here's the public API: five functions, `big_number`, `growth_line`,
`revenue_bar`, `share_gap`, and `arpu_bar`."**

`[SCREEN]` Open `README.md`, scroll slowly to the function table.

**"The README has install and usage, and this table — every function maps to
a family in the Quantitative Chart Chooser and follows the Evergreen Data
Visualization Checklist. That framework is the whole point of the library."**

---

## 2 · Two favorite visualizations + aesthetic choices (0:45–1:30)

`[SCREEN]` Show `examples/pinviz_04_share_gap.png`.

**"My first favorite is `share_gap`. It answers 'so what?' in the title —
'Rest of World is 58% of users but just 7% of revenue.' Three aesthetic
choices: one — I normalize both bars to 100% so it's an honest part-to-whole
comparison. Two — only Rest of World is Pinterest red; everything else is
grey, so color does the pointing instead of decorating. Three — the values
are labeled right on the bars, so there's no legend and no busy axis."**

`[SCREEN]` Show `examples/pinviz_02_growth_line.png`.

**"My second favorite is `growth_line`. Choices: the y-axis starts at zero,
so the growth is honest, not exaggerated. There's a single annotation on the
2021 dip explaining *why* users fell — the chart teaches, not just plots. And
the endpoint is labeled 619M directly, so the takeaway is unmissable. Same
system throughout: one red, takeaway titles, no chartjunk."**

---

## 3 · Two problems and how I solved them (1:30–1:55)

**"Two problems I ran into. First — packaging. `import pinviz` threw
`ModuleNotFoundError` because I use the modern `src/` layout, so Python
couldn't find it until it was installed. The fix was `pip install -e .` run
from the project root — that links the package so imports resolve and edits
apply live."**

**"Second — a rendering bug. Dollar-sign labels like `$4.2B` came out
garbled, because matplotlib read the text between two dollar signs as a LaTeX
math expression. I fixed it by setting `text.parse_math = False`, so dollar
signs render as plain text."**

---

## 4 · Close (1:55–2:00)

**"So that's `pinviz` — installable, importable, and every chart is a
deliberate communication choice. Thanks for watching."**

---

### Backup problems (if you prefer different ones)
- **Card layers painted over the charts** (poster) → drew cards into a
  dedicated background axes with negative z-order.
- **Region labels overflowed** between side-by-side panels → restructured
  into full-width stacked panels so labels always sit inside their card.

### On-screen command cheat-sheet
```bash
python -m pip install -e .                       # install
python -c "import pinviz; print(pinviz.__all__)" # import + API
python examples/pinviz_gallery.py                # regenerate the 5 charts
```
