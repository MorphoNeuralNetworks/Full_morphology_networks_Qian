import matplotlib.pyplot as plt 
import numpy as np
from scipy.stats import ttest_rel,ttest_ind,levene,ks_2samp

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
cell_type={key:soma_info[key][0] for key in soma_info.keys()}
cell_count=dict()
for key in cell_type:
    t=cell_type[key]
    if t not in cell_count:
        cell_count[t]=1
    else:
        cell_count[t]+=1

## plot
sholl_result=np.load('../Data/Temp_Data/sholl_result.npy', allow_pickle=True).item()
sholl_result_density=np.load('../Data/Temp_Data/sholl_result_density_each.npy', allow_pickle=True).item()
for name in ['VPM','SSp-m']: # set cell type. can use cell_count.keys():
    maxlen=0
    count=0
    if cell_count[name]<78: # set min number 
        continue
    for key in cell_type:
        if cell_type[key]==name:
            if len(sholl_result[key][0])>maxlen:
                maxlen=len(sholl_result[key][0])
            if len(sholl_result_density[key])>maxlen:
                maxlen=len(sholl_result_density[key])
            count+=1
    sholl_data=np.zeros((4,count,maxlen))
    
    count=0
    for key in cell_type:
        if cell_type[key]==name:
            t=len(sholl_result[key][0])
            sholl_data[0:3,count,0:t]=sholl_result[key]
            t=len(sholl_result_density[key])
            sholl_data[3,count,0:t]=sholl_result_density[key]
            count+=1
    
    x_as=[i*100 for i in range(1,maxlen+1)]
    
    plt.close('all')
    fig, ax1 = plt.subplots(figsize=(7.5,4))
    ax1.spines['top'].set_visible(False)
    color = 'tab:red'
    ax1.set_xlabel('Length(um)',fontsize=20,fontproperties='Calibri',weight='bold')
    ax1.set_ylabel('Cable length', color=color,fontsize=20,fontproperties='Calibri',weight='bold')
    ax1.plot(x_as, np.mean(sholl_data[1,:,:],0), color=color,label='cable_length',linewidth=3)
    plt.fill_between(x_as, np.mean(sholl_data[1,:,:],0)-np.std(sholl_data[1,:,:],0)/np.sqrt(len(sholl_data)), np.mean(sholl_data[1,:,:],0)+np.std(sholl_data[1,:,:],0)/np.sqrt(len(sholl_data)), facecolor=color, alpha=0.3)
    ax1.tick_params(axis='y', labelcolor=color,labelsize=14)
    ax1.tick_params(axis='x', labelsize=14)
    ax1.set_ylim([min(np.mean(sholl_data[1,:,:],0)-100),max(np.mean(sholl_data[1,:,:],0)+100)])
    x1_label = ax1.get_xticklabels() 
    [x1_label_temp.set_fontname('Calibri') for x1_label_temp in x1_label]
    y1_label = ax1.get_yticklabels() 
    [y1_label_temp.set_fontname('Calibri') for y1_label_temp in y1_label]

    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.spines['top'].set_visible(False)
    color = 'tab:blue'
    ax2.plot(x_as, np.mean(sholl_data[0,:,:],0), color=color,label='Predicted bouton',linewidth=3)
    plt.fill_between(x_as, np.mean(sholl_data[0,:,:],0)-np.std(sholl_data[0,:,:],0)/np.sqrt(len(sholl_data)), np.mean(sholl_data[0,:,:],0)+np.std(sholl_data[0,:,:],0)/np.sqrt(len(sholl_data)), facecolor=color, alpha=0.3)
    ax2.set_ylabel('Number',fontsize=20,fontproperties='Calibri',weight='bold')
    ax2.tick_params(axis='y',labelsize=14)
    color = 'tab:green'
    ax2.plot(x_as, np.mean(sholl_data[2,:,:],0), color=color,label='Branch points',linewidth=3)
    plt.fill_between(x_as, np.mean(sholl_data[2,:,:],0)-np.std(sholl_data[2,:,:],0)/np.sqrt(len(sholl_data)), np.mean(sholl_data[2,:,:],0)+np.std(sholl_data[2,:,:],0)/np.sqrt(len(sholl_data)), facecolor=color, alpha=0.3)
    color = 'tab:orange'
    ax2.plot(x_as, np.mean(sholl_data[3,:,:],0), color=color,label='Uniform bouton',linewidth=3)
    plt.fill_between(x_as, np.mean(sholl_data[3,:,:],0)-np.std(sholl_data[3,:,:],0)/np.sqrt(len(sholl_data)), np.mean(sholl_data[3,:,:],0)+np.std(sholl_data[3,:,:],0)/np.sqrt(len(sholl_data)), facecolor=color, alpha=0.3)
    ax2.set_ylim([min(np.mean(sholl_data[0,:,:],0)-8),max(np.mean(sholl_data[0,:,:],0)+8)])
    x1_label = ax2.get_xticklabels() 
    [x1_label_temp.set_fontname('Calibri') for x1_label_temp in x1_label]
    y1_label = ax2.get_yticklabels() 
    [y1_label_temp.set_fontname('Calibri') for y1_label_temp in y1_label]
    
    shade_list=[]
    for i in range(np.shape(sholl_data)[2]):
        ## ttest_ind
        # (_,tt)=levene(sholl_data[0,:,i],sholl_data[3,:,i])
        # if tt<0.1:
        #     (_,t)=ttest_ind(sholl_data[0,:,i],sholl_data[3,:,i],equal_var=False)
        # else:
        #     (_,t)=ttest_ind(sholl_data[0,:,i],sholl_data[3,:,i])
        
        ## test_rel
        (_,t)=ttest_rel(sholl_data[0,:,i],sholl_data[3,:,i])
        
        ## ks_2samp
        # (_,t)=ks_2samp(sholl_data[0,:,i],sholl_data[3,:,i])
        if t<0.001:
            shade_list.append(i*100+50)
    ax1.bar(shade_list,[np.max(sholl_data[1,:,:])]*len(shade_list),width=100,align="center",color=['#A9A9A9'],alpha=0.7)
    ax2.legend(prop={'family':'Calibri','weight':'bold','size':18},frameon=False)
    fig.tight_layout()
    plt.show()
    # plt.savefig(name+'_all.pdf', dpi=300, transparent=True)
