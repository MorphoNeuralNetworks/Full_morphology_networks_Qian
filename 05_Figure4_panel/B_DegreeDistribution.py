'''
Changes in degree distribution after perturbation
'''
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
fig,ax=plt.subplots(figsize=(5,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
data_list=[]
method=methods[0]   
# select parameter 
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

# plot figure
plt.fill_between(x_t1, y_t1, y_t2[0:len(y_t1)], facecolor="#d62728", alpha=0.4)
plt.fill_between(x_t3, y_t3, y_t4[0:len(y_t3)], facecolor="#2ca02c", alpha=0.5)
plt.fill_between(x_t5, y_t5, y_t2[0:len(y_t5)], facecolor="#9467bd", alpha=0.8)
plt.plot(x_t2,y_t2,alpha=1,c='#1f77b4',linewidth=3)
# plt.legend(['Scale:0.5-1.0','Prune:0.5-1.0','Delete:0.5-1.0','Non-Perturbed'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False)
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
# plt.savefig('Degree distribution 1.pdf', dpi=300)
'''

## impact of scale on two networks
plt.close("all")
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
# plt.savefig('Degree distribution of two networks.pdf', dpi=300)
