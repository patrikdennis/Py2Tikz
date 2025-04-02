import unittest
import tempfile
import os
import pandas as pd
import numpy as np
from Py2Tikz import PyTikzPlot

class TestLatexPlotGenerator(unittest.TestCase):
    def setUp(self):
        # Temporary file for LaTeX output
        self.temp_latex_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_latex_file.close()
        self.data_filename = "temp_data.txt"

    def tearDown(self):
        if os.path.exists(self.temp_latex_file.name):
            os.remove(self.temp_latex_file.name)
        if os.path.exists(self.data_filename):
            os.remove(self.data_filename)

    def test_generate_data_block_with_dataframe(self):
        df = pd.DataFrame({
            "sigma": [0.1, 0.2, 0.3],
            "callFD": [0.01, 0.02, 0.03]
        })
        generator = PyTikzPlot(df, self.data_filename, self.temp_latex_file.name)
        data_block = generator.generate_data_block()
        self.assertIn("\\begin{filecontents*}", data_block)
        self.assertIn("sigma callFD", data_block)
        self.assertIn("0.1 0.01", data_block)

    def test_generate_data_block_with_dict(self):
        data_dict = {
            "sigma": [0.1, 0.2, 0.3],
            "callFD": [0.01, 0.02, 0.03]
        }
        generator = PyTikzPlot(data_dict, self.data_filename, self.temp_latex_file.name)
        data_block = generator.generate_data_block()
        self.assertIn("sigma callFD", data_block)
        self.assertIn("0.2 0.02", data_block)

    def test_generate_data_block_with_numpy_array(self):
        np_array = np.array([[0.1, 0.01],
                             [0.2, 0.02],
                             [0.3, 0.03]])
        header = ["sigma", "callFD"]
        generator = PyTikzPlot(np_array, self.data_filename, self.temp_latex_file.name, header=header)
        data_block = generator.generate_data_block()
        self.assertIn("sigma callFD", data_block)
        self.assertIn("0.3 0.03", data_block)

    def test_generate_data_block_with_list_of_lists(self):
        data_list = [
            [0.1, 0.01],
            [0.2, 0.02],
            [0.3, 0.03]
        ]
        header = ["sigma", "callFD"]
        generator = PyTikzPlot(data_list, self.data_filename, self.temp_latex_file.name, header=header)
        data_block = generator.generate_data_block()
        self.assertIn("sigma callFD", data_block)
        self.assertIn("0.2 0.02", data_block)

    def test_generate_tikz_picture(self):
        # Create a simple DataFrame.
        df = pd.DataFrame({
            "sigma": [0.1, 0.2, 0.3],
            "callFD": [0.01, 0.02, 0.03]
        })
        generator = PyTikzPlot(df, self.data_filename, self.temp_latex_file.name)
        # Set some axis options via methods.
        generator.set_title("Test Plot")
        generator.set_labels("{$\\sigma$}", "{Price}")
        generator.set_legend("north west")
        generator.set_grid("grid", "major")
        generator.set_figsize("12cm", "8cm")
        generator.set_xmin("0")
        generator.set_xmax("1.1")
        # Add a plot line.
        generator.add_plot_line("sigma", "callFD", "CallFD", comment="Test Plot Line", mark="o", color="blue", thick=True, mark_size="3pt")
        tikz_code = generator.generate_tikz_picture()
        self.assertIn("\\begin{tikzpicture}", tikz_code)
        self.assertIn("\\addplot", tikz_code)
        self.assertIn("table [x=sigma, y=callFD", tikz_code)
        self.assertIn("\\addlegendentry{CallFD}", tikz_code)

    def test_save_functionality(self):
        data_dict = {
            "sigma": [0.1, 0.2, 0.3],
            "callFD": [0.01, 0.02, 0.03]
        }
        generator = PyTikzPlot(data_dict, self.data_filename, self.temp_latex_file.name)
        generator.set_title("Test Plot")
        generator.set_labels("{$\\sigma$}", "{Price}")
        generator.set_legend("north west")
        generator.set_grid("grid", "major")
        generator.add_plot_line("sigma", "callFD", "CallFD", comment="Test Plot Line", mark="o", color="blue", thick=True, mark_size="3pt")
        generator.save()
        with open(self.temp_latex_file.name, 'r') as f:
            content = f.read()
        self.assertIn("\\begin{filecontents*}", content)
        self.assertIn("\\begin{tikzpicture}", content)

    def test_invalid_data_type(self):
        with self.assertRaises(TypeError):
            generator = PyTikzPlot(123, self.data_filename, self.temp_latex_file.name)
            generator.generate_data_block()

    def test_numpy_without_header(self):
        np_array = np.array([[0.1, 0.01], [0.2, 0.02]])
        with self.assertRaises(ValueError):
            generator = PyTikzPlot(np_array, self.data_filename, self.temp_latex_file.name)
            generator.generate_data_block()

if __name__ == "__main__":
    unittest.main()

