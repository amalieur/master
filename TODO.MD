# Things that should be done in this project

This file contains the tasks and things that need to be done during development. It will partially serve the purpose of a backlog, and partially as a log for what is done and still needs to be done.


---

## Data preparation
    
- [x] Decide on and create a file-structure that will be used for the project
- [X] Decide on and implement a naming convention for the trajectories


### **Porto**

- [x] Ensure data are within bounded rectangle
- [x] Ensure that traces holds a minimum length
- [x] Ensure traces with invalid data points are removed
- [x] Abiltiy to write trajectories to files and to clear old files

### Common

- [x] Split datasets using meta-files (100 - 200 - ... - 1000)
- [x] Added support for the creation of a smaller test-set of a given size

---

## Development


### Utilities-functions

- [x] Alphabetical incrementer for naming trajectory files
- [x] File handler for reading trajectories
- [x] Meta file handler for retrieving the datasets
- [x] Distance function for the computation of distance beween any two coordinates

### Scheme creation

- [x] Add a common interface with a minimum number of functionality that both schemes should implement
- [x] Create and implement hash naming conventions for both schemes
- [x] Adjust measuring method to use nanosecond timing (add _ns as postfix to the timer object)

**Grid shemes**
- [x] Create a class for gridLSH objects
- [x] Implement grid distortion
- [x] Add grid layers
- [x] Implement hash function and methods
- [x] Print functions
- [x] Save data and meta-files
- [x] Create a procedure-oriented jupyter notebook for streamlining the grid LSH creation process
- [x] Finalize notebook with updated ways of measuring generation speed
- [x] Implement functions so that the time needed to create the hashes can be measured, (Without I/O)


**Disk schemes**
- [x] Create a class for diskLSH objects
- [x] Implement random disk deployment for each layer
- [x] Implement layers
- [x] Print functions
- [x] Save data and meta-files
- [x] Procedure-oriented notebook for streamlining the disk LSH creation process
- [x] Finalize notebook with updated ways of measuring generation speed
- [x] Function that can be used for measuring the actual hashing process 
- [x] Implement a quad-like-tree (no tree really, just four quadrants) for improvement in runtime
- [x] Implement KD-tree during hash generation -> Potentially huge improvement in runtime
- [x] Add measuring methods for the additional trees
 
---
## Experimental part

### Preparations:
- [x] Implement code that can be used for similarity computation
- [x] Implement multiple processing code so that true similarities can be comoputed faster for me
- [x] Create a procedure-oriented notebook for the benchmarks
- [x] Creation of similarity data (DTW - true similarities)
  - [X] Porto

- [X] Creation of similarity data (Frechet - true similarities (SLOW as hell... -> Should be a one-time job but still slooooow :/))
  - [x] Porto
- [x] Storing test-data (benchmarks-folder)
- [x] Implement edit-distance method for the schemes hashes
- [x] Implement methods to measure the time similarity computation time
  - [x] Rewrite so that the methods use the correct hash
  - [x] Method that saves the measurement times (perhaps as df)
  - [x] Method that measure the compuation time (Table is enough i think)
- [x] Implement methods to measure the hash similarity computation time
- [x] Implement methods to compare dataframes containing similarities
  - [x] Method that computes correlation
  - [x] Method that visualises the correlations using figures

**Important**
- [x] Rewrite edit distance so that the distance corresponds to actual distance and not just a binary relation. Should consider DTW
- [x] Evaluate which distance to be used at the hashes(EDR variant working decent > correlation)

---
## Experiments:

The following tasks are directly related to answering the research questions in this thesis

**RQ1 - Adaptable/Reproducible to similarity computation**
- [x] Experimental correlation with different distance measures and methods
  - [x] Porto ED - DTW
  - [x] Porto ED - Frechet
  - [x] Porto DTW - DTW
  - [x] Porto DTW - Frechet
- [x] Use figures from early parameter determination to answer this research question



**RQ2 - Efficiency**
- [X] Measure and save the hash computation time
  - [X] Grid Porto
  - [X] Disk x3 Porto
  - [X] Save the results in TWO tables, one for the grid and one for the disks
- [x] Measure true similarity computation time (DTW only)
  - [x] DTW Porto py (Halfway there)
  - [x] Create a common figure for both cities
- [x] Measure the hash similarity computation time (Ensure correct similarity measure is used)
  - [x] Porto Grid Hash
  - [x] Porto Disk Hash
- [x] Figure, tables and visualising
  - [] Computation time figures true similarities
  - [X] Creation of hash time figures
  - [X] Computation times hash similarities - table

**RQ2 - Accuracy**
- [x] Measure the similarity accuracy
  - [x] Correlation between hash computation and true similarities - Generated binplots over the values
  - [ ] Think it is important to show that the deviation is big, and that the results are dependent on random features (random grids and random disks)

**RQ3 - Clustering**

- [x] Implement HCA and AP
- [x] Implement method that displays the clusters
  - [ ] Might adjust tiny bit to better visability
- [x] Rewrite to class method
- [x] Decide which one to use - perhaps both
  - [x] Going further with HCA, allows us to choose number of clusters. 
- [x] Create clusters over Porto
  - [x] Cluster with True DTW
  - [x] Cluster with True Frechet
  - [x] Cluster with grid hash
  - [x] Cluster with disk hash
- [ ] Cluster analysis:
  - [x] Davies bouldin
    - [x] Porto
  - [x] Rand index?
    - [x] Porto
      - [x] Both grid and disk against dtw and frechet

## Figures and visualisation of data and results 
- [x] Correlation figures visualising the effect of the grid resolution / disk diameter and layers
- [x] Figure showing the effect of number of disks.

### Data
- [x] Simple test method for plotting trajectories

### Results
- [x] Symlink-folder where all csv-result-files are adjacent
- [x] Folder for all figures containing results.