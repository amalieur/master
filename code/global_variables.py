# These variables must be updated when a new subset is chosen.
CHOSEN_SUBSET_NAME = "subset-5000"
CHOSEN_SUBSET_SIZE = 5000
CHOSEN_SUBSET_DATAFILE = "../data/raw_data/sorted-subset-5000-6.csv"
CHOSEN_BUSROUTES_DATAFILE = "../data/raw_data/bus_routes-all-formatted.csv"


#These variables must be updated when a new geographical area is chosen

#Upper left corner: (P_MAX_LAT, P_MIN_LON)
#Upper right corner: (P_MAX_LAT, P_MAX_LON)
#Lower left corner: (P_MIN_LAT, P_MIN_LON)
#Lower right corner: (P_MIN_LAT, P_MAX_LON)
P_MAX_LON = -8.45
P_MIN_LON = -8.72
P_MAX_LAT = 41.26
P_MIN_LAT = 41.07


#FRECHET ALGORITHM:

#Threshold distance to approve that two points are similar enough(in meters) in Frechet distance
FRECHET_THRESHOLD_DISTANCE = 105

#The number of similar trajectories needed to accept a well-used route
THRESHOLD_NUMBER_OF_TRAJECTORIES = 50

#the percentage of connected points that need to match the other trajectory, to be a match
THRESHOLD_PERCENTAGE_OF_TRAJECTORY = 0.7