"""
File for a grid-based LSH scheme class in python
"""

from lsh import LSHInterface


class GridLSH(LSHInterface):
    """ 
    A class for a grid-based LSH function for trajectory data
    """

    def __init__(self, name: str, x_len: float, y_len: float, resolution: float, meta_file: str, data_path: str) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the grid
        x_len : float
            The width of the area containing the trajectories (km)
        y_len: float
            The height of the are containing the trajectories (km)
        resolution: float
            The preferred resolution for the grid (km)
        meta_file: str
            A file containing the file-names that should be hashed through this class. Should be in the same folder as the data_path
        data_path: str
            The folder where the trajectories are stored
        """

        self.name = name
        self.x_len = x_len
        self.y_len = y_len
        self.resolution = resolution
        self.meta_file = meta_file
        self.data_path = data_path

    def __str__(self) -> str:
        return f"GridLSH: {self.name}"

    

    

if __name__=="__main__":
    Grid = GridLSH("G1", 3.3, 2, 0.25, "meta.txt", "/data")
    print(Grid)

