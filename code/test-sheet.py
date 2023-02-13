#from schemes.grid_lsh import GridLSH
from utils.data_stats import *
from schemes.grid_lsh import GridLSH
from schemes.disk_lsh import DiskLSH
from utils.file_handler import read_trajectory_file as FileReader
from utils import trajectory_distance as td

import os, psutil
import gc
from multiprocessing import Pool

# Trying to get high priority
#p = psutil.Process(os.getpid())
#p.nice(psutil.REALTIME_PRIORITY_CLASS)

abs_path = os.path.dirname(__file__)
rel_path = "../data/chosen_data/porto/META-200.TXT"
ful_path = os.path.join(abs_path, rel_path)

data_path = os.path.join(abs_path, "../data/chosen_data/porto/")

#grid = GridLSH("G1",min_lat=41.14, max_lat=41.19, min_lon= -8.66, max_lon=-8.57, resolution=0.25, layers=4, meta_file=ful_path, data_path=data_path)

#print(grid)

#testfile = FileReader("./data/chosen_data/porto/P_AAA.txt")

#hashes = grid.compute_dataset_hashes()
#stats = grid.measure_hash_computation(10,1)
#print(stats)
#print(len(hashes))
#grid.print_hashes()
#grid._create_trajectory_hash(testfile)

disk = DiskLSH("D1",41.14, 41.19, -8.66, -8.57, 50, 4, 1.5, ful_path, data_path=data_path)
#print(disk)
#disk.print_disks()
#hsh = disk._create_trajectory_hash([[1,2],[2,2],[3,3]])
#hsh = disk.compute_dataset_hashes()

#stats1 = disk.measure_hash_computation(1, 3)
#print(stats1)

#stats = disk.measure_hash_computation_with_quad_tree(1, 3)
#print(stats)

def dun(x):
    disk = DiskLSH("D1",41.14, 41.19, -8.66, -8.57, 50, 4, 1.5, ful_path, data_path=data_path)
    return disk.measure_hash_computation(1,1)[0]

def dunq(x):
    disk = DiskLSH("D1",41.14, 41.19, -8.66, -8.57, 50, 4, 1.5, ful_path, data_path=data_path)
    return disk.measure_hash_computation_with_quad_tree(1,1)[0]

def dunk(x):
    disk = DiskLSH("D1",41.14, 41.19, -8.66, -8.57, 50, 4, 1.5, ful_path, data_path=data_path)
    return disk.measure_hash_computation_with_KD_tree(1,1)[0]
def gun(x):
    grid = GridLSH("G1",min_lat=41.14, max_lat=41.19, min_lon= -8.66, max_lon=-8.57, resolution=0.25, layers=4, meta_file=ful_path, data_path=data_path)
    return grid.measure_hash_computation(1,1)[0]


if __name__=="__main__":
    # name=main important for paralell processing
    with Pool() as pool:
        result = pool.map(gun, range(10))
    print(result)

#disk.visualise_hashes()

""" 
create_trajectory_length_histogram("./data/chosen_data/porto/","P_")
create_trajectory_length_histogram("./data/chosen_data/rome/","R_")

a, ami, ama = create_trajectory_length_stats("./data/chosen_data/porto/","P_")
b, bmi, bma = create_trajectory_length_stats("./data/chosen_data/rome/", "R_")

print(int(a), ami, ama)
print(int(b), bmi, bma)
"""



"""
a = td.get_latitude_difference(1)
b = td.get_longitude_difference(1, 40)
print(a, b)
"""