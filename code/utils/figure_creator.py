""" Sheet that contains methods to draw certain figures """
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

COLOR_HASH = "#69b3a2"
COLOR_TRUE = "#3399e6"

def draw_hash_similarity_runtime(path: str, path_to_reference: str = "") -> None:
    """
    Method that draws a figure of the runtime of the hash similarity computation:

    ### Params:
    ---
    path : str (abspath)
        The Path to the csv file containing the runtimes
    path_to_reference_values : str (abspath)
        The Path to the csv file containing the reference runtimes

    """

    timing_data = pd.read_csv(path, index_col=0)
    reference_data = pd.read_csv(path_to_reference, index_col=0) if path_to_reference else None
    
    mean_timing = timing_data.mean(axis=0)
    data_sizes = mean_timing.index.to_numpy(int)
    data_runtimes = mean_timing.values



    fig, ax = plt.subplots(figsize=(10,8), dpi=300)

    if path_to_reference:
        ax2 = ax.twinx()
        rd = reference_data.mean(axis=0)
        r_sizes = rd.index.to_numpy(int)
        r_runtimes = rd.values
        ax2.plot(r_sizes, r_runtimes, color=COLOR_TRUE, lw=2)
        ax2.set_ylabel("True similarity computation time (s)", fontsize=14, color=COLOR_TRUE)
        ax2.tick_params(axis="y", labelcolor=COLOR_TRUE)
    
    ax.plot(data_sizes, data_runtimes, "xr", lw=2)
    ax.set_xlabel("Dataset size", fontsize=14)
    ax.set_ylabel("Hash similarity computation time (s)", fontsize=14, color=COLOR_HASH)
    ax.tick_params(axis="y", labelcolor=COLOR_HASH)

    degree = 4
    coeffs = np.polyfit(data_sizes, data_runtimes, degree)
    p = np.poly1d(coeffs)
    ax.plot(data_sizes, [p(n) for n in data_sizes], color=COLOR_HASH, lw=2)
    plt.show()


