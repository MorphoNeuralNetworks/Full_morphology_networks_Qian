'''
Select some neurons to generate connection heatmap
'''
import numpy as np
import os,csv

soma_info=np.load("..\Data\Other_Infomation\Soma_info.npy",allow_pickle=True).item()
cell_type={key:soma_info[key][0] for key in soma_info.keys()}
neuron_list=[key for key in soma_info.keys()]
for key in cell_type.keys():
    if "SSp-" in cell_type[key]:
        cell_type[key]="SSp"

## connection Matrix
connnect_map=np.load('../Data/Network_Data/bouton_connection.npy',allow_pickle=True)
connnect_map=connnect_map[:,[0,1,3]]

pre_dic=dict()
pre_list=list(set(connnect_map[:,0].tolist()))
count=0
for x in pre_list:
    pre_dic[x]=count
    count+=1
count=0
post_dic=dict()
post_list=list(set(connnect_map[:,1].tolist()))
for x in post_list:
    post_dic[x]=count
    count+=1
mark=np.zeros((len(pre_dic.keys()),len(post_dic.keys())))
data=np.zeros((len(pre_dic.keys()),len(post_dic.keys())))
pre_list=np.array(pre_list)
post_list=np.array(post_list)
for x in connnect_map:
    i=pre_dic[str(x[0])]
    j=post_dic[str(x[1])]
    data[i,j]=np.log10(float(x[2])+1)
    mark[i,j]=1

## remove sparse rows and columns
count=0
for i in range(0,1300): # set the strp of loop
    count+=1
    if count%50==0:
        print(count)
    temp=np.sum(mark,1)
    t=np.argsort(temp)[::-1]
    data = data[t,:]
    mark = mark[t,:]
    pre_list=pre_list[t]
    # delete rows
    data=data[0:-1,:]
    mark=mark[0:-1,:]
    pre_list=pre_list[0:-1]
    
    temp=np.sum(mark,0)
    t=np.argsort(temp)[::-1]
    data = data[:,t]
    mark = mark[:,t]
    post_list=post_list[t]
    # delete columns
    data=data[:,0:-1]
    mark=mark[:,0:-1]
    post_list=post_list[0:-1]

pre_region=[cell_type[x] for x in pre_list]
post_region=[cell_type[x] for x in post_list]
pre_region=np.array(pre_region)
post_region=np.array(post_region)

t=np.argsort(pre_region)[::-1]
data=data[t,:]
pre_region=pre_region[t]

t=np.argsort(post_region)[::-1]
data=data[:,t]
post_region=post_region[t]
np.save('temp.npy',[data,pre_region,post_region])


## use filtered neuron to generate heatmap
temp=np.load('temp.npy',allow_pickle=True)
data,pre_region,post_region=temp[0],temp[1],temp[2]

# Cortex
# Thalamus VPM VPL VM VAL
# Striatum CP

## select the cell type before projection
# pre_select=['VPM','VPL','AId','MOp','MOs','SSs','SSp-ul','SSp-n','SSp-m','CP']
pre_select=["VPM","VPL",\
            "SSp","MOp","SSs","MOs","AId",\
            "CP"]
pre_dict={str(x):0 for x in set(pre_region)}
for x in pre_region: pre_dict[x]+=1

## select the cell type after projection
# post_select=['VPM','MOs','MOp','SSs','SSp-ul','SSp-un','SSp-n','SSp-m','SSp-bfd','CP']
post_select=["VPM",\
             "SSp","MOp","MOs","SSs",\
             "CP"]
post_dict={str(x):0 for x in set(post_region)}
for x in post_region: post_dict[x]+=1

color_dict=np.load("../Data/Other_Infomation/color_network.npy",allow_pickle=True).item()

t=[]
for x in pre_select:
    for i in range(0,len(pre_region)):
        if pre_region[i]==x:
            t.append(i)
data=data[t,:]
pre_region=pre_region[t]

t=[]
for x in post_select:
    for i in range(0,len(post_region)):
        if post_region[i]==x:
            t.append(i)
data=data[:,t]
post_region=post_region[t]

## set region color
row_color=[color_dict[x] for x in pre_region]
xtick=[str(post_region[0])]
for i in range(1,len(post_region)-1):
    if post_region[i-1]!=post_region[i] or post_region[i+1]!=post_region[i]:
        xtick.append(str(post_region[i]))
    else:
        xtick.append('-')
xtick.append(str(post_region[-1]))

col_color=[color_dict[x] for x in post_region]
ytick=[str(pre_region[0])]
for i in range(1,len(pre_region)-1):
    if pre_region[i-1]!=pre_region[i] or pre_region[i+1]!=pre_region[i]:
        ytick.append(str(pre_region[i]))
    else:
        ytick.append('-')
ytick.append(str(pre_region[-1]))

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
plt.close('all')
sns.clustermap(data=data,figsize=(11,11),row_cluster=False,col_cluster=False,
               xticklabels=xtick,yticklabels=ytick,cmap=plt.get_cmap('hot_r'),#OrRd
               row_colors=row_color,col_colors=col_color,square=True,
               cbar_kws={'shrink':0.4,'label':"Connection strength"})
plt.tight_layout()
# plt.savefig('temp.jpg',dpi=600)

