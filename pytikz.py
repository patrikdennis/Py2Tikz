import pandas as pd
import numpy as np

class LatexPlotGenerator:
    """
    A class to generate LaTeX code for a plot using pgfplots.
    
    The class accepts data in different formats (pandas DataFrame, dict of arrays/lists,
    or a 2D numpy array/list-of-lists) and generates a LaTeX code file that contains:
      - a filecontents* block with your data (formatted as a space-delimited text file)
      - a tikzpicture environment that uses that data to plot using pgfplots.
      
    Parameters:
        data: The input data. This can be a pandas DataFrame, a dictionary where keys are 
              column names and values are lists/arrays of equal length, or a 2D numpy array (or 
              list-of-lists) if a header is provided.
        data_filename (str): The filename for the data file (e.g., "all_prices.txt").
        latex_filename (str): The output filename for the complete LaTeX code.
        plot_config (dict): Axis options for the tikzpicture (e.g., xlabel, ylabel, title, grid, etc.).
        plot_lines (list of dict): A list of dictionaries specifying:
            - "options": the options for \addplot (e.g., marker style, color, line thickness).
            - "table_x": the name of the column for the x-axis.
            - "table_y": the name of the column for the y-axis.
            - "legend": the legend entry text.
            - Optional "comment": a comment line to annotate the plot command.
            - Optional "data_file": if different from the global data_filename.
        header (list of str, optional): If data is not a DataFrame or dict (e.g. NumPy array or list-of-lists),
              provide the list of column names.
              
    Example usage is shown in the __main__ block.
    """
    
    def __init__(self, data, data_filename, latex_filename, plot_config, plot_lines, header=None):
        self.data = data
        self.data_filename = data_filename
        self.latex_filename = latex_filename
        self.plot_config = plot_config
        self.plot_lines = plot_lines
        self.header = header  # Only used if data is not a DataFrame or dict.

    def generate_data_block(self):
        """
        Generate a LaTeX filecontents* block containing the data.
        The data is formatted as space-delimited text.
        """
        # Case 1: data is a pandas DataFrame
        if isinstance(self.data, pd.DataFrame):
            data_str = self.data.to_csv(sep=' ', index=False)
        
        # Case 2: data is a dictionary (keys: column names, values: lists or arrays)
        elif isinstance(self.data, dict):
            # Create header line.
            header_line = " ".join(self.data.keys())
            # Zip together the values assuming they are all of the same length.
            rows = zip(*[self.data[col] for col in self.data])
            data_lines = "\n".join(" ".join(map(str, row)) for row in rows)
            data_str = header_line + "\n" + data_lines
        
        # Case 3: data is a NumPy array or a list-of-lists. Header must be provided.
        elif isinstance(self.data, (np.ndarray, list)):
            if self.header is None:
                raise ValueError("A header must be provided when data is a numpy array or list-of-lists.")
            header_line = " ".join(self.header)
            # Ensure data is in list-of-lists format.
            if isinstance(self.data, np.ndarray):
                data_list = self.data.tolist()
            else:
                data_list = self.data
            data_lines = "\n".join(" ".join(map(str, row)) for row in data_list)
            data_str = header_line + "\n" + data_lines
        else:
            raise TypeError("Unsupported data type. Provide a pandas DataFrame, dict, or numpy array/list-of-lists.")
        
        block = f"\\begin{{filecontents*}}{{{self.data_filename}}}\n" + data_str + "\n\\end{filecontents*}\n"
        return block

    def generate_tikz_picture(self):
        """
        Generate the LaTeX tikzpicture block with axis options and plot commands.
        """
        # Build the axis options from plot_config.
        axis_options_lines = []
        for key, value in self.plot_config.items():
            axis_options_lines.append(f"      {key}={value},")
        axis_options = "\n".join(axis_options_lines)

        # Construct the tikzpicture and axis environment.
        tikz = ("\\begin{figure}[H]\n"
                "\\centering\n"
                "\\begin{tikzpicture}\n"
                "\\centering\n"
                "  \\begin{axis}[\n")
        tikz += axis_options + "\n"
        tikz += "    ]\n"
        
        # Add each plot line command.
        for line in self.plot_lines:
            if "comment" in line:
                tikz += f"    % {line['comment']}\n"
            # Use a custom data file if provided, otherwise use the global one.
            data_file = line.get("data_file", self.data_filename)
            tikz += (f"    \\addplot[{line['options']}] table [x={line['x']}, y={line['y']}, col sep=space] "
                     f"{{{data_file}}};\n")
            tikz += f"    \\addlegendentry{{{line['legend']}}};\n\n"
        
        tikz += ("  \\end{axis}\n"
                 "\\end{tikzpicture}\n"
                 "\\end{figure}\n")
        return tikz

    def generate_latex_code(self):
        """
        Combine the data block and the tikzpicture block into a single LaTeX code string.
        """
        data_block = self.generate_data_block()
        tikz_block = self.generate_tikz_picture()
        return data_block + "\n" + tikz_block

    def save(self):
        """
        Save the generated LaTeX code to the specified file.
        """
        latex_code = self.generate_latex_code()
        with open(self.latex_filename, 'w') as f:
            f.write(latex_code)
        print(f"LaTeX code saved to {self.latex_filename}")

        
if __name__ == "__main__":
    # Example: using data as a dictionary of lists (this could be results of your computations).
    data = {
        "strike": [40]*10,
        "sigma": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "callFD": [0.004, 0.29242, 1.06188, 2.08275, 3.2205, 4.41231, 5.62518, 6.83953, 8.042, 9.2214],
        "putFD": [9.39796, 9.68638, 10.45584, 11.47671, 12.61459, 13.80728, 15.02293, 16.2429, 17.45411, 18.64514],
        "callMC": [0.00403, 0.28148, 1.03376, 2.03518, 3.14801, 4.32034, 5.54354, 6.75652, 7.93914, 9.08048],
        "putMC": [9.21174, 9.49389, 10.24453, 11.24502, 12.35711, 13.52894, 14.73119, 15.95383, 17.16725, 18.37135]
    }



    # Define axis options for the plot.
    plot_config = {
        "xlabel": "{$\\sigma$}",
        "ylabel": "{Price}",
        "title": "{Crank-Nicolson vs. Monte Carlo Prices (Parameter set 1)}",
        "legend pos": "north west",
        "grid": "major",
        "width": "12cm",
        "height": "8cm",
        "xmin": "0",
        "xmax": "1.1"
    }

    # Define plot lines corresponding to each curve.
    plot_lines = [
        {
            "options": "mark=o, blue, thick, mark size = 3pt",
            "x": "sigma",
            "y": "callFD",
            "legend": "CallFD"
        },
        {
            "comment": "Plot Crank-Nicolson Put Price.",
            "options": "mark=square*, blue!50!black, thick, mark size = 3pt",
            "x": "sigma",
            "y": "putFD",
            "legend": "PutFD"
        },
        {
            "comment": "Plot Monte Carlo Call Price.",
            "options": "mark=+, red!80!black, thick, mark size = 3pt",
            "x": "sigma",
            "y": "callMC",
            "legend": "CallMC"
        },
        {
            "comment": "Plot Monte Carlo Put Price.",
            "options": "mark=+, yellow!80!black, thick, mark size = 3pt",
            "x": "sigma",
            "y": "putMC",
            "legend": "PutMC"
        },
        {
            "comment": "Plot Strike Price.",
            "options": "thick, color=grey",
            "x": "sigma",
            "y": "strike",
            "legend": "Strike Price"
        }
    ]

    # Instantiate the generator.
    generator = LatexPlotGenerator(data, "all_prices.txt", "plot_code.txt", plot_config, plot_lines)
    # Save the generated LaTeX code to the file "plot_code.txt".
    generator.save()

