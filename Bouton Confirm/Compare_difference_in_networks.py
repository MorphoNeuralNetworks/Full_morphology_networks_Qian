##用于统计两个网络之间变化最大的neurons以及cell type
import numpy as np
import csv,os,random
import matplotlib.pyplot as plt

bouton_map=np.load('../BrainNetwork/bouton_connection.npy',allow_pickle=True)
boutondensity_each_map=np.load('../BrainNetwork/boutondensity_each_connection.npy',allow_pickle=True)

neuron_set=list(set(bouton_map[:,0].tolist()+boutondensity_each_map[:,0].tolist()))
value_dict_bouton={x:[0,0]for x in neuron_set}
for x in bouton_map:
    value_dict_bouton[x[0]]=[value_dict_bouton[x[0]][0]+x[3],value_dict_bouton[x[0]][1]+1]
value_dict_boutondensity={x:[0,0]for x in neuron_set}
for x in boutondensity_each_map:
    value_dict_boutondensity[x[0]]=[value_dict_boutondensity[x[0]][0]+x[3],value_dict_boutondensity[x[0]][1]+1]

value_dict={x:[0,0]for x in neuron_set}
for key in value_dict_bouton.keys():
    if value_dict_bouton[key][1]==0:
        continue
    value_dict[key]=[value_dict_bouton[key][0]/value_dict_bouton[key][1],value_dict[key][1]]
for key in value_dict_boutondensity.keys():
    if value_dict_boutondensity[key][1]==0:
        continue
    value_dict[key]=[value_dict[key][0],value_dict_boutondensity[key][0]/value_dict_boutondensity[key][1]]

score=[]
for key in value_dict.keys():
    if value_dict[key][0]!=0:
        score.append([key,value_dict[key][1]/value_dict[key][0]]) 

score=np.array(score)

score = score[np.argsort(-score[:,1].astype(np.float64))]


## 给出这些neuron的celltype
soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
celltype=[soma_info[x[0]][0] for x in score]


# ## 统计cell type的平均变化
celltype_ave={x:[0,0] for x in list(set(celltype))}
for x in score:
    t=soma_info[x[0]][0]
    celltype_ave[t]=[celltype_ave[t][0]+float(x[1]),celltype_ave[t][1]+1]
celltype_ave_list=dict()
for key in celltype_ave.keys():
    if celltype_ave[key][1]>=10:
        celltype_ave_list[key]=[ celltype_ave[key][0]/celltype_ave[key][1],celltype_ave[key][1]] 
