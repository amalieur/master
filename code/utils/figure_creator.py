""" Sheet that contains methods to draw certain figures """
from matplotlib import pyplot as plt
from matplotlib import colors
import pandas as pd
import numpy as np
import os
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
        ax2.plot(r_sizes, r_runtimes,"o", color=COLOR_TRUE, lw=2)

        degree = 4
        print(data_sizes[:len(r_runtimes)])
        coeffs = np.polyfit(data_sizes[:len(r_runtimes)], r_runtimes, degree)
        p = np.poly1d(coeffs)
        ax2.plot(data_sizes, [p(n) for n in data_sizes], color=COLOR_TRUE, lw=2)

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



def draw_hash_similarity_runtime_logarithmic(path: str, path_to_reference: str = "") -> None:
    """
    Method that draws a figure of the runtime of the hash similarity computation, logarithmic y-scale:

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

    
    rd = reference_data.mean(axis=0)
    r_sizes = rd.index.to_numpy(int)
    r_runtimes = rd.values
    ax.plot(r_sizes, r_runtimes,"or", lw=2)

    degree = 4
    print(data_sizes[:len(r_runtimes)])
    coeffs = np.polyfit(data_sizes[:len(r_runtimes)], r_runtimes, degree)
    p = np.poly1d(coeffs)
    ax.plot(data_sizes, [p(n) for n in data_sizes], color=COLOR_TRUE, lw=2, label="True similarities")

    
    ax.plot(data_sizes, data_runtimes, "xr", lw=2)
    ax.set_xlabel("Dataset size", fontsize=14)
    ax.set_ylabel("Similarity computation time (s)", fontsize=14)

    ax.set_yscale("log")
    ax.tick_params(axis="y")

    degree = 5
    coeffs = np.polyfit(data_sizes, data_runtimes, degree)
    p = np.poly1d(coeffs)
    ax.plot(data_sizes, [p(n) for n in data_sizes], color=COLOR_HASH, lw=2, label="Hash similarities")


    ax.legend(loc="lower right", ncols=3)
    plt.show()



def draw_similarity_correlation(hash_sim_path: str, city: str, hash_type: str, reference_measure: str) -> None:
    """
    Method that draws a similarity correlation graph visualising the correlation between the true similarities and the hashed similarities.
    
    ---
    ### Params:
    hash_sim_path : str (abspath)
        The Path to the csv file containing the hashed similarities
    city : str ("porto" | "rome")
        The city
    hash_type : str ("grid" | "disk")
        The hash method
    reference_measure : str ("dtw" | "frechet")
    """
    # Defining helper functions:

    def _mirrorDiagonal(M: np.ndarray ) -> np.ndarray:
        """Flips and mirrors a two-dimenional np.array """
        return M.values + np.rot90(np.fliplr(M.values))
    
    porto_dtw = _mirrorDiagonal(pd.read_csv(os.path.abspath("./benchmarks/similarities/porto-dtw.csv"), index_col=0)).flatten()
    porto_fre = _mirrorDiagonal(pd.read_csv(os.path.abspath("./benchmarks/similarities/porto-frechet.csv"), index_col=0)).flatten()
    rome_dtw = _mirrorDiagonal(pd.read_csv(os.path.abspath("./benchmarks/similarities/rome-dtw.csv"), index_col=0)).flatten()
    rome_fre = _mirrorDiagonal(pd.read_csv(os.path.abspath("./benchmarks/similarities/rome-frechet.csv"), index_col=0)).flatten()
    
    true_sims = {
        "porto" : {
            "dtw" : porto_dtw,
            "frechet" : porto_fre
        },
        "rome" : {
            "dtw" : rome_dtw,
            "frechet" : rome_fre
        }
    }

    hist_arr = {
        "porto" : {
            "grid" : {
                "dtw" : (np.arange(0, 12, 0.2), np.arange(0, 3, 0.05)),
                "frechet" : (np.arange(0, 12, 0.2), np.arange(0, 0.08, 0.001))
            },
            "disk" : {
                "dtw" : (np.arange(0, 4, 0.05), np.arange(0, 3, 0.05)),
                "frechet" : (np.arange(0, 4, 0.05), np.arange(0, 0.08, 0.001)),
            }
        },
        "rome" : {
            "grid" : {
                "dtw" : (np.arange(0, 15, 0.2), np.arange(0, 6, 0.05)),
                "frechet" : (np.arange(0, 15, 0.2), np.arange(0, 0.10, 0.001))
            },
            "disk" : {
                "dtw" : (np.arange(0, 3, 0.05), np.arange(0, 6, 0.05)),
                "frechet" : (np.arange(0, 3, 0.05), np.arange(0, 0.10, 0.001))
            }
        }
    }

    hash_sim = _mirrorDiagonal(pd.read_csv(hash_sim_path, index_col=0)).flatten()
    corr = np.corrcoef(hash_sim, true_sims[city][reference_measure])[0][1]

    print("Similarity correlation: ", np.corrcoef(hash_sim, true_sims[city][reference_measure])[0][1])

    x = hash_sim

    fig, ax = plt.subplots(figsize=(10,8), dpi=300)

    ax.hist2d(x, true_sims[city][reference_measure], bins=hist_arr[city][hash_type][reference_measure], cmap ="turbo")
    ax.set_ylabel(f"{reference_measure.upper()} distance", fontsize=16)
    ax.set_xlabel(f"{hash_type.capitalize()} scheme distance", fontsize=16)
    ax.tick_params(axis="both", which="major", labelsize=14)
    ax.text(.99, .04, f"{hash_type.capitalize()}/{city.capitalize()} - Correlation: {'{:.2f}'.format(corr)}", ha='right', va='top', transform=ax.transAxes, fontsize=14, color="white" )
    #ax.hist2d(x, true_sims[city]["fre"], bins=hist_arr[city][hash_type]["fre"], cmap="turbo")
  
    plt.show()

if __name__=="__main__":

    hash_sim_porto = os.path.abspath("./code/experiments/similarities/grid_porto.csv")
    dtw_sim_porto = os.path.abspath("./code/benchmarks/similarities/porto-frechet.csv") 

    print(hash_sim_porto)
    print(dtw_sim_porto)

    draw_similarity_correlation(hash_sim_porto, "porto", "grid", "dtw")