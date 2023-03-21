"""
Sheet that will be used to measure the time needed to generate similarities of the grid hashes

Will run N processess in parallell to measure time efficiency
"""

from multiprocessing import Pool
import time
import timeit as ti
import pandas as pd

from schemes.disk_lsh import DiskLSH

from utils.similarity_measures.distance import py_edit_distance as py_ed
from utils.similarity_measures.distance import py_dtw
from utils.similarity_measures.distance import py_dtw_parallell

P_MAX_LON = -8.57
P_MIN_LON = -8.66
P_MAX_LAT = 41.19
P_MIN_LAT = 41.14

R_MAX_LON = 12.53
R_MIN_LON = 12.44
R_MAX_LAT = 41.93
R_MIN_LAT = 41.88

PORTO_CHOSEN_DATA = "../data/chosen_data/porto/"
PORTO_HASHED_DATA = "../data/hashed_data/grid/porto/"

ROME_CHOSEN_DATA = "../data/chosen_data/rome/"
ROME_HASHED_DATA = "../data/hashed_data/grid/rome/"

def PORTO_META(size: int): return f"../data/hashed_data/grid/porto/META-{size}.TXT"
def ROME_META(size: int): return f"../data/hashed_data/grid/rome/META-{size}.TXT"

MEASURE = {
    "ed" : py_ed,
    "dtw" : py_dtw,
}


def _constructDisk(city: str, diameter: float, layers: int, disks: int, size: int) -> DiskLSH:
    """ Constructs a grid hash object over the given city """
    if city.lower() == "porto":
        return DiskLSH(f"DP_{layers}-{'{:.2f}'.format(diameter)}", P_MIN_LAT, P_MAX_LAT, P_MIN_LON, P_MAX_LON, disks, layers, diameter, PORTO_META(size), PORTO_CHOSEN_DATA)
    elif city.lower() == "rome":
        return DiskLSH(f"GDR_{layers}-{'{:.2f}'.format(diameter)}", R_MIN_LAT, R_MAX_LAT, R_MIN_LON, R_MAX_LON, disks, layers, diameter, ROME_META(size), ROME_CHOSEN_DATA)
    else:
        raise ValueError("City argument must be either porto or rome")
    

def _computeSimilarities(args) -> list:
    hashes, measure = args
    elapsed_time = ti.timeit(lambda: MEASURE[measure](hashes), number=1, timer=time.process_time)
    return elapsed_time


def measure_disk_hash_similarity_computation_time(city: str, size: int, diameter: float, layers: int, disks: int, hashtype: str, measure: str = "dtw" , parallell_jobs: int = 10) -> list:
    """
    Method to measure the execution time of similarity computation of the hashes

    Param
    ---
    city : str
        Either "porto" or "rome"
    size : int
        The dataset-size that will be computed
    diameter : float
        The disks diameter
    layers : int
        The number of layers that will be used
    disks : int
        The number of disks that will be used at each layer
    hashtype : str
        "normal" | "quadrants" | "kd"
    measure : str (Either "ed" or "dtw" - "dtw" default)
        The measure that will be used for computation
    parallell_jobs : int
        The number of jobs that will be run
    """

    execution_times = []

    with Pool(parallell_jobs) as pool:
        Disk = _constructDisk(city, diameter, layers, disks, size)
        
        if measure == "dtw" and hashtype == "kd":
            hashes = Disk.compute_dataset_hashes_with_KD_tree_numerical()  
        elif measure=="ed" and hashtype == "normal":
            hashes = Disk.compute_dataset_hashes()
        elif measure=="ed" and hashtype == "quadrants":
            hashes = Disk.compute_dataset_hashes_with_quad_tree()
        elif measure == "ed" and hashtype == "kd":
            hashes = Disk.compute_dataset_hashes_with_KD_tree()
        else:
            raise ValueError("Cannot construct disk hashes as input parameters are uncertain")

        time_measurement = pool.map(_computeSimilarities, [(hashes,measure) for _ in range(parallell_jobs)])
        execution_times.extend(time_measurement)
    
    return execution_times


def generate_disk_hash_similarity(city: str, diameter: float, layers: int, disks: int) -> pd.DataFrame:
    """Generates the full grid hash similarities and saves it as a dataframe """

    Disk =_constructDisk(city, diameter, layers, disks, 1000)
    hashes = Disk.compute_dataset_hashes_with_KD_tree_numerical()
    similarities = py_dtw_parallell(hashes)

    return similarities