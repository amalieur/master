"""
Sheet containing method for creating, fetching and deleting metafiles
"""

import os, shutil
import re
import random
import numpy as np




def create_meta_file(path_to_files: str, data_prefix: str, prefix: str = "META") -> None:
    """
    Function that creates metafiles (data-sets) with an incresing number of files containing random itemes from the chosen data.

    Parameters
    ----------
    path_to_files : str
        The path to the data folder
    data_prefix: str
        The prefix of the data that will be used in the sets
    prefix: str (default "META")
        The prefix of the meta_file
    """

    file_list = [file for file in os.listdir(path_to_files) if re.match(r'\b' + re.escape(data_prefix) + r'[^\\]*\.txt$', file)]

    with open(f'{path_to_files}/{prefix}.txt','w') as file:
        for file_name in file_list:
            file.write("%s\n" % (file_name))
        file.close()
    
    return



def get_meta_file(path_to_files: str, prefix: str = "META") -> list:
    """
    Function that returns the metafile in the given folder

    Parameters
    ----------
    path_to_files : str
        The path to the data folder
    prefix: str (default "META")
        The prefix of the meta_files that will be retrieved
    """

    file_list = [file for file in os.listdir(path_to_files) if re.match(r'\b' + re.escape(prefix) + r'[^\\]*\.txt$', file)]
    
    return file_list


def delete_meta_file(path_to_files: str, prefix: str = "META") -> None:
    """
    Function that deletes the metafiles in the given folder

    Parameters
    ----------
    path_to_files : str
        The path to the data folder
    prefix: str (default "META")
        The prefix of the meta_files that will be retrieved
    """

    file_list = [file for file in os.listdir(path_to_files) if re.match(r'\b' + re.escape(prefix) + r'[^\\]*\.txt$', file)]

    for filename in file_list:
        file_path = os.path.join(path_to_files, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to remove %s. Reason: %s" % (file_path, e))
    
    return


def read_meta_file(path_to_file: str) -> list[str]:
    """
    Reads and returns the content of a trajectory metafile as a list

    Parameters
    ---
    path_to_file : str
        Path to the metafile to be read
    
    Returns
    ---
    A list containing the filenames in the metafile
    """
    try:
        with open(path_to_file,'r') as file:
            trajectory_files = [ line.rstrip() for line in file ]
            file.close()
    except FileNotFoundError:
        raise(Exception(f"Cant find file {path_to_file}"))

    return trajectory_files


