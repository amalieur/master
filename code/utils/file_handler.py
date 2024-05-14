"""
Sheet containing methods for reading trajectories
"""

import os, re


def read_trajectory_file(file_path: str) -> list[list[float]]:
    """
    Reads a trajectory.txt file and returns the content as a list of coordinates

    Parameters
    ----------
    file_path : str
        The file path for the file that should be read

    Returns
    ---
    A list containing the files' coordinates as floats
    """

    try:
        with open(file_path,'r') as file:
            trajectory = [ list(map(float, line.rstrip().split(","))) for line in file ]
            file.close()
    except FileNotFoundError:
        print("Can't find file.")
        print(file_path)

    return trajectory


def load_trajectory_files(files: list[str], folder_path) -> dict:
    """
    Loads all trajectory.txt files and returns the content as a dictionary

    Parameters
    ----------
    files : list[str]
        A list of the files that should be read

    Returns
    ---
    A dictionary containing the files and their coordinates with their filename as key
    """

    file_list = files
    trajectories = dict()

    for file_name in file_list:
        key = os.path.splitext(file_name)[0]
        trajectory = read_trajectory_file(folder_path + file_name)
        
        trajectories[key] = trajectory
    return trajectories


def load_all_trajectory_files(folder_path: str, prefix: str) -> dict:
    """
    Reads all trajectory.txt files with the given prefix in the folder and returns a dictionary containing the data

    Parameters
    ----------
    folder_path : str
        The file path for the file that should be read
    prefix : str
        The prefix of the files that should be loaded
    
    Returns
    ---
    A dictionary containing all files with their filename as key
    """

    file_list = [file for file in os.listdir(folder_path) if re.match(r'\b' + re.escape(prefix) + r'[^\\]*\.txt$', file)]

    trajectories = dict()

    for file_name in file_list:
        key = os.path.splitext(file_name)[0]
        trajectory = read_trajectory_file(folder_path + file_name)
        
        trajectories[key] = trajectory

    return trajectories


def read_hash_file(file_path: str) -> list[list[float]]:
    """
    Reads a hash.txt file and returns the content as a list of hashes

    Parameters
    ----------
    file_path : str
        The file path for the file that should be read

    Returns
    ---
    A list containing the files' hashes as lists
    """

    try:
        with open(file_path,'r') as file:
            hashes = [line.replace(" ","").replace("'","")[1:-2].split(",") for line in file ]
            file.close()
    except FileNotFoundError:
        print("Can't find file.")

    return hashes


def load_trajectory_hashes(files: list[str], folder_path: str) -> dict:
    """
    Loads all hashes.txt files and returns the content as a dictionary

    Parameters
    ----------
    files : list[str]
        A list of the files that should be read

    Returns
    ---
    A dictionary containing the files and their hashes with their filename as key
    """

    file_list = files
    hashes = dict()

    for file_name in file_list:
        key = os.path.splitext(file_name)[0]
        hash = read_hash_file(folder_path + file_name)
        
        hashes[key] = hash

    return hashes