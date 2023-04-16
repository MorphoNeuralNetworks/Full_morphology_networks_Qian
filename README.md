# Full morphology networks

This is the code for the paper "The effect of full morphological reconstruction details on whole brain single cell networks" (doi:)  
### Content
### Data Process
code for generating data  
  - [Data Process/ExtractSwcFiles/](https://github.com/MorphoNeuralNetworks/Full_morphology_networks_Qian/blob/main/01_Data%20Process/01_ExtractSwcFiles.py): extract the swc file before and after registration from the raw eswc file   
  - [Data Process/AddPoint/](): resample the file to add nodes  
  - [Data Process/GetNeuronCelltype/](): get the cell type of neuron  
  - [Data Process/BoutondensityChange/](): convert swc files containing boutons to the corresponding uniformly distributed data using the given bouton density  
  - [Data Process/BoutondensityChange/](): extract the coordinate of boutons  
### Sholl analysis
### TMD analysis
### Network generation
### Perturbation
### Figure 1,2,3,4 panel
### Other tools

* **Bouton Confirm:** code to check the validity of bouton data
* **Bouton Density:** calculate the bouton density of a cell type in a specified area

* **Figure Plot:** code for all figures appearing in the paper
* **Network:** Network generation and analysis
* **Perturbation:** code to perform perturbation and analysis

### Code Contributors

### Publication

### License