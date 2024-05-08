# These variables must be updated when a new subset is chosen.
CHOSEN_SUBSET_NAME = "subset-100"
CHOSEN_SUBSET_SIZE = 100
CHOSEN_SUBSET_DATAFILE = "../data/raw_data/subset-100-6-percent.csv"
CHOSEN_BUSROUTES_DATAFILE = "../data/raw_data/bus_routes-all-formatted.csv"


#These variables must be updated when a new geographical area is chosen
P_MAX_LON = -8.45
P_MIN_LON = -8.72
P_MAX_LAT = 41.26
P_MIN_LAT = 41.07


#FRECHET ALGORITHM
#Threshold distance to approve that to points are similar enough(in meters) in Frechet distance
FRECHET_THRESHOLD_DISTANCE = 120
THRESHOLD_NUMBER_OF_TRAJECTORIES = 3
THRESHOLD_PERCENTAGE_OF_TRAJECTORY = 0.5