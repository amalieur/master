""" Sheet containing DTW methods related to true similarity creation """

import numpy as np
import pandas as pd
import collections as co

from traj_dist.pydist.dtw import e_dtw as p_dtw
from traj_dist.distance import dtw as c_dtw


def py_dtw(trajectories: dict[str, list[list[float]]]) -> pd.DataFrame:
    """ 
    Method for computing DTW similarity between all trajectories in a given dataset using python. 

    Params
    ---
    trajectories : dict[str, list[list[float]]]
        A dictionary containing the trajectories

    Returns
    ---
    A nxn pandas dataframe containing the pairwise similarities - sorted alphabetically 
    """

    sorted_trajectories = co.OrderedDict(sorted(trajectories.items()))
    num_trajectoris = len(sorted_trajectories)

    M = np.zeros((num_trajectoris, num_trajectoris))
    
    for i, traj_i in enumerate(sorted_trajectories.keys()):
        for j, traj_j in enumerate(sorted_trajectories.keys()):
            X = np.array(sorted_trajectories[traj_i])
            Y = np.array(sorted_trajectories[traj_j])
            dtw = p_dtw(X,Y)
            M[i,j] = dtw
            if i == j: 
                break
    
    df = pd.DataFrame(M, index=sorted_trajectories.keys(), columns=sorted_trajectories.keys())

    return df
    



def cy_dtw(trajectories: dict[str, list[list[float]]]) -> pd.DataFrame:
    """ 
    Method for computing DTW similarity between all trajectories in a given dataset using cython. 

    Params
    ---
    trajectories : dict[str, list[list[float]]]
        A dictionary containing the trajectories

    Returns
    ---
    A nxn pandas dataframe containing the pairwise similarities - sorted alphabetically 
    """

    sorted_trajectories = co.OrderedDict(sorted(trajectories.items()))
    num_trajectoris = len(sorted_trajectories)

    M = np.zeros((num_trajectoris, num_trajectoris))
    
    for i, traj_i in enumerate(sorted_trajectories.keys()):
        for j, traj_j in enumerate(sorted_trajectories.keys()):
            X = np.array(sorted_trajectories[traj_i])
            Y = np.array(sorted_trajectories[traj_j])
            dtw = c_dtw(X,Y)
            M[i,j] = dtw
            if i == j: 
                break
    
    df = pd.DataFrame(M, index=sorted_trajectories.keys(), columns=sorted_trajectories.keys())

    return df