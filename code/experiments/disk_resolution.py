"""
This file contains methods for finding an optimal/working number of disks and their diameter / layers

Each experiment will be run in 20 parallell jobs
"""
# Importing nescessary modules

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from multiprocessing import Pool

from utils import file_handler as fh
from utils import metafile_handler as mfh

from schemes.disk_lsh import DiskLSH

from utils.similarity_measures.distance import py_edit_distance as py_ed
from utils.similarity_measures.distance import py_dtw


# Defining helper functions:

def _mirrorDiagonal(M: np.ndarray ) -> np.ndarray:
    """Flips and mirrors a two-dimenional np.array """
    return M.values + np.rot90(np.fliplr(M.values))

# True similarities:

P_DTW = _mirrorDiagonal(pd.read_csv("./benchmarks/similarities/porto-dtw-test.csv", index_col=0)).flatten() #.stack().values
P_FRE = _mirrorDiagonal(pd.read_csv("./benchmarks/similarities/porto-frechet-test.csv", index_col=0)).flatten() #.stack().values

R_DTW = _mirrorDiagonal(pd.read_csv("./benchmarks/similarities/rome-dtw-test.csv", index_col=0)).flatten() #.stack().values
R_FRE = _mirrorDiagonal(pd.read_csv("./benchmarks/similarities/rome-frechet-test.csv", index_col=0)).flatten() #.stack().values

# Some constants

PORTO_CHOSEN_DATA = "../data/chosen_data/porto/"
PORTO_HASHED_DATA = "../data/hashed_data/grid/porto/"
PORTO_META_TEST = "../data/hashed_data/grid/porto/META-50.TXT"

P_MAX_LON = -8.57
P_MIN_LON = -8.66
P_MAX_LAT = 41.19
P_MIN_LAT = 41.14

ROME_CHOSEN_DATA = "../data/chosen_data/rome/"
ROME_HASHED_DATA = "../data/hashed_data/grid/rome/"
ROME_META_TEST = "../data/hashed_data/grid/rome/META-50.TXT"

R_MAX_LON = 12.53
R_MIN_LON = 12.44
R_MAX_LAT = 41.93
R_MIN_LAT = 41.88

MEASURE = {
    "py_ed" : py_ed,
    "py_dtw" : py_dtw,
}

REFERENCE = {
    "portodtw" : P_DTW,
    "portofrechet" : P_FRE,
    "romedtw" : R_DTW,
    "romefrechet" : R_FRE
}

DISTANCE_FUNC = {
    "py_ed" : "ED",
    "py_dtw" : "DTW",
}


def _constructDisk(city: str, diameter: float, layers: int, disks:int=50) -> DiskLSH:
    """ Constructs a grid hash object over the given city """
    if city.lower() == "porto":
        return DiskLSH(f"GP_{layers}-{'{:.2f}'.format(diameter)}", P_MIN_LAT, P_MAX_LAT, P_MIN_LON, P_MAX_LON, disks, layers, diameter, PORTO_META_TEST, PORTO_CHOSEN_DATA)
    elif city.lower() == "rome":
        return DiskLSH(f"GR_{layers}-{'{:.2f}'.format(diameter)}", R_MIN_LAT, R_MAX_LAT, R_MIN_LON, R_MAX_LON, disks, layers, diameter, ROME_META_TEST, ROME_CHOSEN_DATA)
    else:
        raise ValueError("City argument must be either porto or rome")


def _compute_hashes(disk: DiskLSH, measure: str = "py_ed") -> dict[str,list]:
    if measure == "py_ed":
        return disk.compute_dataset_hashes_with_KD_tree() 
    elif measure == "py_dtw": 
        return disk.compute_dataset_hashes_with_KD_tree_numerical()
    else:
        raise ValueError("Preferred similarity measure not supported")
    

def _fun_wrapper_corr(args):
    city, dia, lay, measure, reference = args
    Disk = _constructDisk(city, dia, lay)
    hashes = _compute_hashes(Disk, measure)

    edits = _mirrorDiagonal(MEASURE[measure](hashes)).flatten()
    corr = np.corrcoef(edits, REFERENCE[city.lower()+reference.lower()])[0][1]
    return corr



def _compute_disk_diameter_layers(city: str, layers: list[int], diameter: list[float], measure: str = "py_dtw", reference: str = "dtw", parallell_jobs: int = 20 ):
    """ Computations for the visualisation """
    
    pool = Pool()

    results = []
    for lay in layers:
        result = []
        for dia in np.arange(*diameter):
            print(f"L: {lay}", "{:.2f}".format(dia), end="\r")
            #edits = _mirrorDiagonal(MEASURE[measure](hashes)).flatten()

            #corr = np.corrcoef(edits, REFERENCE[city.lower()+reference.lower()])[0][1]
            corrs = pool.map(_fun_wrapper_corr, [(city, dia, lay, measure, reference) for _ in range(parallell_jobs)])
            corr = np.average(np.array(corrs) )
            std = np.std(np.array(corrs))
            result.append([corr, dia, std])
        
        results.append([result, lay])

    return results




def plot_disk_dia_layers(city: str, layers: list[int], diameter: list[float], measure: str = "py_dtw", reference: str = "dtw", parallell_jobs: int = 20 ):
    """ Visualises the 'optimal' values for resolution and layers for the grid hashes 
    
    Param
    ---
    city : str
        Either "porto" or "rome", throws error unless
    layers : list[int]
        The layers that will be visualised -> [x, y, z...]
    resolution : list[float]
        The resolution that will be visualised -> [min, max, step]
    measure : str (default py_edp)
        The measure that will be used. Either edit distance or dtw -> "py_ed" or "py_edp"
    reference : str (default dtw)
        The true similarities that will be used as reference. Either dtw or frechet
    paralell_jobs : int (default 20)
        Yhe number of parallell jobs that will create the data foundation
    """

    results = _compute_disk_diameter_layers(city, layers, diameter, measure, reference, parallell_jobs)
   

    fig, ax1 = plt.subplots(figsize=(10,8), dpi=300)
    ax2 = ax1.twinx()
    #fig.set_size_inches(10,8)
    cmap = plt.get_cmap('gist_ncar')
    N = len(results) 
    

    for layer_element in results:
        corrs, layer = layer_element
        
        corre, dia, std = list(zip(*corrs))
        corre = np.array(corre)
        dia = np.array(dia)
        std = np.array(std)
        ax1.plot(dia, corre, c=cmap(float(layer-1)/(1.2*N)), label=f"{layer} layers", lw=2)
        ax2.plot(dia, std, c=cmap(float(layer-1)/(1.2*N)), ls="dashed")
        #plt.fill_between(res, np.array(corre)+np.array(std), np.array(corre)-np.array(std))
    
    # Now styling the figure
    ax1.legend(loc="lower left", ncols=3)
    ax2.text(.99, .99, f"{city.capitalize()}/{DISTANCE_FUNC[measure]} - {reference.capitalize()}", ha='right', va='top', transform=ax2.transAxes, fontsize=12, color="grey" )
    ax1.set_xlabel("Disk diameter (km)", fontsize=14)
    ax1.set_ylabel("Pearson correlation coefficient \n (Solid lines)", fontsize=14)
    ax1.set_ylim([ax1.get_ylim()[0]*0.8, ax1.get_ylim()[1]])
    ax2.set_ylabel("Standard deviation \n (Dashed lines)", fontsize=14)
    ax2.set_ylim([0, ax2.get_ylim()[1]*2])
    ax1.tick_params(axis="both", which="major", labelsize=12)
    ax2.tick_params(axis="both", which="major", labelsize=12)

    plt.show()