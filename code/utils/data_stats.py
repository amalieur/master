"""
Sheet for methods related to statistics of the chosen data
"""

import numpy as np
from matplotlib import pyplot as plt

from .file_handler import load_all_trajectory_files

DATASETS = {
    "P_" : "Porto",
}

BIN_SIZE = {
    "P_" : 1,
}


class IllegalArgumentError(ValueError):
    pass


def create_trajectory_length_histogram(folder_path: str, dataset_prefix: str) -> None:
    """
    Creates a histogram over trajectory lengths in the provided dataset 

    Parameters
    ----------
    folder_path : str
        The path of the data_folder
    dataset_prefix : str
        Prefix of the dataset that the histogram should be created over
    """

    trajectories = load_all_trajectory_files(folder_path=folder_path, prefix=dataset_prefix)

    traj_lens = np.array([len(obj) for obj in trajectories.values()])

    bins = np.arange(min(traj_lens), np.percentile(traj_lens, 95), BIN_SIZE[dataset_prefix]) # fixed bin size

    plt.hist(traj_lens, bins=bins, alpha=0.5)
    plt.title(f'0 - 95 th percentile of length of trajectories ({DATASETS[dataset_prefix]})')
    plt.xlabel('Length of trajectories ')
    plt.ylabel('Number of trajectories')

    plt.show()



def create_trajectory_length_stats(folder_path: str, dataset_prefix: str) -> None:
    """
    Calculates statistics over trajectory lengths in the provided dataset 

    Parameters
    ----------
    folder_path : str
        The path of the data_folder
    dataset_prefix : str
        Prefix of the dataset that the histogram should be created over
    
    Returns
    ---
    List of statistics [avg, min, max]
    """
    
    trajectories = load_all_trajectory_files(folder_path=folder_path, prefix=dataset_prefix)

    traj_lens = [len(obj) for obj in trajectories.values()]

    minimum = min(traj_lens)
    maximum = max(traj_lens)
    average = sum(traj_lens)/len(traj_lens)

    return [average, minimum, maximum]

