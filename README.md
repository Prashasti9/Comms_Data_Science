# simple_viz

A small, friendly wrapper around [matplotlib](https://matplotlib.org/) for
creating common plots with a minimum of boilerplate. `simple_viz` gives you
short, consistent helpers for the charts you reach for most often — line, bar,
scatter, and histogram — while still returning the underlying matplotlib
`Axes` so you can customise the result however you like.

## Installation

Install from a local checkout (uses a `src/` layout):

```bash
pip install .
```

For development, install with the optional test dependencies in editable mode:

```bash
pip install -e ".[dev]"
```

## Usage

```python
import matplotlib.pyplot as plt
import simple_viz as sv

# Line plot
sv.line_plot([1, 2, 3, 4], [10, 20, 15, 30], title="Line", xlabel="x", ylabel="y")

# Bar chart
sv.bar_plot(["a", "b", "c"], [3, 7, 2], title="Bar")

# Scatter plot
sv.scatter_plot([1, 2, 3], [4, 1, 5], title="Scatter")

# Histogram
sv.histogram([1, 1, 2, 3, 3, 3, 4], bins=4, title="Histogram")

plt.show()
```

Every helper returns the matplotlib `Axes` it drew on, so you can keep working
with it:

```python
ax = sv.line_plot([0, 1, 2], [0, 1, 4], title="y = x squared")
ax.grid(True)
ax.legend(["squared"])
```

## API

| Function | Description |
| --- | --- |
| `line_plot(x, y, ...)` | Line plot of `y` against `x`. |
| `bar_plot(categories, values, ...)` | Vertical bar chart. |
| `scatter_plot(x, y, ...)` | Scatter plot of `y` against `x`. |
| `histogram(data, bins=10, ...)` | Histogram of `data`. |

All functions accept the common keyword arguments `title`, `xlabel`, `ylabel`,
and `ax`, and forward any additional keyword arguments to the corresponding
matplotlib method.

## License

Released under the [MIT License](LICENSE).
