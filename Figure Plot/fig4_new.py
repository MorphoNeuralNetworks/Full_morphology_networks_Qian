import os
import numpy as np
import matplotlib.pyplot as plt

methods=['all','axon','dendrite']
# methods_color={'all':'#FFB6C1','axon':'#6495ED','dendrite':'#90EE90'}

networks=['b','bde','bda']
colorlist={('b','all'):'#DC143C',('b','axon'):'#FFB6C1',('b','dendrite'):'#DB7093',
           ('bde','all'):'#006400',('bde','axon'):'#3CB371',('bde','dendrite'):'#00FF7F'}
#('bda','all'):'#000080',('bda','axon'):'#6495ED',('bda','dendrite'):'#1E90FF',

# methods_style={'all':'+','axon':'o','dendrite':'s'}
## 查看每种参数下weight的分布
feature_dict_bouton={}
cc=np.load('..\\BrainNetwork_Pertubation\\Temp_Data\\CostStorageRouting_bouton.npy',allow_pickle=True)
for x in cc:
    t=str(x[0])
    t=t.replace('_bouton','')
    x[1]=float(x[1])/10000
    c=x[1:].astype(np.float64)
    feature_dict_bouton[t]=c.tolist()

# feature_dict_boutondensity_all={}
# cc=np.load('..\\BrainNetwork_Pertubation_density_all\\Temp_Data\\CostStorageRouting_boutondensity_all.npy',allow_pickle=True)
# for x in cc:
#     t=str(x[0])
#     t=t.replace('_boutondensity_all','')
#     t=t.replace('normal_boutondensity','normal')
#     x[1]=float(x[1])/10000
#     c=x[1:].astype(np.float64)
#     feature_dict_boutondensity_all[t]=c.tolist()
    
feature_dict_boutondensity_each={}
cc=np.load('..\\BrainNetwork_Pertubation_density_each\\Temp_Data\\CostStorageRouting_boutondensity_each.npy',allow_pickle=True)
for x in cc:
    t=str(x[0])
    t=t.replace('_boutondensity_each','')
    t=t.replace('normal_boutondensity','normal')
    x[1]=float(x[1])/10000
    c=x[1:].astype(np.float64)
    feature_dict_boutondensity_each[t]=c.tolist()

'''
## perturbation types
plt.close('all')
fig, ax1 = plt.subplots(figsize=(18,6))
ax1.set_xlabel('Perturbation',fontsize=14)
ax1.set_ylabel('Routing efficiency/Cost(—)',fontsize=14)
ax1.tick_params(axis='y',labelsize=12)
ax1.tick_params(axis='x', labelsize=12)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Storage capacity/Cost(...)',fontsize=14)
ax2.tick_params(axis='y',labelsize=12)
for network in networks[0:2]:
    feature_dict={}
    if network=='b':
        feature_dict=feature_dict_bouton
    elif network=='bde':
        feature_dict=feature_dict_boutondensity_each
    # elif network=='bda':
    #     feature_dict=feature_dict_boutondensity_all
    for method in methods[1:2]:
        y1_t1=[]
        y2_t1=[]
        x_t=[]
        for x in range(5,10):
            name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
            y1_t1.append(feature_dict[name][2])
            y2_t1.append(feature_dict[name][1])  
            x_t.append(x/10)
        y1_t1.append(feature_dict['normal'][2])
        y2_t1.append(feature_dict['normal'][1])
        x_t.append(1)
         
        y1_t2=[]
        y2_t2=[]
        x_t2=[]
        for x in range(5,10):
            name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
            y1_t2.append(feature_dict[name][2])
            y2_t2.append(feature_dict[name][1])  
            x_t2.append(x/10)
        y1_t2.append(feature_dict['normal'][2])
        y2_t2.append(feature_dict['normal'][1])
        x_t2.append(1)       
        
        y1_t3=[]
        y2_t3=[]
        for x in range(5,10):
            name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
            y1_t3.append(feature_dict[name][2])
            y2_t3.append(feature_dict[name][1])  
        y1_t3.append(feature_dict['normal'][2])
        y2_t3.append(feature_dict['normal'][1])
        
        ax1.plot(x_t, y1_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle='-',marker='^',markersize=10,alpha=0.7)
        ax1.plot(x_t2, y1_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle='-',marker='s',markersize=10,alpha=0.7)
        if method=='all':
            ax1.plot(x_t2, y1_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle='-',marker='*',markersize=10,alpha=0.7)

        ax2.plot(x_t, y2_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle=':',marker='^',markersize=10,alpha=0.7)
        ax2.plot(x_t2, y2_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle=':',marker='s',markersize=10,alpha=0.7)
        if method=='all':
            ax2.plot(x_t2, y2_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle=':',marker='*',markersize=10,alpha=0.7)
        
ax2.legend(fontsize=10)
plt.title('BoutonNetwork',fontsize=16)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()
'''

## perturbation types
plt.close('all')
fig, ax1 = plt.subplots(figsize=(18,10))
ax1.set_xlabel('Perturbation',fontsize=14)
ax1.set_ylabel('Routing efficiency/Cost(—)',fontsize=14)
ax1.tick_params(axis='y',labelsize=12)
ax1.tick_params(axis='x', labelsize=12)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Storage capacity/Cost(...)',fontsize=14)
ax2.tick_params(axis='y',labelsize=12)
for network in networks[0:2]:
    feature_dict={}
    if network=='b':
        feature_dict=feature_dict_bouton
    elif network=='bde':
        feature_dict=feature_dict_boutondensity_each
    for method in methods[2:3]:
        y1_t1=[]
        y2_t1=[]
        x_t=[]
        for x in range(5,10):
            name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
            y1_t1.append(feature_dict[name][2]/feature_dict[name][0])
            y2_t1.append(feature_dict[name][1]/feature_dict[name][0])  
            x_t.append(x/10)
        y1_t1.append(feature_dict['normal'][2]/feature_dict['normal'][0])
        y2_t1.append(feature_dict['normal'][1]/feature_dict['normal'][0])
        x_t.append(1)

         
        y1_t2=[]
        y2_t2=[]
        x_t2=[]
        for x in range(5,10):
            name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
            y1_t2.append(feature_dict[name][2]/feature_dict[name][0])
            y2_t2.append(feature_dict[name][1]/feature_dict[name][0])  
            x_t2.append(x/10)
        y1_t2.append(feature_dict['normal'][2]/feature_dict['normal'][0])
        y2_t2.append(feature_dict['normal'][1]/feature_dict['normal'][0])
        x_t2.append(1)       
        
        y1_t3=[]
        y2_t3=[]
        for x in range(5,10):
            name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
            y1_t3.append(feature_dict[name][2]/feature_dict[name][0])
            y2_t3.append(feature_dict[name][1]/feature_dict[name][0])  
        y1_t3.append(feature_dict['normal'][2]/feature_dict['normal'][0])
        y2_t3.append(feature_dict['normal'][1]/feature_dict['normal'][0])
        
        ax1.plot(x_t, y1_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle='-',marker='^',markersize=10,alpha=0.7)
        ax1.plot(x_t2, y1_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle='-',marker='s',markersize=10,alpha=0.7)
        if method=='all':
            ax1.plot(x_t2, y1_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle='-',marker='*',markersize=10,alpha=0.7)

        ax2.plot(x_t, y2_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle=':',marker='^',markersize=10,alpha=0.7)
        ax2.plot(x_t2, y2_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle=':',marker='s',markersize=10,alpha=0.7)
        if method=='all':
            ax2.plot(x_t2, y2_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle=':',marker='*',markersize=10,alpha=0.7)
        
ax1.legend(fontsize=10)
# plt.title('BoutonNetwork',fontsize=16)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()
'''
'''

'''
plt.close('all')
fig, ax1 = plt.subplots(figsize=(18,6))
ax1.set_xlabel('Perturbation',fontsize=14)
ax1.set_ylabel('Routing efficiency/Cost(—)',fontsize=14)
ax1.tick_params(axis='y',labelsize=12)
ax1.tick_params(axis='x', labelsize=12)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Storage capacity/Cost(...)',fontsize=14)
ax2.tick_params(axis='y',labelsize=12)
for network in networks:
    feature_dict={}
    if network=='b':
        feature_dict=feature_dict_bouton
    elif network=='bde':
        feature_dict=feature_dict_boutondensity_each
    elif network=='bda':
        feature_dict=feature_dict_boutondensity_all
    for method in methods:
        y1_t1=[]
        y2_t1=[]
        x_t=[]
        for x in range(5,10):
            name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
            y1_t1.append(feature_dict[name][2]/feature_dict[name][0])
            y2_t1.append(feature_dict[name][1]/feature_dict[name][0])  
            x_t.append(x/10)
        y1_t1.append(feature_dict['normal'][2]/feature_dict[name][0])
        y2_t1.append(feature_dict['normal'][1]/feature_dict[name][0])
        x_t.append(1)
        for x in range(12,22,2):
            name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
            y1_t1.append(feature_dict[name][2]/feature_dict[name][0])
            y2_t1.append(feature_dict[name][1]/feature_dict[name][0])
            x_t.append(x/10)
         
        y1_t2=[]
        y2_t2=[]
        x_t2=[]
        for x in range(5,10):
            name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
            y1_t2.append(feature_dict[name][2]/feature_dict[name][0])
            y2_t2.append(feature_dict[name][1]/feature_dict[name][0])  
            x_t2.append(x/10)
        y1_t2.append(feature_dict['normal'][2]/feature_dict['normal'][0])
        y2_t2.append(feature_dict['normal'][1]/feature_dict['normal'][0])
        x_t2.append(1)       
        
        y1_t3=[]
        y2_t3=[]
        for x in range(5,10):
            name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
            y1_t3.append(feature_dict[name][2]/feature_dict[name][0])
            y2_t3.append(feature_dict[name][1]/feature_dict[name][0])  
        y1_t3.append(feature_dict['normal'][2]/feature_dict['normal'][0])
        y2_t3.append(feature_dict['normal'][1]/feature_dict['normal'][0])
        
        ax1.plot(x_t, y1_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle='-',marker='^',markersize=10,alpha=0.7)
        ax1.plot(x_t2, y1_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle='-',marker='s',markersize=10,alpha=0.7)
        if method=='all':
            ax1.plot(x_t2, y1_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle='-',marker='*',markersize=10,alpha=0.7)

        ax2.plot(x_t, y2_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle=':',marker='^',markersize=10,alpha=0.7)
        ax2.plot(x_t2, y2_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle=':',marker='s',markersize=10,alpha=0.7)
        if method=='all':
            ax2.plot(x_t2, y2_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle=':',marker='*',markersize=10,alpha=0.7)
        
ax2.legend(fontsize=10)
# plt.title(name,fontsize=16)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()
'''