"""
Superclass for LSHschemes
"""

class LSHInterface:
    """ Interface for LSH classes"""

    def read_meta_file(self, path: str, file_name: str) -> None:
        """ Read the meta_data_file """
        pass

    def read_data_file(self, path: str) -> list:
        """ Read a trajectory file """
        pass

    def load_files(self, path: str, meta_file: str) -> None:
        """ Loads the trajectory data into memory """
        pass

    def write_file(self, output_path: str) -> None:
        """ Write a file to a given path """
        pass

    def hash_trajectory(self, trajectory: list[tuple[float]]) -> list:
        """ Hashes a trajectory through the created grid """
        pass

    def compute_grid_distortion(self, x_len: float, y_len: float, resolution: float) -> float:
        """ Compute a random grid distortion off the resolution,"""
        pass

    