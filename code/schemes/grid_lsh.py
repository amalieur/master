"""
File for a grid-based LSH scheme class in python.

Takes min/max lat/lon as argument -> Could potentially make this integrated in the future
"""
import random

from .lsh_interface import LSHInterface

from utils import trajectory_distance as td
from utils import alphabetical_number as an


class GridLSH(LSHInterface):
    """ 
    A class for a grid-based LSH function for trajectory data
    """

    def __init__(self, name: str, min_lat: float, max_lat: float, min_lon: float, max_lon: float, resolution: float, layers: int, meta_file: str, data_path: str) -> None:
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
        resolution: float
            The preferred resolution for the grid (km)
        layers: int
            The number of layers that will be created
        meta_file: str
            A file containing the file-names that should be hashed through this class. Should be in the same folder as the data_path
        data_path: str
            The folder where the trajectories are stored
        """
        
        # First, initiating the direct variables

        self.name = name
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.resolution = resolution
        self.layers = layers
        self.meta_file = meta_file
        self.data_path = data_path

        # Second, instantiate the indirect variables required for the scheme

        self.lat_len = td.calculate_trajectory_distance([(self.min_lat, self.min_lon), (self.max_lat, self.min_lon)])
        self.lon_len = td.calculate_trajectory_distance([(self.min_lat, self.min_lon), (self.min_lat, self.max_lon)])
        self.lat_res = td.get_latitude_difference(self.resolution)
        self.lon_res = td.get_longitude_difference(self.resolution, self.min_lat)

        self.distortion = self._compute_grid_distortion(self.lat_len, self.lon_len, self.resolution, self.layers)


    def __str__(self) -> str:
        """ Prints information about the grid """
        lat_cells = int((self.max_lat - self.min_lat) // self.lat_res)
        lon_cells = int((self.max_lon - self.min_lon) // self.lon_res)

        return f"Grid: {self.name}\nCovering: " \
            f"{td.calculate_trajectory_distance([[self.min_lat, self.min_lon],[self.max_lat, self.min_lon]]), td.calculate_trajectory_distance([[self.min_lat, self.min_lon],[self.min_lat, self.max_lon]])} km \n" \
            f"Resolution: {self.resolution} km \n" \
            f"Distortion: {self.distortion} km \n" \
            f"Dimensions: {lat_cells, lon_cells} cells"
        

    def _compute_grid_distortion(self, lat_len: float, lon_len: float, resolution: float, layers: int) -> list[float]:
        """ Compute a random grid distortion off the resolution for the number of layers"""

        # Distortion should be a random float in the interval [0, resolution)
        distortion = [random.random()*resolution for x in range(layers)]
        return distortion

    def _compute_grid_resolution(self, lat_len: float, lon_len: float):
        """ Compute resolution if not provided during init"""
        pass

    def _create_trajectory_hash(self, trajectory: list[list[float]]) -> list[list[str]]:
        """ Creates a hash for one trajectory for all layers, returns it as a list of length layers with a list for each hashed layer """

        hashes = []
        for layer in range(self.layers):
            distortion = self.distortion[layer]
            
            lat_distort = td.get_latitude_difference(distortion)
            lon_distort = td.get_longitude_difference(distortion, self.min_lat)
            hash = []
            # print(lat_res, lon_res)
            for coordinate in trajectory:
                lat, lon = coordinate
                
                # Normalise the coordinate over 0 and compute the corresponding cell in for eac direction
                lat_hash = int((lat + lat_distort - self.min_lat) // self.lat_res)
                lon_hash = int((lon + lon_distort - self.min_lon) // self.lon_res)
                hash.append(an.get_alphabetical_value([lat_hash, lon_hash]))
            hashes.append(hash)
        
        #print(hashes)
        
        # TODO Further work
    
    def _compute_grid():
        pass
    

if __name__=="__main__":
    Grid = GridLSH("G1",min_lat=41.14, max_lat=41.19, min_lon= -8.66, max_lon=-8.57, resolution=0.25, meta_file="meta.txt", data_path="/data")
    print(Grid)

