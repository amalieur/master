"""
Slightly adjusted version of davies bouldin index

Written to mimic the proposal from "Review and Perspective for distance based trajectory clustering" by Besse et al.

"""

import numpy as np

import global_variables

def davies_bouldin(X: np.ndarray, clusters: np.ndarray):
    """Computes the adjusted davies bouldin index"""
    n_clusters = len(set(clusters))
    bl = db_between_like(X, clusters)
    wl = db_within_like(X, clusters)
    return 1/n_clusters * float(wl)/float(bl), wl/(wl+bl)*100, bl/(wl+bl)*100



def db_between_like(X: np.ndarray, clusters: np.ndarray):
    """Computing the between like part of the davis bouldin index
    Returns the sum of the clusters distance from the cluster centroid
    """
    T_centroid = find_centroid(X, clusters=np.zeros(global_variables.CHOSEN_SUBSET_SIZE), cluster=0)

    n_clusters = len(set(clusters))
    inter_cluster_sum = 0
    for i in range(n_clusters):
        # Computes the intra cluster distance for one cluster
        #cluster_trajectories = np.where(clusters == i)[0]
        C_centroid = find_centroid(X, clusters, i)
        distance = X[T_centroid][C_centroid]
        inter_cluster_sum += distance
    #print(intra_cluster_sum/n_clusters)
    return inter_cluster_sum
        
    

def db_within_like(X: np.ndarray, clusters: np.ndarray):
    """Computing the within like part of the davies bouldin index
    
    Returns the average sum of each clusters intra-cluster distance
    """
    n_clusters = len(set(clusters))
    #print(n_clusters)

    intra_cluster_sum = 0
    for i in range(n_clusters):
        # Computes the intra cluster distance for one cluster
        cluster_trajectories = np.where(clusters == i)[0]
        centroid = find_centroid(X, clusters, i)
        summ = sum([ X[centroid][traj] for traj in cluster_trajectories if traj != centroid])
        intra_cluster_sum += summ
    #print(intra_cluster_sum/n_clusters)
    return intra_cluster_sum/n_clusters



def find_centroid(X: np.ndarray, clusters: np.ndarray, cluster: int):
    """ Finding the exemplar centroid of a cluster """ 
    cluster_trajectories = np.where(clusters == cluster)[0]
    #cluster_trajectories = X.take = 
    centroid = cluster_trajectories[0]
    smallest_combined_distance = np.inf
    
    for traj in cluster_trajectories:
        distance = sum([ X[traj2][traj] for traj2 in cluster_trajectories if traj2 != traj])
        if distance < smallest_combined_distance:
            centroid = traj
            smallest_combined_distance = distance
    return centroid

if __name__=="__main__":
    distances = np.array([[0,2,3,2,3,1],[2,2,2,2,2,2],[3,2,3,2,4,2],[1,2,3,2,3,1],[2,2,2,2,2,2],[3,2,3,2,4,2]])
    print(len(distances))
    print(np.argmin(distances, axis=0))
    clusters = np.array([0,1,2,1,2,1])
    find_centroid(distances,clusters,2)
    db_within_like(distances, clusters)
    db_between_like(distances, clusters)