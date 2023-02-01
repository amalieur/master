#from schemes.grid_lsh import GridLSH
from utils.data_stats import *
from schemes.grid_lsh import GridLSH
from utils.file_handler import read_trajectory_file as FileReader
from utils import trajectory_distance as td


grid = GridLSH("G1",min_lat=41.14, max_lat=41.19, min_lon= -8.66, max_lon=-8.57, resolution=0.25, layers=4, meta_file="meta.txt", data_path="/data")

print(grid)

testfile = FileReader("./data/chosen_data/porto/P_AAA.txt")

grid._create_trajectory_hash(testfile)


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