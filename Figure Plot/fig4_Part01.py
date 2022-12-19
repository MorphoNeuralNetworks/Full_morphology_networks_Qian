import os
import numpy as np
import matplotlib.pyplot as plt

methods=['all','axon','dendrite']
colorlist={'1':'#FFB6C1','2':'#6495ED','3':'#FFA500'}

def changeNPY(cc):
    temp=dict()
    temp['node_number']=cc[0][0]
    temp['edge_number']=cc[0][1]
    temp['degree_dis_x_log']=cc[1]
    temp['degree_dis_y_log']=cc[2]
    temp['traid_census_y_log']=cc[3]
    return temp

feature_dict_bouton={}
feature_dict_boutondensity_all={}
feature_dict_boutondensity_each={}
folderpath = os.listdir(r'..\BrainNetwork_Pertubation\Pertubation')
cc=np.load(r'..\BrainNetwork\normal_bouton.npy',allow_pickle=True)
feature_dict_bouton['normal']=changeNPY(cc)
for x in folderpath:
    cc=np.load('..\\BrainNetwork_Pertubation\\graph_feature\\'+x+'_bouton.npy',allow_pickle=True)
    feature_dict_bouton[x]=changeNPY(cc)

# folderpath = os.listdir(r'..\BrainNetwork_Pertubation_density_all\Pertubation')
# cc=np.load(r'..\BrainNetwork\normal_boutondensity_all.npy',allow_pickle=True)
# feature_dict_boutondensity_all['normal']=changeNPY(cc)
# for x in folderpath:
#     cc=np.load('..\\BrainNetwork_Pertubation_density_all\\graph_feature\\'+x+'_boutondensity_all.npy',allow_pickle=True)
#     feature_dict_boutondensity_all[x]=changeNPY(cc)

folderpath = os.listdir(r'..\BrainNetwork_Pertubation_density_each\Pertubation')
cc=np.load(r'..\BrainNetwork\normal_boutondensity_each.npy',allow_pickle=True)
feature_dict_boutondensity_each['normal']=changeNPY(cc)
for x in folderpath:
    cc=np.load('..\\BrainNetwork_Pertubation_density_each\\graph_feature\\'+x+'_boutondensity_each.npy',allow_pickle=True)
    feature_dict_boutondensity_each[x]=changeNPY(cc)


### 对于bouton网络三种操作画在一起 degree distribution
plt.close()
fig,ax=plt.subplots(figsize=(5,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
data_list=[]
method=methods[0]   
name='scale_0.5_prune_0_delete_0_'+method
x_t1=feature_dict_bouton[name]['degree_dis_x_log']
y_t1=feature_dict_bouton[name]['degree_dis_y_log']

x_t2=feature_dict_bouton['normal']['degree_dis_x_log']
y_t2=feature_dict_bouton['normal']['degree_dis_y_log']     


name='scale_0_prune_0.5_delete_0_'+method
x_t3=feature_dict_bouton[name]['degree_dis_x_log']
y_t3=feature_dict_bouton[name]['degree_dis_y_log']
x_t4=feature_dict_bouton['normal']['degree_dis_x_log']
y_t4=feature_dict_bouton['normal']['degree_dis_y_log']

name='scale_0_prune_0_delete_0.5_all'
x_t5=feature_dict_bouton[name]['degree_dis_x_log']
y_t5=feature_dict_bouton[name]['degree_dis_y_log']


plt.fill_between(x_t1, y_t1, y_t2[0:len(y_t1)], facecolor="#d62728", alpha=0.4)
plt.fill_between(x_t3, y_t3, y_t4[0:len(y_t3)], facecolor="#2ca02c", alpha=0.5)
plt.fill_between(x_t5, y_t5, y_t2[0:len(y_t5)], facecolor="#9467bd", alpha=0.8)
plt.plot(x_t2,y_t2,alpha=1,c='#1f77b4',linewidth=3)
plt.legend(['Scale:0.5-1.0','Prune:0.5-1.0','Delete:0.5-1.0','Non-Perturbed'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False)
plt.fill_between(x_t2[len(y_t1)-1:],0, y_t2[len(y_t1)-1:], facecolor="#d62728", alpha=0.4)
plt.fill_between(x_t4[len(y_t3)-1:],0, y_t4[len(y_t3)-1:], facecolor="#2ca02c", alpha=0.5)
plt.fill_between(x_t2[len(y_t5)-1:],0, y_t2[len(y_t5)-1:], facecolor="#9467bd", alpha=0.8)
plt.plot(x_t1,y_t1,alpha=0.7,c="#d62728",linewidth=1.5)
# plt.plot(x_t2,y_t2,alpha=0.7,c=colorlist['1'],linewidth=2)
plt.plot(x_t5,y_t5,alpha=0.7,c="#2ca02c",linewidth=1.5)
plt.plot(x_t3,y_t3,alpha=0.7,c="#9467bd",linewidth=1.5)
# plt.title('Degree distribution on predicted bouton network')
plt.xticks([0,1,2],['1','10','100'],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([0,1,2,3],['1','10','100','1000'],size=14,fontproperties='Calibri',weight='bold')
plt.xlabel('Degrees(log)',fontsize=22,fontproperties='Calibri',weight='bold')
plt.ylabel('Frequency(log)',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('Degree distribution 1.png', dpi=300)
'''
plt.close()
fig,ax=plt.subplots(figsize=(10,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
data_list=[]
method=methods[0]   
name='scale_0.5_prune_0_delete_0_'+method
x_t1=feature_dict_bouton[name]['degree_dis_x_log']
y_t1=feature_dict_bouton[name]['degree_dis_y_log']

x_t2=feature_dict_bouton['normal']['degree_dis_x_log']
y_t2=feature_dict_bouton['normal']['degree_dis_y_log']   
  

name='scale_0.5_prune_0_delete_0_'+method
x_t5=feature_dict_boutondensity_each[name]['degree_dis_x_log']
y_t5=feature_dict_boutondensity_each[name]['degree_dis_y_log']

x_t6=feature_dict_boutondensity_each['normal']['degree_dis_x_log']
y_t6=feature_dict_boutondensity_each['normal']['degree_dis_y_log']  

plt.fill_between(x_t1, y_t1, y_t2[0:len(y_t1)], facecolor="#1f77b4", alpha=0.4)
plt.fill_between(x_t5, y_t5, y_t6[0:len(y_t5)], facecolor="#ff7f0e", alpha=0.4)
plt.legend(['Predicted Scale:0.5-1.0','Uniform Scale:0.5-1.0'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False)
plt.fill_between(x_t2[len(y_t1)-1:],0, y_t2[len(y_t1)-1:], facecolor="#1f77b4", alpha=0.4)
plt.fill_between(x_t6[len(y_t5)-1:],0, y_t6[len(y_t5)-1:], facecolor="#ff7f0e", alpha=0.4)
plt.plot(x_t1,y_t1,alpha=0.7,c="#1f77b4",linewidth=1.5)
plt.plot(x_t2,y_t2,alpha=0.7,c="#1f77b4",linewidth=3)
plt.plot(x_t5,y_t5,alpha=0.7,c="#ff7f0e",linewidth=1.5)
plt.plot(x_t6,y_t6,alpha=0.7,c="#ff7f0e",linewidth=3)
# plt.title('Degree distribution of two networks')
plt.xticks([0,1,2],['1','10','100'],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([0,1,2,3],['1','10','100','1000'],size=14,fontproperties='Calibri',weight='bold')
plt.xlabel('Degrees(log)',fontsize=22,fontproperties='Calibri',weight='bold')
plt.ylabel('Frequency(log)',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
plt.savefig('Degree distribution of two networks.png', dpi=300)
'''

'''
### 对于三种网络在一起 degree distribution
plt.close()

data_list=[]
for method in methods[0:1]:
    temp=[]
    for x in [5,20]:
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t=feature_dict_bouton[name]['degree_dis_x_log']
        y_t=feature_dict_bouton[name]['degree_dis_y_log']
        plt.scatter(x_t,y_t,marker='+',alpha=0.7)

    for x in [5,20]:
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t=feature_dict_boutondensity_all[name]['degree_dis_x_log']
        y_t=feature_dict_boutondensity_all[name]['degree_dis_y_log']
        plt.scatter(x_t,y_t,marker='o',alpha=0.7)

    for x in [5,20]:
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t=feature_dict_boutondensity_each[name]['degree_dis_x_log']
        y_t=feature_dict_boutondensity_each[name]['degree_dis_y_log']
        plt.scatter(x_t,y_t,marker='s',alpha=0.7)

plt.title('Degree distribution-Scale')
plt.legend(['Bouton_Scale:0.5','Bouton_Scale:2.0','DensityAll_Scale:0.5','DensityAll_Scale:2.0','DensityEach_Scale:0.5','DensityEach_Scale:2.0'])
plt.xticks([0,1,2,3],['1','10','100','1000'])
plt.yticks([0,1,2,3],['1','10','100','1000'])
plt.xlabel('Degrees(log)',fontsize=12)
plt.ylabel('Frequency(log)',fontsize=12)
'''
