
import pandas as pd 
import numpy as np
from pytikz import PytikzPlot 


def main():


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

    generator = PytikzPlot(df, "pandas_data.txt", "pandas_plot_code.tex")
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

    generator_np = PytikzPlot(data_np, "numpy_data.txt", "numpy_plot_code.tex", header=header_np)
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

if __name__ == "__main__":
    main()


