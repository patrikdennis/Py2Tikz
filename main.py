from pytikz import LatexPlotGenerator

if __name__ == "__main__":
    import pandas as pd
    import numpy as np

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

    plot_config_df = {
        "xlabel": r"{$\sigma$}",
        "ylabel": "{Price}",
        "title": "{Large Pandas DataFrame Plot}",
        "legend pos": "north west",
        "grid": "major",
        "width": "12cm",
        "height": "8cm",
        "xmin": "0",
        "xmax": "1.1"
    }

    plot_lines_df = [
        {
            "comment": "Plot Crank-Nicolson Call Price (DataFrame).",
            "options": "mark=o, blue, thick, mark size=2pt",
            "x": "sigma",
            "y": "callFD",
            "legend": "CallFD"
        },
        {
            "comment": "Plot Crank-Nicolson Put Price (DataFrame).",
            "options": "mark=square*, blue!50!black, thick, mark size=2pt",
            "x": "sigma",
            "y": "putFD",
            "legend": "PutFD"
        }
    ]

    # Instantiate and save LaTeX code for the DataFrame example.
    generator_df = LatexPlotGenerator(df, "pandas_data.txt", "pandas_plot_code.txt", plot_config_df, plot_lines_df)
    generator_df.save()


    # ==============================
    # Example 2: Using a large NumPy array
    # ==============================
    n_np = 200  # Number of data points
    sigma_np = np.linspace(0.1, 1.0, n_np)
    strike_np = np.full(n_np, 40)
    callFD_np = np.sin(sigma_np) * 10         # Example function for callFD
    putFD_np = np.cos(sigma_np) * 10           # Example function for putFD
    callMC_np = np.log(sigma_np + 1) * 10        # Example function for callMC
    putMC_np = np.sqrt(sigma_np) * 10            # Example function for putMC

    # Combine columns into a large NumPy array (each row represents one data point).
    data_np = np.column_stack((strike_np, sigma_np, callFD_np, putFD_np, callMC_np, putMC_np))
    header_np = ["strike", "sigma", "callFD", "putFD", "callMC", "putMC"]

    plot_config_np = {
        "xlabel": r"{$\sigma$}",
        "ylabel": "{Price}",
        "title": "{Large NumPy Array Plot}",
        "legend pos": "north west",
        "grid": "major",
        "width": "12cm",
        "height": "8cm",
        "xmin": "0",
        "xmax": "1.1"
    }

    plot_lines_np = [
        {
            "comment": "Plot Monte Carlo Call Price (NumPy).",
            "options": "mark=+, red, thick, mark size=2pt",
            "x": "sigma",
            "y": "callMC",
            "legend": "CallMC"
        },
        {
            "comment": "Plot Monte Carlo Put Price (NumPy).",
            "options": "green, thick, mark size=2pt",
            "x": "sigma",
            "y": "putMC",
            "legend": "PutMC"
        }
    ]

    # Instantiate and save LaTeX code for the NumPy array example.
    generator_np = LatexPlotGenerator(data_np, "numpy_data.txt", "numpy_plot_code.txt", plot_config_np, plot_lines_np, header=header_np)
    generator_np.save()

