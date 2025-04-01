import pandas as pd
import numpy as np

class LatexPlotGenerator:
    """
    A class to generate LaTeX code for a plot using pgfplots.

    This version provides a modular, matplotlib-like API:
      - set_title(title): Set the plot title.
      - set_labels(x, y): Set the x and y axis labels.
      - set_legend(legend_pos): Set the legend position.
      - set_grid(option, value): Set the grid option (e.g., "grid", "major").
      - set_figsize(width, height): Set the figure width and height.
      - set_xmin(xmin): Set the minimum x-value.
      - set_xmax(xmax): Set the maximum x-value.
      - set_ymin(ymin): Set the minimum y-value.
      - set_ymax(ymax): Set the maximum y-value.
      
    For plot lines, use:
      - add_plot_line(table_x, table_y, legend, comment="", **line_options): 
          Add a plot line. Extra keyword arguments are interpreted as TikZ plot options.
      
    The class accepts data as a pandas DataFrame, dict, NumPy array, or list-of-lists.
    For NumPy arrays and list-of-lists a header must be provided.
    The generated LaTeX code includes a filecontents* block with the data and a tikzpicture
    environment with the specified axis options and plot commands.
    """

    def __init__(self, data, data_filename, latex_filename, header=None):
        self.data = data
        self.data_filename = data_filename
        self.latex_filename = latex_filename
        self.header = header  # Only used for NumPy arrays or list-of-lists.
        self.axis_options = {}   # Axis options for the plot.
        self.plot_lines = []     # Each plot line is stored as a dict.

    # --- Axis configuration methods ---
    def set_title(self, title):
        """Set the plot title."""
        self.axis_options["title"] = "{" + title + "}"

    def set_labels(self, xlabel, ylabel):
        """Set the x and y axis labels."""
        self.axis_options["xlabel"] = "{" + xlabel + "}"
        self.axis_options["ylabel"] = "{" + ylabel + "}"

    def set_legend(self, legend_pos):
        """Set the legend position (e.g., 'north west')."""
        self.axis_options["legend pos"] = legend_pos

    def set_grid(self, option, value):
        """
        Set a grid option.
        For example, set_grid("grid", "major") sets the grid to 'major'.
        """
        self.axis_options[option] = value

    def set_figsize(self, width, height):
        """Set the figure width and height."""
        self.axis_options["width"] = width
        self.axis_options["height"] = height

    def set_xmin(self, xmin):
        """Set the minimum x-value."""
        self.axis_options["xmin"] = xmin

    def set_xmax(self, xmax):
        """Set the maximum x-value."""
        self.axis_options["xmax"] = xmax

    def set_ymin(self, ymin):
        """Set the minimum y-value."""
        self.axis_options["ymin"] = ymin

    def set_ymax(self, ymax):
        """Set the maximum y-value."""
        self.axis_options["ymax"] = ymax

    # --- Plot line configuration ---
    def add_plot_line(self, table_x, table_y, legend, comment="", **line_options):
        """
        Add a plot line.
        
        Parameters:
          table_x (str): Column name for the x-axis.
          table_y (str): Column name for the y-axis.
          legend (str): The legend entry.
          comment (str): Optional comment.
          **line_options: Additional TikZ plot options (e.g., mark="o", color="blue", thick=True, mark_size="2pt").
          
        Example:
            add_plot_line("sigma", "callFD", "CallFD", mark="o", color="blue", thick=True, mark_size="2pt")
        """
        self.plot_lines.append({
            "table_x": table_x,
            "table_y": table_y,
            "legend": legend,
            "options": line_options,  # stored as dict
            "comment": comment
        })

    def _format_options(self, options):
        """
        Convert the options dictionary into a TikZ options string.
        Boolean True prints just the key; other options print as key=value.
        """
        if not options:
            return ""
        parts = []
        for key, value in options.items():
            if isinstance(value, bool):
                if value:
                    parts.append(f"{key}")
            elif value is None or value == "":
                parts.append(f"{key}")
            else:
                parts.append(f"{key}={value}")
        return ", ".join(parts)

    # --- Data block generation ---
    def generate_data_block(self):
        """
        Generate a LaTeX filecontents* block containing the data.
        The data is formatted as space-delimited text.
        """
        if isinstance(self.data, pd.DataFrame):
            data_str = self.data.to_csv(sep=' ', index=False)
        elif isinstance(self.data, dict):
            header_line = " ".join(self.data.keys())
            rows = zip(*[self.data[col] for col in self.data])
            data_lines = "\n".join(" ".join(map(str, row)) for row in rows)
            data_str = header_line + "\n" + data_lines
        elif isinstance(self.data, (np.ndarray, list)):
            if self.header is None:
                raise ValueError("A header must be provided when data is a numpy array or list-of-lists.")
            header_line = " ".join(self.header)
            data_list = self.data.tolist() if isinstance(self.data, np.ndarray) else self.data
            data_lines = "\n".join(" ".join(map(str, row)) for row in data_list)
            data_str = header_line + "\n" + data_lines
        else:
            raise TypeError("Unsupported data type. Provide a pandas DataFrame, dict, or numpy array/list-of-lists.")

        return f"\\begin{{filecontents*}}{{{self.data_filename}}}\n{data_str}\n\\end{{filecontents*}}\n"

    # --- TikZ picture generation ---
    def generate_tikz_picture(self):
        """
        Generate the LaTeX tikzpicture block with axis options and plot commands.
        """
        axis_opts = "\n".join(f"      {k}={v}," for k, v in self.axis_options.items())
        tikz = (
            "\\begin{figure}[H]\n"
            "\\centering\n"
            "\\begin{tikzpicture}\n"
            "\\centering\n"
            "  \\begin{axis}[\n" +
            axis_opts + "\n"
            "    ]\n"
        )
        for line in self.plot_lines:
            if line.get("comment"):
                tikz += f"    % {line['comment']}\n"
            opts = self._format_options(line.get("options", {}))
            tikz += (
                f"    \\addplot[{opts}] table "
                f"[x={line['table_x']}, y={line['table_y']}, col sep=space] "
                f"{{{self.data_filename}}};\n"
            )
            tikz += f"    \\addlegendentry{{{line['legend']}}};\n\n"
        tikz += (
            "  \\end{axis}\n"
            "\\end{tikzpicture}\n"
            "\\end{figure}\n"
        )
        return tikz

    def generate_latex_code(self):
        """Combine the data block and tikzpicture block into the complete LaTeX code."""
        return self.generate_data_block() + "\n" + self.generate_tikz_picture()

    def save(self):
        """Save the generated LaTeX code to the specified file."""
        latex_code = self.generate_latex_code()
        with open(self.latex_filename, 'w') as f:
            f.write(latex_code)
        print(f"LaTeX code saved to {self.latex_filename}")


if __name__ == "__main__":
    # ==============================
    # Example 1: Using a large pandas DataFrame
    # ==============================
    n_df = 100  # Number of data points
    sigma_df = np.linspace(0.1, 1.0, n_df)
    strike_df = np.full(n_df, 40)
    callFD_df = np.sin(sigma_df) * 10         # Example function for callFD
    putFD_df = np.cos(sigma_df) * 10           # Example function for putFD
    callMC_df = np.log(sigma_df + 1) * 10        # Example function for callMC
    putMC_df = np.sqrt(sigma_df) * 10            # Example function for putMC

    df = pd.DataFrame({
        "strike": strike_df,
        "sigma": sigma_df,
        "callFD": callFD_df,
        "putFD": putFD_df,
        "callMC": callMC_df,
        "putMC": putMC_df
    })

    generator = LatexPlotGenerator(df, "pandas_data.txt", "pandas_plot_code.tex")
    generator.set_title("Large Pandas DataFrame Plot")
    generator.set_labels("{$\\sigma$}", "{Price}")
    generator.set_legend("north west")
    generator.set_grid("grid", "major")
    generator.set_figsize("12cm", "8cm")
    generator.set_xmin("0")
    generator.set_xmax("1.1")
    # (Optionally, you could add set_ymin() and set_ymax() if needed.)

    # Add plot lines with options provided as keyword arguments:
    generator.add_plot_line(
        table_x="sigma",
        table_y="callFD",
        legend="CallFD",
        mark="o",
        #color="blue",
        thick=True,
        mark_size="2pt",
        comment="Plot Crank-Nicolson Call Price (DataFrame)"
    )
    generator.add_plot_line(
        table_x="sigma",
        table_y="putFD",
        legend="PutFD",
        mark="square*",
        color="blue!50!black",
        thick=True,
        mark_size="2pt",
        comment="Plot Crank-Nicolson Put Price (DataFrame)"
    )
    generator.save()

    # ==============================
    # Example 2: Using a large NumPy array
    # ==============================
    n_np = 200  # Number of data points
    sigma_np = np.linspace(0.1, 1.0, n_np)
    strike_np = np.full(n_np, 40)
    callFD_np = np.sin(sigma_np) * 10
    putFD_np = np.cos(sigma_np) * 10
    callMC_np = np.log(sigma_np + 1) * 10
    putMC_np = np.sqrt(sigma_np) * 10

    data_np = np.column_stack((strike_np, sigma_np, callFD_np, putFD_np, callMC_np, putMC_np))
    header_np = ["strike", "sigma", "callFD", "putFD", "callMC", "putMC"]

    generator_np = LatexPlotGenerator(data_np, "numpy_data.txt", "numpy_plot_code.tex", header=header_np)
    generator_np.set_title("Large NumPy Array Plot")
    generator_np.set_labels("{$\\sigma$}", "{Price}")
    generator_np.set_legend("north west")
    generator_np.set_grid("grid", "major")
    generator_np.set_figsize("12cm", "8cm")
    generator_np.set_xmin("0")
    generator_np.set_xmax("1.1")

    generator_np.add_plot_line(
        table_x="sigma",
        table_y="callMC",
        legend="CallMC",
        mark="+",
        color="red",
        thick=True,
        comment="Plot Monte Carlo Call Price (NumPy)"
    )
    generator_np.add_plot_line(
        table_x="sigma",
        table_y="putMC",
        legend="PutMC",
        mark="triangle*",
        color="green",
        thick=True,
        comment="Plot Monte Carlo Put Price (NumPy)"
    )
    generator_np.save()

