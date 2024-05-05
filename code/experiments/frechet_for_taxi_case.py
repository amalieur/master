from utils import metafile_handler as mfh
from utils import file_handler as fh

import global_variables

#for testing
import random

#tar inn alle clusterene, også må den finne ut om noen av trajectoriene i noen av clusteret er like
def find_similarity_in_clusters(clusters_dict: dict):
    result_list = []

    #samler sammen selve trajectorien, da vi kun har navnet foreløpig
    files = mfh.read_meta_file(f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/META.txt")
    trajectories = fh.load_trajectory_files(files, f"../data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}/")

    #cluster: 0, 1, 2, 3, ...
    for cluster in clusters_dict:
        #if the number of trajectories in the cluster is below threshold there is no need to check for similarity
        if(len(clusters_dict[cluster])>=global_variables.THRESHOLD_NUMBER_OF_TRAJECTORIES):
            #will contain the actual coordinates of every trajectory in the cluster
            trajectories_coordinates_list = []
            for traj in clusters_dict[cluster]:
                trajectories_coordinates_list.append(trajectories[traj])
            groups = find_similarity_in_cluster(clusters_dict[cluster], trajectories_coordinates_list)
            for group in groups:
                result_list.append(group)
            
    return result_list

        

#Tar inn alle trajectoriene i et cluster, og sammenligner de for likhet
def find_similarity_in_cluster(trajectory_names_list: list, trajectories_coordinates_list: list):
    similar_trajectories = []
    for i in range(len(trajectory_names_list)):
        for j in range(len(trajectory_names_list)):
            #to avoid comparing a trajectory with itself and to avoid compare a pair of trajectories several times
            if i<j:
                #similar is a boolean telling wether the two trajectories are similar or not
                similar = frechet_similar_taxi_trajectories(trajectories_coordinates_list[i], trajectories_coordinates_list[j])
                if(similar):
                    similar_trajectories.append([trajectory_names_list[i], trajectory_names_list[j]])
    result = merge_clusters(similar_trajectories)
    return result

#tar inn to trajectories (taxi og taxi), og sjekker disse, returnerer true false, som betyr om de to trajectoriene inneholder en match eller ikke, der matchen må være en stor nok del av begge taxiturene
def frechet_similar_taxi_trajectories(tt1: list, tt2: list):
    #temporarly function to get some True, but most false
    return random.randint(0,9)>8


#tar inn to trajectories (taxi og taxi), og sjekker disse, returnerer true false, som betyr om de to trajectoriene inneholder en match eller ikke, der matchen må være en stor nok del av begge taxiturene
def frechet_similar_taxi_and_bus_trajectories(tt: list, bt: list):
    print("test")


# input: list of lists with pairwise similar trajectories
# output: list of groups of similar trajectories
# merge pairs/groups with at least one similar trajectory
def merge_clusters(pair_list: list):
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
        #HER er nok feilen, går ikke når vi tar remove rett i lista virker det som, må ta en kopi
        new_list = cluster_list.copy()
        for l in cluster_list:
            if len(l)==0:
                new_list.remove(l)
        cluster_list = new_list.copy()
    return cluster_list











