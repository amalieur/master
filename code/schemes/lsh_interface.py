"""
Superclass for LSHschemes
"""

class LSHInterface:
    """ Interface for LSH classes"""

    def read_meta_file(self, file_path: str) -> list:
        """ 
        Read the meta_data_file 

        Parameters
        ---
        file_path : str
            The file_path of the meta-file containing the dataset

        Returns
        ---
        A list containing the file name of each trajectory in the set
        """
        pass

    def read_data_file(self, file_path: str) -> list:
        """ 
        Read a trajectory file and return the content as a two-dimesional list 
        
        Parameters
        ---
        file_path : str
            The file_path of the trajectory file

        Returns
        ---
        A list containing the coordinates of the trajectory
        """
        pass

    def load_files(self, file_path: str) -> None:
        """ 
        Loads the trajectories of a given dataset into memory
        
        Parameters
        ---
        file_path : str
            The file_path of the met

        """
        pass

    def write_file(self, output_path: str) -> None:
        """ Write a file to a given path """
        pass

    def hash_trajectory(self, trajectory: list[tuple[float]]) -> list:
        """ Hashes a trajectory through the created grid """
        pass

   

    