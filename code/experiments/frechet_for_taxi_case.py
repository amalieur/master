from utils import metafile_handler as mfh
from utils import file_handler as fh

import pandas as pd

import global_variables

from geopy.distance import great_circle


def do_whole_experiment(clusters_dict: dict, taxi_df: pd.DataFrame, bus_df: pd.DataFrame):
    taxi_trajectory_clusters = find_similarity_in_clusters(clusters_dict)

    if(len(taxi_trajectory_clusters)>0):
        bus_trajectories_file = mfh.read_meta_file(f"../data/bus_data/META.txt")
        bus_trajectories_dict = fh.load_trajectory_files(bus_trajectories_file, f"../data/bus_data/")

        #reads the coordinates of the trajectories, because so far we only have their names
        taxi_trajectory_files = mfh.read_meta_file(f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/META.txt")
        taxi_trajectories_dict = fh.load_trajectory_files(taxi_trajectory_files, f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/")

        #saving all matches of trajectory-clusters (frequently used taxi-routes) and bus-routes
        routes_with_match = []
        #saving all trajectory-clusters (frequently used taxi-routes) that doesn't match any bus-route
        routes_without_match = []

        for cluster in taxi_trajectory_clusters:
            has_a_match = False
            for bus_name, bus_trajectory in bus_trajectories_dict.items():
                for traj in cluster:
                    taxi_trajectory = taxi_trajectories_dict[traj]
                    matching_points = find_matching_points(taxi_trajectory, bus_trajectory)
                    if(check_for_similarity(matching_points, [len(taxi_trajectory), len(bus_trajectory)], 1)):
                        routes_with_match.append([cluster, bus_name])
                        has_a_match = True
                        break
            if(not has_a_match):
                routes_without_match.append(cluster)
        save_to_files(routes_with_match, routes_without_match, taxi_df, bus_df)
        print(f"It was found {len(clusters_dict)} well used taxi routes.")
        print(f"{len(routes_without_match)} of the well used routes did not match any bus routes.")
        print(f"While it was found {len(routes_with_match)} matches between well-used taxi routes and bus routes.")
        print(f"The results are written to file in the folder: code/experiments/results/{global_variables.CHOSEN_SUBSET_NAME}/lists")
    else:
        save_to_files([], [], taxi_df, bus_df)
        print("No well-used taxi routes is found.")
            
def save_to_files(routes_with_match, routes_without_match, taxi_trajectories_df, bus_trajectories_df):
    #To give user some respons even if there are no well used taxi routes
    if(len(routes_with_match)==0 and len(routes_without_match)==0):
        with open(f"../code/experiments/results/{global_variables.CHOSEN_SUBSET_NAME}/lists/no-clusters-found.txt", "w") as file:
            file.write("No well used taxi routes were found.")

    for i in range(len(routes_with_match)):
        result_list = []
        
        for index, row in taxi_trajectories_df.iterrows():
            if str(row["TRIP_ID"]) in routes_with_match[i][0]:
                result_list.append({'TRIP_ID': row["TRIP_ID"], 'CALL_TYPE': row["CALL_TYPE"], 'TIMESTAMP': row["TIMESTAMP"], 'POLYLINE': row["POLYLINE"]})
        for index, row in bus_trajectories_df.iterrows():
            if str(row["name"])==routes_with_match[i][1]:
                result_list.append({'TRIP_ID': row["name"], 'CALL_TYPE': '0', 'TIMESTAMP': 0, 'POLYLINE': row["coordinates"]})
        result_df = pd.DataFrame(result_list, columns=['TRIP_ID', 'CALL_TYPE', 'TIMESTAMP', 'POLYLINE'])
        result_df.to_csv(f"../code/experiments/results/{global_variables.CHOSEN_SUBSET_NAME}/lists/match-{i}.csv", index=False)

    for i in range(len(routes_without_match)):
        result_list = []
        for index, row in taxi_trajectories_df.iterrows():
            if str(row["TRIP_ID"]) in routes_without_match[i]:
                result_list.append({'TRIP_ID': row["TRIP_ID"], 'CALL_TYPE': row["CALL_TYPE"], 'TIMESTAMP': row["TIMESTAMP"], 'POLYLINE': row["POLYLINE"]})
        result_df = pd.DataFrame(result_list, columns=['TRIP_ID', 'CALL_TYPE', 'TIMESTAMP', 'POLYLINE'])
        result_df.to_csv(f"../code/experiments/results/{global_variables.CHOSEN_SUBSET_NAME}/lists/not-match-{i}.csv", index=False)
            


#input: a dictionary containing all the clusters in the dataset, after LSH
#output: a list of lists with all discovered similar trajectories. Each list contains the name of trajectories which is discovered to be similar
#example: [[traj_1_in_group_A, traj_2_in_group_A, traj_3_in_group_A....], [traj_1_in_group_B, traj_2_in_group_B, traj_3_in_group_B....], ...]
def find_similarity_in_clusters(clusters_dict: dict):
    result_list = []

    #reads the coordinates of the trajectories, because so far we only have their names
    files = mfh.read_meta_file(f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/META.txt")
    trajectories = fh.load_trajectory_files(files, f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/")

    #loops through every cluster (0, 1, 2, 3, ...) found by LSH
    for cluster in clusters_dict:
        #if the number of trajectories in the cluster is below threshold there is no need to check for similarity
        if(len(clusters_dict[cluster])>=global_variables.THRESHOLD_NUMBER_OF_TRAJECTORIES):
            #will contain the actual coordinates of every trajectory in the cluster
            trajectories_coordinates_list = []
            for traj in clusters_dict[cluster]:
                trajectories_coordinates_list.append(trajectories[traj])
            groups = find_similarity_in_cluster(clusters_dict[cluster], trajectories_coordinates_list)
            for group in groups:
                if(len(group)>=global_variables.THRESHOLD_NUMBER_OF_TRAJECTORIES):
                    result_list.append(group)
            
    return result_list
        

   

#input: a list with the names of all trajectories in a cluster and a list with the coordinates of all trajectories in a cluster. With the same ordering
#output: a list of lists, each containing the names of the trajectories that are considered similar
def find_similarity_in_cluster(trajectory_names_list: list, trajectories_coordinates_list: list):
    similar_trajectories = []
    for i in range(len(trajectory_names_list)):
        for j in range(len(trajectory_names_list)):
            #to avoid comparing a trajectory with itself and to avoid compare a pair of trajectories several times
            if i<j:
                #similar is a boolean telling wether the two trajectories are similar or not
                similar = frechet_similar_trajectories(trajectories_coordinates_list[i], trajectories_coordinates_list[j])
                if(similar):
                    similar_trajectories.append([trajectory_names_list[i], trajectory_names_list[j]])
    result = merge_list_of_clusters(similar_trajectories)
    discovered_clusters = []
    for r in result:
        if(len(r)>=global_variables.THRESHOLD_NUMBER_OF_TRAJECTORIES):
            discovered_clusters.append(r)
    return result

# takes in two trajectories, and check these for similarity. Which means whether the two trajectories contains a similar sub-trajectory where the length of the sub-trajectory is at least 
# THRESHOLD_PERCENTAGE_OF_TRAJECTORY of one of the trajectories
# input: one list for each of the trajectories, containing the coordinates of the trajectory. 
# output: true or false
def frechet_similar_trajectories(t1: list, t2: list):
    #creating the grid of match/not-match
    matching_points = find_matching_points(t1, t2)
    is_a_match_1 = check_for_similarity(matching_points, [len(t1), len(t2)], 1)
    if(is_a_match_1):
        return True
    is_a_match_2 = check_for_similarity(matching_points, [len(t1), len(t2)], 2)
    return is_a_match_2


#HELPING FUNCTIONS TO FRECHET ALGORITHM 

def find_matching_points(t1: list, t2: list):
    #creating the grid of match/not-match
    matching_points = []
    for i1 in range(len(t1)):
        for i2 in range(len(t2)):
            distance = great_circle((t1[i1][0], t1[i1][1]), (t2[i2][0], t2[i2][1])).m
            if distance <= global_variables.FRECHET_THRESHOLD_DISTANCE:
                matching_points.append([i1, i2])
    return matching_points

# input: list of lists with pairwise similar trajectories
# output: list of groups of similar trajectories
# merge pairs/groups with at least one similar trajectory
def merge_list_of_clusters(pair_list: list):
    is_changed = True
    cluster_list = pair_list
    while is_changed:
        is_changed = False
        for i in range(len(cluster_list)):
            for j in range(len(cluster_list)):
                #if i and j are not the same cluster, but they contain ANY similar items
                if i!=j and any(traj in cluster_list[i] for traj in cluster_list[j]):
                    is_changed = True
                    cluster_list[i] += cluster_list[j]
                    cluster_list[j] = []
        new_list = cluster_list.copy()
        for l in cluster_list:
            if len(l)==0:
                new_list.remove(l)
        for cluster_index in range(len(new_list)):
            temp_point_list = []
            for traj in new_list[cluster_index]:
                if traj not in temp_point_list:
                    temp_point_list.append(traj)
            new_list[cluster_index] = temp_point_list
        cluster_list = new_list.copy()
    return cluster_list
 

#point_list: list with points that is a match (t1-point-number, t2-point-number)
#lengths: list with the lengths of the trajectories to compare [traj1-length, traj2-length]
#traj_to_check: A number indicating wheter we should use traj1 og traj2 as the "main" traj
def check_for_similarity(point_list: list, lengths: list, traj_to_check: int):
    temp_list = []
    temp_number_of_points = 0
    #if traj_to_check=1, use index 0, if traj_to_check=2, use index 1
    for i in range(lengths[traj_to_check-1]):
        has_connection = False
        for point in point_list:
            if point[traj_to_check-1]==i:
                has_connection = True
                break
        if has_connection:
            temp_list.append(i)
            temp_number_of_points += 1
        elif len(temp_list)>0:
            #to allow a gap of two routes
            if i-1 not in temp_list and i-2 not in temp_list:
                #if the length of the connected points represents the threshold percentage (in global_variables) of the whole trajectory it is a match 
                if temp_number_of_points>=lengths[traj_to_check-1]*global_variables.THRESHOLD_PERCENTAGE_OF_TRAJECTORY:
                    return True
                #if it is still possible to find a sequence that is long enough
                elif i <= (lengths[traj_to_check-1]*(1-global_variables.THRESHOLD_PERCENTAGE_OF_TRAJECTORY))-1:
                    temp_list = []
                    temp_number_of_points = 0
                else:
                    return False
    if temp_number_of_points>=lengths[traj_to_check-1]*global_variables.THRESHOLD_PERCENTAGE_OF_TRAJECTORY:
        return True
    return False