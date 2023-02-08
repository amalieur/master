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


### **Rome**

- [x] Concatenate the traces from one row per point to one row with a list of points
- [x] Ensure data are within bounded rectangle
- [x] Ensure all traces hold the minimum length
- [x] Remove traces with invalid data points
- [x] Abiltiy to write trajectories to files and to clear old files when refreshing data set

### Common

- [x] Split datasets using meta-files (100 - 200 - ... - 1000)
- [x] Added support for the creation of a smaller test-set of a given size
- [ ] Create and develop statistics methods over the datasets
- [ ] Gather statistics for the two datasets

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
- [ ] Adjust measuring method to use nanosecond timing (add _ns as postfix to the timer object)

**Grid shemes**
- [x] Create a class for gridLSH objects
- [x] Implement grid distortion
- [x] Add grid layers
- [x] Implement hash function and methods
- [x] Print functions
- [x] Save data and meta-files
- [x] Create a procedure-oriented jupyter notebook for streamlining the grid LSH creation process
- [ ] Implement functions so that the time needed to create the hashes can be measured, (Without I/O)


**Disk schemes**
- [x] Create a class for diskLSH objects
- [x] Implement random disk deployment for each layer
- [x] Implement layers
- [x] Print functions
- [x] Save data and meta-files
- [x] Procedure-oriented notebook for streamlining the disk LSH creation process
- [ ] Function that can be used for measuring the actual hashing process 
- [ ] Implement KD-tree during hash generation -> Potentially huge improvement in runtime
 
---
## Experiments

### Preparations:
- [ ] Creation of test-data (DTW / Frechet - true similarities)
- [ ] Storing test-data
- [ ] LCSS vs edit-distance of hashes. Are there any significant differences?
- [ ] 
---

## Figures and visualisation of data and results 

### Data
- [x] Simple test method for plotting trajectories

### Results







# Aspects to potentially be included in the discussion:

Dataen som er benyttet har er ikke labelet og har heller ingen forhåndsdefinert mønster, slik at vi kan forvente å få klare og tydelige clusters. Sporene er valgt vilkårlig, og siden de opererer innenfor trafikkmønster kan vi anta at dataen inneholder et visst mønster. Det er fair å gå ut i fra at dersom man hadde hatt testdata som inneholder tydeligere clustere, kunne man sannsynligvis scoret høyere på clustering - scopet for denne oppgaven er imidlertid ikke å lage tydelige clustere, men å sammenlikne hvorvidt LSH og true similarities korrelerer.

Også et avsnitt om hvorvidt generering av diskLSH hashes har tilstrekkelig kjøretid. I tidlig februar tok genereringen av hashes i snitt et minutt or tusen spor.... Denne prosessen kan trolig speedes opp med multithreaing / multiprocessing. Sammenlikner man med gridLSH så tar den samme prosessen under et sekund