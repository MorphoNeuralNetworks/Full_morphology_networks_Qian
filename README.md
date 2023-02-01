# Full_morphology_networks_Qian
* **Data Process:**  code for generating data  
  - "BoutonNoRegist.py": Generate neuronal morphology information before and after registration using the .eswc file of the raw data  
  - "AddPoint.py": Resample swc files at 10um intervals
  - "GetNeuronCelltype.py": Determine the cell type of the neuron based on the position of the soma in the CCF and existing information
  - "BoutondensityChange.py": Rearrange the bouton in the swc file by the bouton density of the given cell type so that it becomes uniformly distributed
* **Bouton Confirm:** code to check the validity of bouton data
* **Bouton Density:** calculate the bouton density of a cell type in a specified area

* **Figure Plot:** code for all figures appearing in the paper
* **Network:** Network generation and analysis
* **Perturbation:** code to perform perturbation and analysis