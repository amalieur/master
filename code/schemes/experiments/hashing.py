"""
Script to be run from jupyter notebook to measure the efficiency of the disk-LSH hash generation using multiprocessing.

10 processess will be run in parallell and each process will be measured using the process time, so that the actual processing time will be measured
"""

from multiprocessing import Pool

from schemes.disk_lsh import DiskLSH
from schemes.grid_lsh import GridLSH

import global_variables

PORTO_DATA = f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/"

# Defining some nescesary variables:

#layers = 4
#diameter = 1.5
#num_disks = 50
#meta_file_p = "../data/chosen_data/porto/META-1000.TXT"



# Must define some wrapper functions that will be used by the pool processess in the notebook



def fun_wrapper_p_grid(args):
    """ Wrapper function for measuring grid hash computation  over porto
    ---
    params : [num_of_files, resolution, layers]
        num_of_files must match one of the meta-files
    """

    num_of_files, resolution, layers = args
    meta_file_p = f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/META.txt"
    grid = GridLSH("Porto G1", global_variables.P_MIN_LAT, global_variables.P_MAX_LAT, global_variables.P_MIN_LON, global_variables.P_MAX_LON, resolution, layers, meta_file_p, PORTO_DATA )

    return grid.measure_hash_computation(1,1)[0]

# All methods takes as input a list: [num_of_files, disks, layers, diameter]

def fun_wrapper_p_naive(args):
    """ Wrapper function for measuring disk hash computation
    ---
    params : [num_of_files, disks, layers, diameter]
        num_of_files must match one of the meta-files
    """

    num_of_files, num_disks, layers, diameter = args
    meta_file_p = f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/META.txt"
    disk = DiskLSH("Porto D1", global_variables.P_MIN_LAT, global_variables.P_MAX_LAT, global_variables.P_MIN_LON, global_variables.P_MAX_LON, num_disks, layers, diameter, meta_file_p, PORTO_DATA)
    
    return disk.measure_hash_computation_numerical(1,1)[0]


def fun_wrapper_p_quadrants(args):
    """ Wrapper function for measuring disk hash computation
    ---
    params : [num_of_files, disks, layers, diameter]
        num_of_files must match one of the meta-files
    """

    num_of_files, num_disks, layers, diameter = args
    meta_file_p = f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/META.txt"
    disk = DiskLSH("Porto D1", global_variables.P_MIN_LAT, global_variables.P_MAX_LAT, global_variables.P_MIN_LON, global_variables.P_MAX_LON, num_disks, layers, diameter, meta_file_p, PORTO_DATA)
    
    return disk.measure_hash_computation_with_quad_tree_numerical(1,1)[0]


def fun_wrapper_p_KD_tree(args):
    """ Wrapper function for measuring disk hash computation
    ---
    params : [num_of_files, disks, layers, diameter]
        num_of_files must match one of the meta-files
    """

    num_of_files, num_disks, layers, diameter = args
    meta_file_p = f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/META.txt"
    disk = DiskLSH("Porto D1", global_variables.P_MIN_LAT, global_variables.P_MAX_LAT, global_variables.P_MIN_LON, global_variables.P_MAX_LON, num_disks, layers, diameter, meta_file_p, PORTO_DATA)
   
    return disk.measure_hash_computation_with_KD_tree_numerical(1,1)[0]
