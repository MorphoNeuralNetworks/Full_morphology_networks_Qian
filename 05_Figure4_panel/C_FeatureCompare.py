import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

methods=['all','axon','dendrite']
# methods_color={'all':'#FFB6C1','axon':'#6495ED','dendrite':'#90EE90'}
networks=['b','bde','bda']
colorlist={('b','all'):'#DC143C',('b','axon'):'#FFB6C1',('b','dendrite'):'#DB7093',
           ('bda','all'):'#000080',('bda','axon'):'#6495ED',('bda','dendrite'):'#1E90FF',
           ('bde','all'):'#006400',('bde','axon'):'#3CB371',('bde','dendrite'):'#00FF7F'}
# methods_style={'all':'+','axon':'o','dendrite':'s'}

feature_dict_bouton={}
cc=np.load('..\\Data\\\Perturbation_Data\\CostStorageRouting_bouton.npy',allow_pickle=True)
for x in cc:
    t=str(x[0])
    t=t.replace('_bouton','')
    x[1]=float(x[1])/10000
    c=x[1:].astype(np.float64)
    feature_dict_bouton[t]=c.tolist()
feature_dict_boutondensity_each={}
cc=np.load('..\\Data\\\Perturbation_Data\\CostStorageRouting_boutondensity_each.npy',allow_pickle=True)
for x in cc:
    t=str(x[0])
    t=t.replace('_boutondensity_each','')
    t=t.replace('normal_boutondensity','normal')
    x[1]=float(x[1])/10000
    c=x[1:].astype(np.float64)
    feature_dict_boutondensity_each[t]=c.tolist()

## perturbation types
data_list_PruneDelete_RE=[]
data_list_PruneDelete_SC=[]
data_list_Scale_RE=[]
data_list_Scale_SC=[]
for network in networks[0:2]:
    feature_dict={}
    if network=='b':
        feature_dict=feature_dict_bouton
    elif network=='bde':
        feature_dict=feature_dict_boutondensity_each
    for method in methods:
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
        
        data_list_Scale_RE.append([y1_t1[0],y1_t1[5],y1_t1[-1],'scale',method])
        data_list_PruneDelete_RE.append([y1_t2[0],y1_t2[-1],'prune',method])
        if method=='all':
            data_list_PruneDelete_RE.append([y1_t3[0],y1_t3[-1],'delete',method])

        data_list_Scale_SC.append([y2_t1[0],y2_t1[5],y2_t1[-1],'scale',method])
        data_list_PruneDelete_SC.append([y2_t2[0],y2_t2[-1],'prune',method])
        if method=='all':
            data_list_PruneDelete_SC.append([y2_t3[0],y2_t3[-1],'delete',method])

## Prune Delete Routing Efficiency
plt.close("all")
fig,ax=plt.subplots(figsize=(8,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
bar_width=0.15
x=np.arange(0,2)
plt.bar(x+bar_width*0, [data_list_PruneDelete_RE[0][1],data_list_PruneDelete_RE[4][1]], bar_width,label="Non-Perturbed",alpha=0.7,color=["#1f77b4"])
plt.bar(x+bar_width*1, [data_list_PruneDelete_RE[0][0],data_list_PruneDelete_RE[4][0]], bar_width,label="Prune:0.5 All",alpha=0.7,color=["#2ca02c"])
plt.bar(x+bar_width*2, [data_list_PruneDelete_RE[2][0],data_list_PruneDelete_RE[6][0]], bar_width,label="Prune:0.5 Axon",alpha=0.7,color=["#006400"])
plt.bar(x+bar_width*3, [data_list_PruneDelete_RE[3][0],data_list_PruneDelete_RE[7][0]], bar_width,label="Prune:0.5 Dendrite",alpha=0.7,color=["#8FBC8F"])
plt.bar(x+bar_width*4, [data_list_PruneDelete_RE[1][0],data_list_PruneDelete_RE[5][0]], bar_width,label="Delete:0.5",alpha=0.7,color=["#9467bd"])

plt.legend(prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
plt.xticks([bar_width*1.5,1+bar_width*1.5],['Predicted','Uniform'],size=22,fontproperties='Calibri',weight='bold')
plt.yticks(size=14,fontproperties='Calibri',weight='bold')
plt.ylabel('Routing efficiency/Cost',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('PruneDelete_RE_C.pdf', dpi=300)


## Prune Delete Storage Capacity
plt.close("all")
fig,ax=plt.subplots(figsize=(8,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
bar_width=0.15
x=np.arange(0,2)
plt.bar(x+bar_width*0, [data_list_PruneDelete_SC[0][1],data_list_PruneDelete_SC[4][1]], bar_width,label="Non-Perturbed",alpha=0.7,color=["#1f77b4"])
plt.bar(x+bar_width*1, [data_list_PruneDelete_SC[0][0],data_list_PruneDelete_SC[4][0]], bar_width,label="Prune:0.5 All",alpha=0.7,color=["#2ca02c"])
plt.bar(x+bar_width*2, [data_list_PruneDelete_SC[2][0],data_list_PruneDelete_SC[6][0]], bar_width,label="Prune:0.5 Axon",alpha=0.7,color=["#006400"])
plt.bar(x+bar_width*3, [data_list_PruneDelete_SC[3][0],data_list_PruneDelete_SC[7][0]], bar_width,label="Prune:0.5 Dendrite",alpha=0.7,color=["#8FBC8F"])
plt.bar(x+bar_width*4, [data_list_PruneDelete_SC[1][0],data_list_PruneDelete_SC[5][0]], bar_width,label="Delete:0.5",alpha=0.7,color=["#9467bd"])

plt.legend(prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
plt.xticks([bar_width*1.5,1+bar_width*1.5],['Predicted','Uniform'],size=22,fontproperties='Calibri',weight='bold')
plt.yticks(size=14,fontproperties='Calibri',weight='bold')
plt.ylabel('Storage capacity/Cost',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('PruneDelete_SC_C.pdf', dpi=300)


## Scale Routing Efficiency
plt.close("all")
fig,ax=plt.subplots(figsize=(8,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
bar_width=0.15
x=np.arange(0,2)
plt.bar(x, [data_list_Scale_RE[0][1],data_list_Scale_RE[3][1]], bar_width,label="Non-Perturbed",alpha=0.7,color=["#1f77b4"])
plt.bar(x+bar_width*1, [data_list_Scale_RE[0][0],data_list_Scale_RE[3][0]], bar_width,label="Scale:0.5 All",alpha=0.7,color=["#d62728"])
plt.bar(x+bar_width*2, [data_list_Scale_RE[1][0],data_list_Scale_RE[4][0]], bar_width,label="Scale:0.5 Axon",alpha=0.7,color=["#FFB6C1"])
plt.bar(x+bar_width*3, [data_list_Scale_RE[2][0],data_list_Scale_RE[5][0]], bar_width,label="Scale:0.5 Dendrite",alpha=0.7,color=["#FF69B4"])

plt.legend(prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
plt.xticks([bar_width*1.5,1+bar_width*1.5],['Predicted','Uniform'],size=22,fontproperties='Calibri',weight='bold')
plt.yticks(size=14,fontproperties='Calibri',weight='bold')
plt.ylabel('Routing efficiency/Cost',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('Scale_RE_C.pdf', dpi=300)


## Scale Storage Capacity
plt.close("all")
fig,ax=plt.subplots(figsize=(8,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
bar_width=0.15
x=np.arange(0,2)
plt.bar(x, [data_list_Scale_SC[0][1],data_list_Scale_SC[3][1]], bar_width,label="Non-Perturbed",alpha=0.7,color=["#1f77b4"])
plt.bar(x+bar_width*1, [data_list_Scale_SC[0][0],data_list_Scale_SC[3][0]], bar_width,label="Scale:0.5 All",alpha=0.7,color=["#d62728"])
plt.bar(x+bar_width*2, [data_list_Scale_SC[1][0],data_list_Scale_SC[4][0]], bar_width,label="Scale:0.5 Axon",alpha=0.7,color=["#FFB6C1"])
plt.bar(x+bar_width*3, [data_list_Scale_SC[2][0],data_list_Scale_SC[5][0]], bar_width,label="Scale:0.5 Dendrite",alpha=0.7,color=["#FF69B4"])

plt.legend(prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
plt.xticks([bar_width*1.5,1+bar_width*1.5],['Predicted','Uniform'],size=22,fontproperties='Calibri',weight='bold')
plt.yticks(size=14,fontproperties='Calibri',weight='bold')
plt.ylabel('Storage capacity/Cost',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('Scale_SC_C.pdf', dpi=300)