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
- [ ] Ensure that traces are of a certain length, and that the distance between start and end-point are great enough


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
  - [X] Rome
- [X] Creation of similarity data (Frechet - true similarities (SLOW as hell... -> Should be a one-time job but still slooooow :/))
  - [x] Porto
  - [X] Rome
- [x] Storing test-data (benchmarks-folder)
- [x] Implement edit-distance method for the schemes hashes
- [x] Implement methods to measure the time similarity computation time
  - [ ] Method that saves the measurement times (perhaps as df)
  - [ ] Method that visualise the compuation time
- [ ] Implement methods to measure the hash similarity computation time
- [ ] Implement methods to compare dataframes containing similarities
  - [ ] Method that computes correlation
  - [ ] Method that visualises the correlations using figures
  - [ ] Method that ...

**important**
- [ ] Rewrite edit distance so that the distance corresponds to actual distance and not just a binary relation

### Experiments:

**RQ2 - Efficiency**
- [ ] Measure and save the hash computation time
  - [ ] Grid Porto
  - [ ] Grid Rome
  - [ ] Disk x3 Porto
  - [ ] Disk x3 Rome
- [ ] Measure true similarity computation time (all sets for DTW (py and cy), perhaps one for frechet)
  - [ ] DTW Porto py and cy for all set-sizes
  - [ ] DTW Rome py and cy for all set-sizes
  - [ ] Frechet for ~ 100 traces for both datasets (perhaps only cy)
- [ ] Measure the hash similarity computation time (all sets using edit-distance)
  - [ ] Porto Grid Hash
  - [ ] Porto Disk Hash
  - [ ] Rome Grid Hash
  - [ ] Rome Disk Hash
- [ ] Figure and visualising
  - [ ] Computation time figures true similarities
  - [ ] Creation of hash time figures
  - [ ] Hash similarity computation times

**RQ2 - Accuracy**
- [ ] Measure the similarity accuracy
  - [ ] Correlation between hash computation and true similarities
  - [ ] 
## Figures and visualisation of data and results 

### Data
- [x] Simple test method for plotting trajectories

### Results







# Aspects to potentially be included in the discussion:

Dataen som er benyttet har er ikke labelet og har heller ingen forhåndsdefinert mønster, slik at vi kan forvente å få klare og tydelige clusters. Sporene er valgt vilkårlig, og siden de opererer innenfor trafikkmønster kan vi anta at dataen inneholder et visst mønster. Det er fair å gå ut i fra at dersom man hadde hatt testdata som inneholder tydeligere clustere, kunne man sannsynligvis scoret høyere på clustering - scopet for denne oppgaven er imidlertid ikke å lage tydelige clustere, men å sammenlikne hvorvidt LSH og true similarities korrelerer.

Også et avsnitt om hvorvidt generering av diskLSH hashes har tilstrekkelig kjøretid. I tidlig februar tok genereringen av hashes i snitt et minutt or tusen spor.... For å redusere denne tiden har vi implementert et quadrant som splitter arealet i fire deler, og slikt sett eliminerer mange av diskene som må kontrolleres om toucher hvert punkt. Dette ga redusert kjøretid. Det ble også ytterligere implementert et KD-tree for å øke hatigheteten på denne prosessen. KD-treet medførte betydelig kortere kjøretid, og dette er verdt å bruke litt tid på i rapporten.  Sammenlikner man med gridLSH så tar den samme prosessen under et sekund, men til forsvar så gjøres det kun enkel aritmetiske beregninger for hvert punkt i denne hashen. I DiskLSH må man først finne hvilke disker som er innenfor punktet og ha en "within" control. Se koden for yttterligere dokumentasjon.

Vi gar benyttet euclidean distance i disk-lsh for beregning av hashene og hvilke disker et punkt befinner seg i. Dette gir ikke en riktig fremstilling av en disk, mer en ellipseform grunnet at geo-koordinater (lat,lon) ligger til grunn for avstandsberegningene. For økt nøykatightet kunne det vært spennende å se hvorvidt det faktisk har en innvirkning. Uansett mener vi at avveiingen some er gjort tilfreddstiller "kravene" bak disk-based LSH av trajectories. 

Kan evnt trekke inn et avsnitt der cython/python diskuteres kort og valg rundt dette under effektivitetsanalysen av hash-generering / similarity-beregning

