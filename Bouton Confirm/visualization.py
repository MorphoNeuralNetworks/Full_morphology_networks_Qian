import os
import numpy as np
import matplotlib.pyplot as plt

methods=['all','axon','dendrite']
# methods_color={'all':'#FFB6C1','axon':'#6495ED','dendrite':'#90EE90'}

networks=['b','bde']
colorlist={('b','all'):'#DC143C',('b','axon'):'#FFB6C1',('b','dendrite'):'#DB7093',
           ('bde','all'):'#006400',('bde','axon'):'#3CB371',('bde','dendrite'):'#00FF7F'}

# methods_style={'all':'+','axon':'o','dendrite':'s'}
## 查看每种参数下weight的分布
feature_dict_bouton={}
feature_dict_bouton=np.load('BoutonRatio_bouton.npy',allow_pickle=True).item()
feature_dict_bouton['normal']=feature_dict_bouton['bouton']

feature_dict_boutondensity={}
feature_dict_boutondensity=np.load('BoutonRatio_boutondensity_each.npy',allow_pickle=True).item()
feature_dict_boutondensity['normal']=feature_dict_boutondensity['boutondensity']


## perturbation types
plt.close('all')
fig, ax1 = plt.subplots(figsize=(18,10))
ax1.set_xlabel('Perturbation',fontsize=14)
ax1.tick_params(axis='y',labelsize=12)
ax1.tick_params(axis='x', labelsize=12)

for network in networks[0:2]:
    feature_dict={}
    if network=='b':
        feature_dict=feature_dict_bouton
    elif network=='bde':
        feature_dict=feature_dict_boutondensity
    for method in methods:
        y1_t1=[]
        y2_t1=[]
        y3_t1=[]
        x_t=[]
        for x in range(5,10):
            name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
            y1_t1.append(feature_dict[name][0])
            y2_t1.append(feature_dict[name][1])  
            y3_t1.append(feature_dict[name][2])
            x_t.append(x/10)
        y1_t1.append(feature_dict['normal'][0])
        y2_t1.append(feature_dict['normal'][1])
        y3_t1.append(feature_dict['normal'][2])
        x_t.append(1)
        for x in range(12,22,2):
            name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
            y1_t1.append(feature_dict[name][0])
            y2_t1.append(feature_dict[name][1])
            y3_t1.append(feature_dict[name][2])
            x_t.append(x/10)

        y1_t2=[]
        y2_t2=[]
        y3_t2=[]
        x_t2=[]
        for x in range(5,10):
            name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
            y1_t2.append(feature_dict[name][0])
            y2_t2.append(feature_dict[name][1])
            y3_t2.append(feature_dict[name][2])
            x_t2.append(x/10)
        y1_t2.append(feature_dict['normal'][0])
        y2_t2.append(feature_dict['normal'][1])
        y3_t2.append(feature_dict['normal'][2])
        x_t2.append(1)       
        
        y1_t3=[]
        y2_t3=[]
        y3_t3=[]
        for x in range(5,10):
            name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
            y1_t3.append(feature_dict[name][0])
            y2_t3.append(feature_dict[name][1])
            y3_t3.append(feature_dict[name][2])
        y1_t3.append(feature_dict['normal'][0])
        y2_t3.append(feature_dict['normal'][1])
        y3_t3.append(feature_dict['normal'][2])
        
        # ax1.set_ylabel('Connected bouton',fontsize=14)
        # # # ax1.plot(x_t, y1_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle='-',marker='^',markersize=10,alpha=0.7)
        # ax1.plot(x_t2, y1_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle='-',marker='s',markersize=10,alpha=0.7)
        # if method=='all':
        #     ax1.plot(x_t2, y1_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle='-',marker='*',markersize=10,alpha=0.7)
        
        # ax1.set_ylabel('Total bouton',fontsize=14)
        # # ax1.plot(x_t, y2_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle=':',marker='^',markersize=10,alpha=0.7)
        # ax1.plot(x_t2, y2_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle=':',marker='s',markersize=10,alpha=0.7)
        # # if method=='all':
        # #     ax1.plot(x_t2, y2_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle=':',marker='*',markersize=10,alpha=0.7)
        
        ax1.set_ylabel('Ratio',fontsize=14)
        ax1.plot(x_t, y3_t1,linewidth=2,color=colorlist[(network,method)],label=(network,method,'scale'),linestyle=':',marker='^',markersize=10,alpha=0.7)
        # ax1.plot(x_t2, y3_t2,linewidth=2,color=colorlist[(network,method)],label=(network,method,'prune'),linestyle=':',marker='s',markersize=10,alpha=0.7)
        # if method=='all':
        #     ax1.plot(x_t2, y3_t3,linewidth=2,color=colorlist[(network,method)],label=(network,method,'delete'),linestyle=':',marker='*',markersize=10,alpha=0.7)
        
ax1.legend(fontsize=10)
# plt.title('BoutonNetwork',fontsize=16)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()
'''
'''