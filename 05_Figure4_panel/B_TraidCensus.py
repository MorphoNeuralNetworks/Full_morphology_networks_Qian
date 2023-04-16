import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

methods=['all','axon','dendrite']
colorlist={'1':'#FFB6C1','2':'#6495ED','3':'#FFA500'}

feature_dict_bouton=np.load("../Data/Perturbation_Data/feature_dict_bouton.npy",allow_pickle=True).item()
feature_dict_boutondensity_each=np.load("../Data/Perturbation_Data/feature_dict_boutondensity_each.npy",allow_pickle=True).item()

'''
## impact of three operations on the network
plt.close("all")
fig,ax=plt.subplots(figsize=(8,3))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
data_list=[]
method=methods[0]
# select parameter    
name='scale_0.5_prune_0_delete_0_'+method
data_list.append(feature_dict_bouton[name]['traid_census_y_log'])
  
name='scale_0_prune_0.5_delete_0_'+method
data_list.append(feature_dict_bouton[name]['traid_census_y_log'])

name='scale_0_prune_0_delete_0.5_all'
data_list.append(feature_dict_bouton[name]['traid_census_y_log'])

data_list.append(feature_dict_bouton['normal']['traid_census_y_log'])

for i in range(3):
    for j in range(16):
        data_list[i][j]=data_list[i][j]-data_list[3][j]

# plot figure
bar_width=0.3
plt.bar(np.arange(1,17)+bar_width*0, data_list[0], bar_width, align="center",alpha=0.7,color=["#d62728"])
plt.bar(np.arange(1,17)+bar_width*1, data_list[1], bar_width, align="center",alpha=0.7,color=["#2ca02c"])
plt.bar(np.arange(1,17)+bar_width*2, data_list[2], bar_width, align="center",alpha=0.7,color=["#9467bd"])
# plt.bar(np.arange(1,17)+bar_width*3, data_list[3], bar_width, align="center",alpha=0.7)

# plt.title('Triad census on Predicted network')
# plt.legend(['Scale:0.5/Non-Perturbed','Prune:0.5/Non-Perturbed','Delete:0.5/Non-Perturbed'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([-3,-2,-1,0],["0.001","0.01","0.1","1"],size=14,fontproperties='Calibri',weight='bold')
# plt.xlabel('States',fontsize=12)
plt.ylabel('Times(log)',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('triad census 1.pdf', dpi=300)
'''


## impact of scale on two networks
plt.close("all")
fig,ax=plt.subplots(figsize=(8,3))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
data_list=[]
method=methods[0]   
# select parameter  
name='scale_0.5_prune_0_delete_0_'+method
data_list.append(feature_dict_bouton[name]['traid_census_y_log'])
data_list.append(feature_dict_bouton['normal']['traid_census_y_log'])
  
name='scale_0.5_prune_0_delete_0_'+method
data_list.append(feature_dict_boutondensity_each[name]['traid_census_y_log'])
data_list.append(feature_dict_boutondensity_each['normal']['traid_census_y_log'])

for j in range(16):
    data_list[0][j]=data_list[0][j]-data_list[1][j]
for j in range(16):
    data_list[2][j]=data_list[2][j]-data_list[3][j]

bar_width=0.4
plt.bar(np.arange(1,17)+bar_width*0, data_list[0], bar_width, align="center",alpha=0.9,color=["#1f77b4"])
plt.bar(np.arange(1,17)+bar_width*1, data_list[2], bar_width, align="center",alpha=0.9,color=["#ff7f0e"])

# plt.title('Triad census of two networks')
# plt.legend(['Predicted Scale:0.5/Non-Perturbed','Uniform Scale:0.5/Non-Perturbed'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([-3,-2,-1,0],["0.001","0.01","0.1","1"],size=14,fontproperties='Calibri',weight='bold')
# plt.xlabel('States',fontsize=12)
plt.ylabel('Times(log)',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('triad census 2.pdf', dpi=300)
