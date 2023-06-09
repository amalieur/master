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
  - [x] Rome ED - DTW
  - [x] Rome ED - Frechet
  - [x] Rome DTW - DTW
  - [x] Rome DTW - Frechet
- [x] Use figures from early parameter determination to answer this research question



**RQ2 - Efficiency**
- [X] Measure and save the hash computation time
  - [X] Grid Porto
  - [X] Grid Rome
  - [X] Disk x3 Porto
  - [X] Disk x3 Rome
  - [X] Save the results in TWO tables, one for the grid and one for the disks
- [x] Measure true similarity computation time (DTW only)
  - [x] DTW Porto py (Halfway there)
  - [x] DTW Rome py
  - [ ] Create a common figure for both cities
  - [ ] Frechet for ~ 100 traces for both datasets (As a curiosity more or less)
- [x] Measure the hash similarity computation time (Ensure correct similarity measure is used)
  - [x] Porto Grid Hash
  - [x] Porto Disk Hash
  - [x] Rome Grid Hash
  - [x] Rome Disk Hash
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
- [x] Create clusters over Rome
  - [x] Cluster with True DTW
  - [x] Cluster with True Frechet
  - [x] Cluster with grid hash
  - [x] Cluster with disk hash
- [ ] Cluster analysis:
  - [x] Davies bouldin
    - [x] Porto
    - [x] Rome
  - [x] Rand index?
    - [x] Porto
      - [x] Both grid and disk against dtw and frechet
    - [x] Rome
      - [x] Both grid and disk against dtw and frechet

## Figures and visualisation of data and results 
- [x] Correlation figures visualising the effect of the grid resolution / disk diameter and layers
- [x] Figure showing the effect of number of disks.

### Data
- [x] Simple test method for plotting trajectories

### Results
- [x] Symlink-folder where all csv-result-files are adjacent
- [ ] Folder for all figures containing results.

# Things that should be included in the thesis
## Introduction
- [ ] Introduction
  - [ ] Include an "Outline" chapter which briefly explains what is included in the different sections
  - [ ] Should also write in the outline section that the theory and relevant works chapter is based on the work from the autumn project
## Theory
- [ ] Theory
  - [ ] Perhaps add some more on the topic off locality senstive hashing. Make sure that it is highly understandable for the thesis. Should rewrite the section so that it is more in touch with the version we have used in our project. Presenter først vanlig teori, for så å si at ved å ta utgangspunkt i prinsippet om datalokalitet gjennom hashing, kan bruke teknikken til mer enn bare near-neighbour. Vårt øsnke er å se om det fungerer som distansemål også. 
  - [ ] Remove Affinity Propagation from the clustering subchapter -  no need to include it as I am not using it.
  - [ ] Write more on the topic of rand index. What is it intuitively and so on... What does the score mean? (Share of common objects over the share of common objects and uncommon objects) 
  - [ ] Remove Silhouette coefficient - not in use
 
## Relevant Work
- [ ] Relevant work
  - [ ] Should be fine for now
  
## Methodology


# Aspects to potentially be included in the discussion:

Dataen som er benyttet har er ikke labelet og har heller ingen forhåndsdefinert mønster, slik at vi kan forvente å få klare og tydelige clusters. Sporene er valgt vilkårlig, og siden de opererer innenfor trafikkmønster kan vi anta at dataen inneholder et visst mønster. Det er fair å gå ut i fra at dersom man hadde hatt testdata som inneholder tydeligere clustere, kunne man sannsynligvis scoret høyere på clustering - scopet for denne oppgaven er imidlertid ikke å lage tydelige clustere, men å sammenlikne hvorvidt LSH og true similarities korrelerer.

Også et avsnitt om hvorvidt generering av diskLSH hashes har tilstrekkelig kjøretid. I tidlig februar tok genereringen av hashes i snitt et minutt or tusen spor.... For å redusere denne tiden har vi implementert et quadrant som splitter arealet i fire deler, og slikt sett eliminerer mange av diskene som må kontrolleres om toucher hvert punkt. Dette ga redusert kjøretid. Det ble også ytterligere implementert et KD-tree for å øke hatigheteten på denne prosessen. KD-treet medførte betydelig kortere kjøretid, og dette er verdt å bruke litt tid på i rapporten.  Sammenlikner man med gridLSH så tar den samme prosessen under et sekund, men til forsvar så gjøres det kun enkel aritmetiske beregninger for hvert punkt i denne hashen. I DiskLSH må man først finne hvilke disker som er innenfor punktet og ha en "within" control. Se koden for yttterligere dokumentasjon.

Vi gar benyttet euclidean distance i disk-lsh for beregning av hashene og hvilke disker et punkt befinner seg i. Dette gir ikke en riktig fremstilling av en disk, mer en ellipseform grunnet at geo-koordinater (lat,lon) ligger til grunn for avstandsberegningene. For økt nøykatightet kunne det vært spennende å se hvorvidt det faktisk har en innvirkning. Uansett mener vi at avveiingen some er gjort tilfreddstiller "kravene" bak disk-based LSH av trajectories. 


Som videre arbeid kan det være spennende å trekke frem utforsking av grid hashes med grovt rutenett. 0.6 i korrelasjon. Ref figurene som viser korrelasjon. 



Diskutere effekten av clustering resultat. Kan vi trekke noe reelt ut av disse resultatene. Viktig å reflektere rundt DavisBouldin indeksen og andre valgte indekser


Litt usortert før jeg har generert clustere over hash-similaritetene men: Observerer at frechet distanse danner penere clustere enn dtw. Ettersom vi har høyere korrelasjon mot frechet distanse enn dtw, kan man muligens anta at clustrene vil kunne være "relativt" penere enn dtw - et interessant diskusjonspunkt i forhold til praktisk anvendelse av hash-similaritetene. 


- [ ] Diskutere effekten av gridoppløsning/ antall disker.


Svært viktig at jeg diskuterer det faktum at selv om diskhash oppnådde bedre resultater enn gridhash, så er det potensielt et resultat av bedre konfigurasjon. Ved å øke antallet lag/ grid-oppløsning og tilsvarende for diskhashene vil man kunne oppnå høyere nøyaktighet osv. Eksperimentene våre har vist noe bedre nøyaktighet for diskhash, men diskhashsimilarity hadde også litt lenger kjøretid -> Kunne man fått økt nøyaktigheten til gridsene om man hadde endret parametrene til mer finkornede slik at kjøretiden hadde blitt den samme? Bare et tankesprang det her. Men viktig å få med at hashene tilbyr en tradeoff mellom kjøretid og nøyaktighet.


- [ ] Også drøfte litt rundt at test-eksperimentene ha en høyere korrelasjon mot sannhetsverdiene enn det som var tilfelle når similaritetene for hele datasettet ble beregnet. (Korrelasjonen som er på 2dhistogrammene). Kan det skyldes at økningen i antall spor burde ha mer finmaskede grids for å skille sporene bedre? Ser ikke helt den samme effekten for disks, men det er en liten endring her også... 



# Konklusjon
  Vi har vist at disk og grid fungerer godt til formålet dersom parametrene er innenfor riktig vindu. Dvs innenfor akseptabel tidskompleksitet, men samtidig store nok til at høy korrelasjon med sanne verdier er vedlikeholdt. 
  Vi har derfor vist at LSH-skjemaene er gjenbrukbare til similaritetsberegning, dog med noe redusert nøyaktighet, men til gjengjeld kraftig redusert kjøretid.

  Vi har i 2d-histogrammene sett at grid-verdiene er litt mer spredte enn det man hadde håpet på, men at korrelasjonen fortsatt er akseptabel. Diskene har bedre korrelasjon, hvilket tydelig fremkommer av hsitogrammene. Spredningen er key her.  