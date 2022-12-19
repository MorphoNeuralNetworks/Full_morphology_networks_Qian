import os,math,csv,nrrd,json
import numpy as np
import matplotlib.pyplot as plt 

from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
import shutil

path='./similar_neuron/'

neuron_list=np.load('neruon_order.npy',allow_pickle=True)
files=[str(x)+'.swc' for x in neuron_list]


pro_bouton_dict=dict()   
pro_axon_dict=dict()
for file in files:
    name=file.split('.')[0]
    temp=np.load('./Bouton_Stat/'+name+'_bouton.npy',allow_pickle=True).item()
    pro_bouton_dict[name]=temp
    temp=np.load('./Bouton_Stat/'+name+'_axon.npy',allow_pickle=True).item()
    pro_axon_dict[name]=temp

pro_list=[]
for i in range(0,len(neuron_list)):
    neuron=neuron_list[i]
    temp=pro_axon_dict[neuron]
    for key in temp.keys():
        if temp[key]>0 and key!="fiber tract" and key not in pro_list :
            pro_list.append(key)

pro_map_bouton=np.zeros((len(neuron_list),len(pro_list)))
total_map=np.zeros((len(neuron_list),len(pro_list)))
pro_map_axon=np.zeros((len(neuron_list),len(pro_list)))
for i in range(0,len(neuron_list)):
    neuron=neuron_list[i]
    temp=pro_bouton_dict[neuron]
    total=0
    for key in temp.keys():
        total+=temp[key]
    total=0
    for key in temp.keys():
        total+=temp[key]
    for key in temp.keys():
        if temp[key]>0 and key!="fiber tract":
            t=pro_list.index(key)
            # pro_map_bouton[i,t]=temp[key]
            total_map[i,t]=temp[key]
            pro_map_bouton[i,t]=temp[key]/total*100
            # pro_map_bouton[i,t]=np.log10(temp[key])
    temp=pro_axon_dict[neuron]
    for key in temp.keys():
        if temp[key]>0 and key!="fiber tract":
            t=pro_list.index(key)
            pro_map_axon[i,t]=temp[key]
            # pro_map_axon[i,t]=np.log10(temp[key])

'''
temp=['SSp-bfd','fiber tracts','SSs','VPL','VPM']
select_list=[pro_list.index(x) for x in temp]
# for i in range(len(pro_list)):
#     t=np.mean(pro_map_bouton,0)[i]
#     if t>0.2:
#         select_list.append(i)
pro_map_axon=pro_map_axon[:,select_list]
pro_map_bouton=pro_map_bouton[:,select_list]
pro_list=np.array(pro_list)
pro_list=pro_list[select_list]

batch_width=0.5
plt.close('all')
fig,ax1=plt.subplots(figsize= (6, 6))
ax1.spines['top'].set_visible(False)
color = 'tab:red'
ax1.set_xlabel('Cell type',fontsize=22,fontproperties='Calibri',weight='bold')
ax1.set_ylabel('Axon length', color=color,fontsize=22,fontproperties='Calibri',weight='bold')
x=np.array(range(0,len(pro_list)))
ax1.boxplot(pro_map_axon,positions=x,widths=0.4,patch_artist=True,
            medianprops={'color': 'red', 'linewidth': '1.5'},
            meanline=True,
            showmeans=True,
            meanprops={'color': 'blue', 'ls': '--', 'linewidth': '1.5'},
            flierprops={"marker": "o", "markerfacecolor": "red", "markersize": 2},  
            boxprops={"facecolor": "white","edgecolor": "tab:red"}
            )
ax1.set_xticks([x+0.25 for x in range(5)])
ax1.set_xticklabels(pro_list,size=14,fontproperties='Calibri',weight='bold',rotation=90)
ax1.tick_params(axis='y', labelcolor=color,labelsize=14)
# ax1.set_yticks([0,1,2,3,4])
# ax1.set_yticklabels(["1","10","1e2","1e3","1e4"],size=14,fontproperties='Calibri',weight='bold')
ax1.set_ylim([-400,24000])
ax1.set_yticks([0,5000,10000,15000,20000])
ax1.set_yticklabels([0,5000,10000,15000,20000],size=14,fontproperties='Calibri',weight='bold')
# y1_label = ax1.get_yticklabels() 
# [y1_label_temp.set_fontname('Calibri') for y1_label_temp in y1_label]

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.spines['top'].set_visible(False)
color = 'tab:blue'
y=np.mean(pro_map_bouton,0)
std=np.std(pro_map_bouton,0)
ax2.boxplot(pro_map_bouton,positions=x+0.51,widths=0.4,patch_artist=True,
            medianprops={'color': 'red', 'linewidth': '1.5'},
            meanline=True,
            showmeans=True,
            meanprops={'color': 'blue', 'ls': '--', 'linewidth': '1.5'},
            flierprops={"marker": "o", "markerfacecolor": "red", "markersize": 2},  
            boxprops={"facecolor": "white","edgecolor": "tab:blue","linewidth": 1.5}
            )

ax2.set_xticks(x)
ax2.set_xticks([x+0.25 for x in range(5)])
ax2.set_xticklabels(pro_list,size=14,fontproperties='Calibri',weight='bold',rotation=90)
ax2.set_ylabel('Bouton number',color=color,fontsize=22,fontproperties='Calibri',weight='bold')
ax2.tick_params(axis='y', labelcolor=color,labelsize=14)
ax2.set_ylim([-40,2400])
ax2.set_yticks([0,500,1000,1500,2000])
ax2.set_yticklabels([0,500,1000,1500,2000],size=14,fontproperties='Calibri',weight='bold')
# ax2.set_yticks([0,1,2,3])
# ax2.set_yticklabels(["1","10","1e2","1e3"],size=14,fontproperties='Calibri',weight='bold')
# plt.legend(prop={'family':'Calibri','weight':'bold','size':22},frameon=False)
plt.tight_layout()
# plt.savefig('boxplot.png', dpi=300)


##  coefficient_of_variation
def coefficient_of_variation(data):
    mean=np.mean(data) #计算平均值
    std=np.std(data,ddof=0) #计算标准差
    cv=std/mean
    return cv

plt.close('all')
fig,ax=plt.subplots(figsize= (6, 4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Cell type',fontsize=22,fontproperties='Calibri',weight='bold')
plt.ylabel('Coefficient of variation',fontsize=22,fontproperties='Calibri',weight='bold')

bar_width=0.4
x=np.array(range(0,len(pro_list)))
y1=[coefficient_of_variation(pro_map_axon[:,i]) for i in range(len(pro_list))]
y2=[coefficient_of_variation(pro_map_bouton[:,i]) for i in range(len(pro_list))]

plt.bar(x, y1, bar_width, align="center",color='tab:blue',label='Axon length')
plt.bar(x+bar_width*1, y2, bar_width, align="center",color=['#ff7f0e'],label='Bouton number')


plt.legend(prop={'family':'Calibri','weight':'bold','size':22},frameon=False)
plt.xticks(x,pro_list,size=14,fontproperties='Calibri',weight='bold')
plt.yticks(size=14,fontproperties='Calibri',weight='bold')#设置大小及加粗
plt.tight_layout()
plt.savefig('coefficient of variation.png', dpi=300)
'''
'''
plt.close('all')
fig, ax1 = plt.subplots(figsize=(6,4))
ax1.spines['top'].set_visible(False)
color = 'tab:red'
ax1.set_xlabel('Length(um)',fontsize=20,fontproperties='Calibri',weight='bold')
ax1.set_ylabel('Cable length', color=color,fontsize=20,fontproperties='Calibri',weight='bold')
ax1.plot(x_as, np.mean(sholl_data[1,:,:],0), color=color,label='cable_length',linewidth=3)
ax1.tick_params(axis='y', labelcolor=color,labelsize=14)
ax1.tick_params(axis='x', labelsize=14)
x1_label = ax1.get_xticklabels() 
[x1_label_temp.set_fontname('Calibri') for x1_label_temp in x1_label]
y1_label = ax1.get_yticklabels() 
[y1_label_temp.set_fontname('Calibri') for y1_label_temp in y1_label]


ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.spines['top'].set_visible(False)
color = 'tab:blue'
ax2.plot(x_as, np.mean(sholl_data[0,:,:],0), color=color,label='bouton',linewidth=3)
ax2.set_ylabel('Number',fontsize=20,fontproperties='Calibri',weight='bold')
ax2.tick_params(axis='y',labelsize=14)
color = 'tab:green'
ax2.plot(x_as, np.mean(sholl_data[2,:,:],0), color=color,label='branch_points',linewidth=3)
color = 'tab:orange'
ax2.plot(x_as, np.mean(sholl_data[3,:,:],0), color=color,label='boutondensity',linewidth=3)
x1_label = ax2.get_xticklabels() 
[x1_label_temp.set_fontname('Calibri') for x1_label_temp in x1_label]
y1_label = ax2.get_yticklabels() 
[y1_label_temp.set_fontname('Calibri') for y1_label_temp in y1_label]
'''

# ## 相关性矩阵
# from scipy.stats import pearsonr
# c1=np.zeros((15,15))
# c2=np.zeros((15,15))
# for i in range(15):
#     for j in range(15):
#         c1[i,j],c2[i,j]=pearsonr(pro_map_bouton[i],pro_map_bouton[j])

# import seaborn as sns
# plt.close('all')
# plt.figure(figsize=(4,4))
# #
# pic=sns.heatmap(data=c1,cbar=True,yticklabels=False,xticklabels=False,square=True,
#                 annot=False, fmt=".0f",linewidths=.5,cmap=plt.get_cmap('OrRd'),
#                 cbar_kws={'shrink':0.8,'label':"Pearson correlation coefficient"},
#                 annot_kws={'fontsize':11})
# cbar = pic.collections[0].colorbar
# # here set the labelsize by 20
# cbar.ax.tick_params(labelsize=12)


import seaborn as sns
## 投射矩阵
pro_list=np.array(pro_list)
t=np.argsort(-np.mean(total_map,0))
pro_list=pro_list[t]
pro_list=pro_list[0:-6]
pro_map_bouton=pro_map_bouton[:,t]
pro_map_bouton=pro_map_bouton[:,0:-6]
t=[0,1,2,5,6,3,4]
pro_list[0:7]=pro_list[t]
pro_map_bouton[:,0:7]=pro_map_bouton[:,t]
# set_list=['SSp-bfd',='SSp-n','SSs','VISa','VISrl']
# t=[pro_list.index(x) for x in set_list]
# pro_map=pro_map[:,t]

sns.set(font_scale = 1.2)
plt.close('all')
plt.figure(figsize=(8,6))
#
pic=sns.heatmap(data=pro_map_bouton,cbar=True,yticklabels=False,xticklabels=pro_list,square=True,
                annot=True, fmt=".0f",linewidths=.5,cmap=plt.get_cmap('OrRd'),
                cbar_kws={'shrink':0.4,'label':"Projection intensity(%)"},
                annot_kws={'fontsize':11})
cbar = pic.collections[0].colorbar
# here set the labelsize by 20
cbar.ax.tick_params(labelsize=12)

pic.set_xticklabels(pro_list,fontsize=12,rotation=90)
pic.set_ylabel("Neurons",fontsize=16)
pic.set_xlabel("Projection regions (boutons>100)",fontsize=16)
plt.tight_layout()
# plt.savefig('similar_neurons.png', dpi=300)


for root,dirs,files in os.walk(path,topdown=True):
    file_list=[x.split('.')[0] for x in files]
color_list=["#FF0000","#00FF00","#0000FF","#FFFF00","#00FFFF","#FF00FF",
            "#FF8000","#00FF80","#8000FF","#80FF00","#0080FF","#FF0080",
            "#800000","#008000","#000080"] # ,"#808000","#008080","#800080","#ff8080","#80ff80","#8080ff","#db5f56","#39f710","#e27215","#51cb82"
file_color=dict()
for i in range(len(file_list)):
    file_color[i]=color_list[i]

count=0
for i in range(len(neuron_list)):
    pro_map_bouton[i]=count
    count+=1

sns.set(font_scale = 1.2)
plt.close('all')
plt.figure(figsize=(8,6))
#
pic=sns.heatmap(data=pro_map_bouton,cbar=True,yticklabels=False,xticklabels=pro_list,square=True,
                annot=False, fmt=".0f",linewidths=.5,cmap=color_list,
                cbar_kws={'shrink':0.4,'label':"Projection intensity(%)"}
                )
cbar = pic.collections[0].colorbar
# here set the labelsize by 20
cbar.ax.tick_params(labelsize=12)

pic.set_xticklabels(pro_list,fontsize=12,rotation=90)
pic.set_ylabel("Neurons",fontsize=16)
pic.set_xlabel("Projection regions (boutons>100)",fontsize=16)
plt.tight_layout()
plt.savefig('neuron_legend.png', dpi=300)