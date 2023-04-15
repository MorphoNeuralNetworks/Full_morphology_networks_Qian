import os,math,csv
import numpy as np
import matplotlib.pyplot as plt 

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

density_dict=np.load("../Data/Other_Infomation/best_density.npy",allow_pickle=True).item()
best_density={key:density_dict[key]*0.061 for key in density_dict.keys()}

soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
cell_type={key:soma_info[key][0] for key in soma_info.keys()}
cell_count=dict()
for key in cell_type:
    t=cell_type[key]
    if t not in cell_count:
        cell_count[t]=1
    else:
        cell_count[t]+=1
        
d=['LGd','MG','VPL','VPM','RT','CP','DG','VISp','SSp-ul','MOs','MOp','SSp-n','SSp-bfd','SSp-m','SSs','CLA','AId','RSPv']
d_t=[[x,cell_count[x],best_density[x]] for x in d]

d_t=np.array(d_t)

xticks=[x[0]+'\nN='+x[1] for x in d_t]
plt.close('all')
fig,ax=plt.subplots(figsize= (10, 5))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# plt.xlabel('Cell type',fontsize=22,fontproperties='Calibri',weight='bold')
# plt.ylabel('Bouton density(/um)',fontsize=22,fontproperties='Calibri',weight='bold')

plt.bar(range(0,5),d_t[0:5,2].astype(np.float64),label='Thalamus')
plt.bar(5,d_t[5,2].astype(np.float64),label='Striatum')
plt.bar(6,d_t[6,2].astype(np.float64),label="Hippocampus")
plt.bar(range(7,18),d_t[7:18,2].astype(np.float64),label='Cortex')

plt.legend(prop={'family':'Calibri','weight':'bold','size':18},frameon=False)
plt.xticks(range(0,len(d_t)),xticks,size=12,fontproperties='Calibri',weight='bold')
plt.yticks(size=12,fontproperties='Calibri',weight='bold')#设置大小及加粗

plt.tight_layout()
# plt.savefig('barplot.pdf', dpi=300)

