""" 
Sheet that will be used to measure the time needed to generate similarities of the grid-hashes 

Will run N processess in parallell to measure time efficiency
"""

from multiprocessing import Pool
import time
import timeit as ti
import pandas as pd

import global_variables

from schemes.grid_lsh import GridLSH

from utils.similarity_measures.distance import py_edit_distance as py_ed
from utils.similarity_measures.distance import py_edit_distance_penalty as py_edp
from utils.similarity_measures.distance import py_edit_distance_penalty_parallell as py_edp_parallell

PORTO_CHOSEN_DATA = f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/"
PORTO_HASHED_DATA = f"../data/hashed_data/grid/{global_variables.CHOSEN_SUBSET_NAME}/"

#TODO: remove size
def PORTO_META(size: int): return f"../data/hashed_data/{global_variables.CHOSEN_SUBSET_NAME}/META.txt"

MEASURE = {
    "ed" : py_ed,
    "dtw" : py_edp,
}

def _constructGrid(city: str, res: float, layers: int, size: int) -> GridLSH:
    """ Constructs a grid hash object over the given city """
    if city.lower() == "porto":
        return GridLSH(f"GP_{layers}-{'{:.2f}'.format(res)}", global_variables.P_MIN_LAT, global_variables.P_MAX_LAT, global_variables.P_MIN_LON, global_variables.P_MAX_LON, res, layers, PORTO_META(size), PORTO_CHOSEN_DATA)
    else:
        raise ValueError("City argument must be porto")
    

def _computeSimilarities(args) -> list:
    hashes, measure = args
    elapsed_time = ti.timeit(lambda: MEASURE[measure](hashes), number=1, timer=time.process_time)
    return elapsed_time


def measure_grid_hash_similarity_computation_time(city: str, size: int, res: float, layers: int, measure: str = "dtw", parallell_jobs: int = 10) -> list:
    """
    Method to measure the execution time of similarity computation of the hashes

    Param
    ---
    city : str
        Either "porto" or "rome"
    size : int
        The dataset-size that will be computed
    res : float
        The grid resolution
    layers : int
        The number of layers that will be used
    measure : str (Either "ed" or "dtw" - "dtw" default)
        The measure that will be used for computation
    parallell_jobs : int
        The number of jobs that will be run
    """
    times = []
    with Pool(parallell_jobs) as pool:
        Grid = _constructGrid(city, res, layers, size)
        hashes = Grid.compute_dataset_hashes()
        time_measurement = pool.map(_computeSimilarities, [(hashes,measure) for _ in range(parallell_jobs)])
        times.extend(time_measurement)
    return times



def generate_grid_hash_similarity(city: str, res: float, layers: int) -> pd.DataFrame:
    """Generates the full grid hash similarities and saves it as a dataframe """
    Grid =_constructGrid(city, res, layers, 1000)
    hashes = Grid.compute_dataset_hashes()
    similarities = py_edp_parallell(hashes)

    return similarities