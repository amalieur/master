"""
File for a disk-based LSH scheme class in python.

Takes min/max lat/lon as argument -> Could potentially make this integrated in the future
"""
import random
from .lsh_interface import LSHInterface

from utils import trajectory_distance as td
from utils import alphabetical_number as an
from utils import metafile_handler as mfh
from utils import file_handler as fh

from matplotlib import pyplot as plt
from matplotlib import collections as mc

from colorama import init as colorama_init, Fore, Style
import timeit as ti
import time


class DiskLSH(LSHInterface):
    """ 
    A class for a grid-based LSH function for trajectory data
    """

    def __init__(self, name: str, min_lat: float, max_lat: float, min_lon: float, max_lon: float, disks: int, layers: int, diameter: float, meta_file: str, data_path: str) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the grid
        min_lat : float
            The minimum latitude coordinate in the dataset
        max_lat : float
            The maximum latitude coordinate in the dataset
        min_lon : float
            The minimum lontitude coordinate in the dataset
        max_lon : float
            The maximum lontitude coordinate in the dataset
        disks : int
            The number of disks at each layer
        layers: int
            The number of layers that will be created
        diameter: float
            The preferred diameter of a disk in the scheme (km)
        meta_file: str
            A file containing the file-names that should be hashed through this class. Should be in the same folder as the data_path
        data_path: str
            The folder where the trajectories are stored
        """

        # First, intializing the direct variables

        self.name = name
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.num_disks = disks
        self.layers = layers
        self.diameter = diameter
        self.meta_file = meta_file
        self.data_path = data_path

        # Second, instantiate the indirect variables required for the scheme:
        self.lat_len = td.calculate_trajectory_distance([(self.min_lat, self.min_lon), (self.max_lat, self.min_lon)])
        self.lon_len = td.calculate_trajectory_distance([(self.min_lat, self.min_lon), (self.min_lat, self.max_lon)])
        
        # Lastly, instantiate and compute the disks that will represent the hash function
        self.disks = self._instantiate_disks(self.layers, self.num_disks)
        
        self.hashes = dict()



    def __str__(self) -> str:
        """ Prints information about the disks"""

        return f"Disk-scheme: {self.name} \n" \
            f"Covering: {self.lat_len, self.lon_len} km \n" \
            f"Diameter: {self.diameter} km\n" \
            f"Layers: {self.layers} \n"


    def set_meta_file(self, meta_file: str) -> None:
        """ Resets the meta_file """
        self.meta_file = meta_file


    def _instantiate_disks(self, layers: int, num_disks: int) -> dict[str, list]:
        """ Instantiates the random disks that will be present at each layer """
        disks = dict()
        for layer in range(layers):
            disks_list = []
            for disk in range(num_disks):
                lat = random.uniform(self.min_lat, self.max_lat)
                lon = random.uniform(self.min_lon, self.max_lon)
                disks_list.append([lat, lon])
            
            disks[layer] = disks_list
        return disks


    def _create_trajectory_hash(self, trajectory: list[list[float]]) -> list[list[str]]:
        """ Creates a hash for one trajectory for all layers. Returns it as a alist of length layers with a list of hashed point for each layer """
        
        hashes = []
        for layer in self.disks.keys():
            hash = []   # The created hash
            within = [] # The disks that the trajectory are currently within
            disks = self.disks[layer]
            for coordinate in trajectory:
                lat, lon = coordinate
                
                # If next point no longer in disk: Remove from within list
                for disk in within:
                    if td.calculate_trajectory_distance([[lat, lon], disk]) > self.diameter:
                        within.remove(disk)

                # If next point inside disk: Append to hash if not still within disk
                for i, disk in enumerate(disks):
                    if td.calculate_trajectory_distance([[lat, lon], disk]) <= self.diameter:
                        if disk not in within:
                            within.append(disk)
                            diskHash = an.get_alphabetical_value(i)
                            hash.append(diskHash)
            hashes.append(hash)
        return hashes


    def compute_dataset_hashes(self) -> dict[str, list]:
        """ Method for computing the disk hashes for a given dataset. Stores the hashes in a dictionary

        Params
        ---
        meta_file_path : str
            The path to the dataset metafile

        Returns
        ---
        A dictionary containing the hashes
        """
        files = mfh.read_meta_file(self.meta_file)
        trajectories = fh.load_trajectory_files(files, self.data_path)

        # Beginning to hash trajectories
        for key in trajectories:
            self.hashes[key] = self._create_trajectory_hash(trajectories[key])
        
        return self.hashes


    def measure_hash_computation(self, number: int, repeat: int) -> None:
        """ Method for measuring the computation time of the grid hashes. Does not change the object nor its attributes. """
        files = mfh.read_meta_file(self.meta_file)
        trajectories = fh.load_trajectory_files(files, self.data_path)
        hashes = dict()
        def compute_hashes(trajectories, hashes):
            for key in trajectories:
                hashes[key] = self._create_trajectory_hash(trajectories[key])
        
        measures = ti.repeat(lambda: compute_hashes(trajectories, hashes), number=number, repeat=repeat, timer=time.process_time)
        return (measures, len(hashes))


    def print_hashes(self) -> None:
        """ Printing the hashes """
        if len(self.hashes) == 0: print("No hashes created yet")
        else:
            colorama_init()
            for key in self.hashes:
                print(f"{Fore.GREEN}{key}{Style.RESET_ALL}:  {Fore.BLUE}{self.hashes[key][0]}{Style.RESET_ALL} ")
                for hash in self.hashes[key][1:]:
                    print(f"\t{Fore.BLUE}{hash}{Style.RESET_ALL}")

    

    def print_disks(self):
        for key in self.disks:
            print(key)
            for disk in self.disks[key]:
                print(f"\t{disk}")


    def visualise_hashes(self) -> None:
        """ Method to visualise hashes """
        plt.rcParams["figure.autolayout"] = True

        fig, ax = plt.subplots()

        radius = td.get_latitude_difference(self.diameter)/2
        
        for disk in self.disks[0]:
            x, y= disk
            print(disk, radius)
            ax.add_patch(plt.Circle((y,x), radius, fill=False))

        plt.show()


if __name__=="__main__":
    DiskLSH = DiskLSH("Disk1", 41.88, 41.93, 12.44, 12.53, 50, 4, 2, "meta.txt", "data")