# LatexPlotGenerator

**Author:** Patrik Dennis
**Version:** v0.0.1

## Overview

LatexPlotGenerator is a utility class for generating LaTeX code to create publication-ready plots. It automatically creates:

1. A `filecontents*` environment block containing the table data (space-delimited).  
2. A `tikzpicture` environment with an `axis` block and one or more `\addplot[...]` commands.

The end result is a self-contained LaTeX snippet that you can include in your document by simply uploading the `.tex` file in for instance Overleaf and then writing `\input{filename.text}`.

## Key Features

- **Data input:** Accepts `pandas.DataFrame`, Python `dict`, `numpy.ndarray`, or a list-of-lists.
- **Configurable axis options:** Title, labels, legend position, grid, figure size, axis limits, etc.
- **Multiple plot lines:** Each plot line can have its own legend entry and styling options.
- **Easy customization:** Additional TikZ or pgfplots options can be passed as keyword arguments.

---

## Installation

   ```bash
   pip install Py2Tikz
   
   ```

---

## Basic Usage

```python
from Py2Tikz import PyTikzPlot
import pandas as pd

# 1. Prepare your data (e.g., as a pandas DataFrame)
data = pd.DataFrame({
    "x": [0, 1, 2, 3, 4],
    "y": [0, 1, 4, 9, 16],
    "z": [0, 2, 3, 6, 10]
})

# 2. Create an instance of LatexPlotGenerator
generator = PyTikzPlot(
    data=data,
    data_filename="mydata.dat",
    latex_filename="myfigure.tex",
)

# 3. Configure the axis
generator.set_title("My Awesome Plot")
generator.set_labels("X-axis", "Y-axis")
generator.set_legend("north east")
generator.set_grid("grid", "major")
generator.set_figsize("8cm", "6cm")

# 4. Add one or more plot lines
generator.add_plot_line(table_x="x", table_y="y", legend="Quadratic", mark="o")
generator.add_plot_line(table_x="x", table_y="z", legend="Random Values", mark="*", color="red", thick=True)

# 5. (Optional) Adjust axis limits
generator.set_xmin(0)
generator.set_xmax(5)
generator.set_ymin(0)
generator.set_ymax(20)

# 6. Generate and save the LaTeX code
generator.save()
```

---

## Constructor

```python
PyTikzPlot(
    data,
    data_filename,
    latex_filename,
    header=None
)
```

**Parameters**  
- `data`: `pd.DataFrame` | `dict` | `np.ndarray` | `list` of lists  
- `data_filename`: str  
- `latex_filename`: str  
- `header`: list of str (required for array or list-of-lists)

---

## Methods

### set_title(title)
Sets the plot’s title.

### set_labels(xlabel, ylabel)
Sets axis labels.

### set_legend(legend_pos)
Sets legend position.

### set_grid(option, value)
Sets grid options.

### set_figsize(width, height)
Sets figure width and height.

### set_xmin(xmin), set_xmax(xmax), set_ymin(ymin), set_ymax(ymax)
Set axis limits.

### add_plot_line(table_x, table_y, legend, comment="", **line_options)
Adds a line to the plot.

### generate_data_block()
Returns the LaTeX `filecontents*` block.

### generate_tikz_picture()
Returns the `tikzpicture` block.

### generate_latex_code()
Returns the full LaTeX code.

### save()
Writes the LaTeX code to file.

---

## Data Requirements

- **DataFrame:** uses columns as headers.
- **dict:** keys are headers, values are columns.
- **array/list-of-lists:** must provide header.

---

## Example LaTeX Output

```latex
\begin{filecontents*}{mydata.dat}
x y
0 0
1 1
2 4
3 9
4 16
\end{filecontents*}

\begin{figure}[H]
\centering
\begin{tikzpicture}
\centering
  \begin{axis}[
      title={My Plot},
      xlabel={X-axis},
      ylabel={Y-axis},
      legend pos=north east,
      grid=major,
      width=8cm,
      height=6cm,
      xmin=0,
      xmax=5,
      ymin=0,
      ymax=20,
    ]
    \addplot[mark=o] table [x=x, y=y, col sep=space]{mydata.dat};
    \addlegendentry{Quadratic};

  \end{axis}
\end{tikzpicture}
\end{figure}
```

---

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Test your changes.
4. Submit a pull request.

---


Happy plotting!
