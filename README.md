# Full morphology networks

This is the code for the paper "The effect of full morphological reconstruction details on whole brain single cell networks" (doi:)  
(links to code files are not available)  
### Content
### Data Process
  - [DataProcess/ExtractSwcFiles/](https://github.com/MorphoNeuralNetworks/Full_morphology_networks_Qian/blob/main/01_Data%20Process/01_ExtractSwcFiles.py): extract the swc file before and after registration from the raw eswc file   
  - [DataProcess/AddPoint/](): resample the file to add nodes  
  - [DataProcess/GetNeuronCelltype/](): get the cell type of neuron  
  - [DataProcess/BoutondensityChange/](): convert swc files containing boutons to the corresponding uniformly distributed data using the given bouton density  
  - [DataProcess/BoutondensityChange/](): extract the coordinate of boutons  
### Sholl analysis
  - [Figure1/ShollAnalysis/](): get sholl analysis results for all neurons  
  - [Figure1/GetBoutonDensity/](): curve fitting to obtain bouton density of each neuron and cell type  
### TMD analysis
  - [Figure1_TMD/GetBoutonDensity/](): analysis of structure and bouton distribution using TMD functions  
### Network generation
  - [Figure3/FileCalculation/](): convert the data format and add the length of each node  
  - [Figure3/CombineFiles/](): count the length of axon and dendrite for each neuron within each cube   
  - [Figure3/SingleNeuronConnectivity/](): build the dictionary needed for the network connection  
  - [Figure3/ConnectMatrix/](): generate connection matrix  
  - [Figure3/NetworkGenerate/](): visualizing the network  
### Perturbation
  - [Figure4/Perturbation/](): three kinds of perturbation: scale, prune and delete bouton  
  - [Figure4/ScaleAddDeleteBouton/](): add or remove nodes for bouton density changes caused by scale operations  
### Other tools
  - [OtherTools/GenerateColor/](): generating color dictionaries for brain regions and community detection  
  - [OtherTools/Networkanalysis/](): network analysis to obtain cost, storage capacity and routing efficiency  
  - [OtherTools/GetDenstiy/](): set the cell type and brain area, count bouton number and axon length, then get the bouton density  
### Figure 1,2,3,4 panel
Code for each image in figures  

### Code Contributors
- **Penghao Qian** [@Mr-strlen](https://github.com/Mr-strlen) (Institute for Brain and Intelligence, Southeast University)
- **Linus Manubens-Gil** [@lmanubens](https://github.com/lmanubens) ()

### Publication

### License
