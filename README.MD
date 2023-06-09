# Code repository for master thesis project

This repo includes code and experiments. Experiments mainly conducted in jupyter notebooks and written in python scripts.

## Description
/data folder contains the chosen trajectories that the experiments was conducted on, extracted from the raw_data subfolder. 

/figures folder contains the output figures from the conducted experiments.

/code folder contains:
- Jupyter notebooks where experiments was conducted
- /benchmarks - code for computing the true similarities, as well as the computed similarities
- /experiments - code for all experiments, as well as the hashed similarities and timing data.
- /schemes - implementation of the LSH schemes (disk_lsh.py & grid_lsh.py), including the timing of hash computation.
- /utils - Mostly helper functions used throughout this project 

/results - Symlink folder containing similarities and timing-results


## NOTES:

"traj-dist" module have been used for similarity computation in this research. Package installed directly as a dependency in this project from: https://github.com/bguillouet/traj-dist

"py_edp" as an option in similarity computation is in reality the dtw distance between the inputs. Not edit distance penalty as the name of the file suggests.
