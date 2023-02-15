""" Sheet containing Frechet methods related to true similarity creation """

import numpy as np
import pandas as pd
import collections as co

from traj_dist.pydist.frechet import frechet as p_frechet
from traj_dist.distance import frechet as c_frechet

def py_frechet(trajectories: dict[str, list[list[float]]]) -> pd.DataFrame:
    """ 
    Method for computing frechet similarity between all trajectories in a given dataset using python. 

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
            dtw = p_frechet(X,Y)
            M[i,j] = dtw
            if i == j: 
                break
    
    df = pd.DataFrame(M, index=sorted_trajectories.keys(), columns=sorted_trajectories.keys())

    return df



def cy_frechet(trajectories: dict[str, list[list[float]]]) -> pd.DataFrame:
    """ 
    Method for computing frechet similarity between all trajectories in a given dataset using cython. 

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
            frech = c_frechet(X,Y)
            M[i,j] = frech
            if i == j: 
                break
    
    df = pd.DataFrame(M, index=sorted_trajectories.keys(), columns=sorted_trajectories.keys())

    return df


