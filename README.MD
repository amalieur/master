# Repository to perform experiments for TDT4900 - Computer Science, Master's Thesis  

This work is a collaboration between Amalie Udrshals and Andrea Hetlevik Vanebo.  

## Description
/data folder contains the chosen data the experiments were conducted on.  
/code folder contains:
- The main Jupyter notebook running the whole experiment, [taxi-similarity.ipynb](./code/taxi-similarity.ipynb)
- Jupyter notebooks running the different parts of the experiments 
- /experiments/results: The resulting plots and CSV files
- /experiments/timing: The time consumption of the experiments
- /schemes - implementation of the LSH schemes (disk_lsh.py & grid_lsh.py).
- /utils - Mostly helper functions used throughout this project 



## NOTES:

Repository cloned from https://github.com/bjorafla/master and edited to suit our needs, as our work is a real-world application of the results of that experiment.

The "traj-dist" module has been used for similarity computation in this research. Package installed directly as a dependency in this project from: https://github.com/bguillouet/traj-dist
