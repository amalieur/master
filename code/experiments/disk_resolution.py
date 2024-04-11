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

# Some constants

PORTO_CHOSEN_DATA = "../data/chosen_data/porto/"
PORTO_HASHED_DATA = "../data/hashed_data/grid/porto/"
PORTO_META_TEST = "../data/hashed_data/grid/porto/META-50.TXT"

# SE PÅ DENNE SENERE
P_MAX_LON = -8.57
P_MIN_LON = -8.66
P_MAX_LAT = 41.19
P_MIN_LAT = 41.14


MEASURE = {
    "py_ed" : py_ed,
    "py_dtw" : py_dtw,
}

REFERENCE = {
    "portodtw" : P_DTW,
    "portofrechet" : P_FRE,
}

DISTANCE_FUNC = {
    "py_ed" : "ED",
    "py_dtw" : "DTW",
}


def _constructDisk(city: str, diameter: float, layers: int, disks:int=50) -> DiskLSH:
    """ Constructs a grid hash object over the given city """
    if city.lower() == "porto":
        return DiskLSH(f"GP_{layers}-{'{:.2f}'.format(diameter)}", P_MIN_LAT, P_MAX_LAT, P_MIN_LON, P_MAX_LON, disks, layers, diameter, PORTO_META_TEST, PORTO_CHOSEN_DATA)
    else:
        raise ValueError("City argument must be porto")


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
    diameter : list[float]
        The diameter that will be visualised -> [min, max, step]
    measure : str (default py_dtw)
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
    ax1.legend(loc="center right", ncols=2, fontsize=16, labelspacing=0.2, borderpad=0.2, handlelength=1, handletextpad=0.5, borderaxespad=0.2, columnspacing=1)
    ax2.text(.99, .99, f"{city.capitalize()}/{DISTANCE_FUNC[measure]} - {reference.capitalize()}", ha='right', va='top', transform=ax2.transAxes, fontsize=14, color="grey" )
    ax1.set_xlabel("Disk diameter (km)", fontsize=18)
    ax1.set_ylabel("Pearson correlation coefficient - Solid lines", fontsize=18)
    ax1.set_ylim([ax1.get_ylim()[0]*0.8, ax1.get_ylim()[1]])
    ax2.set_ylabel("Standard deviation \- Dashed lines", fontsize=18)
    ax2.set_ylim([0, ax2.get_ylim()[1]*2])
    ax1.tick_params(axis="both", which="major", labelsize=16)
    ax2.tick_params(axis="both", which="major", labelsize=16)

    plt.show()




## Methods for visualusing the effect of number of disks

def _fun_wrapper_corr_disks(args):
    city, dia, lay, disks, measure, reference = args
    Disk = _constructDisk(city, dia, lay, disks)
    hashes = _compute_hashes(Disk, measure)

    edits = _mirrorDiagonal(MEASURE[measure](hashes)).flatten()
    corr = np.corrcoef(edits, REFERENCE[city.lower()+reference.lower()])[0][1]
    return corr


def _compute_disk_numbers(city: str, layers: int, diameter: int, disks: list[int], measure: str = "py_dtw", reference: str = "dtw", parallell_jobs: int = 20):
    """ Computations for the visualisation of the number of disks"""
    
    pool = Pool()

    results = []

    for disk_number in disks:
        print(f"DN: {disk_number}", end="\r")
        corrs = pool.map(_fun_wrapper_corr_disks, [(city, diameter, layers, disk_number, measure, reference)for _ in range(parallell_jobs)])
        corr = np.average(np.array(corrs))
        std = np.std(np.array(corrs))
        results.append([corr, disk_number, std])
    
    return results


def plot_disk_numbers(city: str, layers: int, diameter: int, disks: list[int], measure: str = "py_dtw", reference: str = "dtw", parallell_jobs: int = 20):
    """ Visualises the effect of adjusting the number of disks 
    
    Param
    ---
    city : str
        Either "porto" or "rome", throws error unless
    layers : int
        The layers that will be visualised
    diameter : list[float]
        The resolution that will be used for the disks
    disks : list[int]
        The number of disks that will be plotted
    measure : str (default py_dtw)
        The measure that will be used. Either edit distance or dtw -> "py_ed" or "py_edp"
    reference : str (default dtw)
        The true similarities that will be used as reference. Either dtw or frechet
    paralell_jobs : int (default 20)
        Yhe number of parallell jobs that will create the data foundation
    """

    results = _compute_disk_numbers(city, layers, diameter, disks, measure, reference, parallell_jobs)

    fig, ax1 = plt.subplots(figsize=(10,8), dpi=300)
    ax2 = ax1.twinx()
    #fig.set_size_inches(10,8)
    cmap = plt.get_cmap('gist_ncar')
    N = len(results)
    
      
    corre, num_disks, std = list(zip(*results))
    corre = np.array(corre)
    num_disks = np.array(num_disks)
    std = np.array(std)
    ax1.plot(num_disks, corre, c=cmap(float(1.3-1)/(1.2*N)), lw=2)
    ax2.plot(num_disks, std, c=cmap(float(1.3-1)/(1.2*N)), ls="dashed")
    #plt.fill_between(res, np.array(corre)+np.array(std), np.array(corre)-np.array(std))
    
    # Now styling the figure
    #ax1.legend(loc="lower left", ncols=3)
    ax2.text(.99, .99, f"{city.capitalize()}/{DISTANCE_FUNC[measure]} - {reference.capitalize()}", ha='right', va='top', transform=ax2.transAxes, fontsize=12, color="grey" )
    ax1.set_xlabel("Number of disks", fontsize=18)
    ax1.set_ylabel("Pearson correlation coefficient - Solid line", fontsize=18)
    ax1.set_ylim([ax1.get_ylim()[0]*0.8, ax1.get_ylim()[1]])
    ax2.set_ylabel("Standard deviation - Dashed line", fontsize=18)
    ax2.set_ylim([0, ax2.get_ylim()[1]*2])
    ax1.tick_params(axis="both", which="major", labelsize=16)
    ax2.tick_params(axis="both", which="major", labelsize=16)

    plt.show()