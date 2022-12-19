import os,math,csv
import numpy as np
import matplotlib.pyplot as plt 

density_dict=np.load("best_density.npy",allow_pickle=True).item()
best_density={key:density_dict[key]*0.061 for key in density_dict.keys()}

# 获取神经元所在脑区的信息
with open(r'..\Data\Other_Infomation\BoutonDataCellType.csv', 'r', newline='') as csvfile:
    t = csv.reader(csvfile)
    area_data=np.array(list(t))
    csvfile.close()
cell_type=dict()
for root, dirs, files in os.walk(r'..\Data\Noregisted\bouton_swc'):
    for file in files:
        t=file.split('.')[0]
        tt=np.where(area_data[:,0]==t)
        if len(tt[0])==0:
            print(t+' out of file')
        else:
            cell_type[file.split('.')[0]]=str(area_data[tt[0],1][0])
cell_count=dict()
for key in cell_type:
    t=cell_type[key]
    if t not in cell_count:
        cell_count[t]=1
    else:
        cell_count[t]+=1
d=['VPM','MG','VPL','LGd','RT','CP','DG','VISp','SSp-bfd','SSp-m','SSp-ul','SSp-n','RSPv','MOp','MOs','SSs','CLA','AId']
d_t=[[x,cell_count[x],best_density[x]] for x in d]

d_t=np.array(d_t)

xticks=[x[0]+'\nN='+x[1] for x in d_t]
plt.close('all')
fig,ax=plt.subplots(figsize= (10, 5))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Cell type',fontsize=22,fontproperties='Calibri',weight='bold')
plt.ylabel('Bouton density(/um)',fontsize=22,fontproperties='Calibri',weight='bold')

plt.bar(range(0,5),d_t[0:5,2].astype(np.float64),label='Thalamus')
plt.bar(5,d_t[5,2].astype(np.float64),label='Striatum')
plt.bar(6,d_t[6,2].astype(np.float64),label="Hippocampus")
plt.bar(range(7,18),d_t[7:18,2].astype(np.float64),label='Cortex')


plt.legend(prop={'family':'Calibri','weight':'bold','size':22},frameon=False)
plt.xticks(range(0,len(d_t)),xticks,size=12,fontproperties='Calibri',weight='bold')
plt.yticks(size=12,fontproperties='Calibri',weight='bold')#设置大小及加粗


plt.tight_layout()
# plt.savefig('barplot.png', dpi=300)
