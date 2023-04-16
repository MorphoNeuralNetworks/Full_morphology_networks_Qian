import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
cell_type={key:soma_info[key][0] for key in soma_info.keys()}
for key in cell_type.keys():
    if "SSp-" in cell_type[key]:
        cell_type[key]="SSp"
cell_count={}
for key in cell_type.keys():
    if cell_type[key] not in cell_count.keys():
        cell_count[cell_type[key]]=1
    else:
        cell_count[cell_type[key]]=cell_count[cell_type[key]]+1

select_list=["all","VPM","CP","SSp","LGd","VPL","MOp","SSs","MOs"] #
for select_type in select_list[1:2]:
    print(select_type)
    plt.close("all")
    ##  x: TMD bouton distance, y: default TMD distance
    fig,ax=plt.subplots(figsize= (5.5, 5))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    neuron_list=np.load("../Data/Temp_Data/TMD_Bouton_list.npy",allow_pickle=True)
    neuron_type=np.array([cell_type[x] for x in neuron_list])
    x_l=np.load("../Data/Temp_Data/TMD_Bouton_list.npy",allow_pickle=True)
    x_dict={str(x_l[i]):i for i in range(len(x_l))}
    y_l=np.load("../Data/Temp_Data/TMD_default_list.npy",allow_pickle=True)
    y_dict={str(y_l[i]):i for i in range(len(y_l))}
    
    x_matrix=np.load("../Data/Temp_Data/TMD_Bouton.npy",allow_pickle=True)
    y_matrix=np.load("../Data/Temp_Data/TMD_default.npy",allow_pickle=True)
    
    ## keep the two matrices aligned
    if x_l.tolist()!=y_l.tolist():
        # print("neuron order not same")
        y_select=[y_dict[x] for x in x_l]
        y_select=np.array(y_select)
        y_l=y_l[y_select]
        y_matrix=y_matrix[y_select,:]
        y_matrix=y_matrix[:,y_select]
    
    ## select cell type
    if select_type!="all":
        t=np.where(neuron_type==select_type)[0]
        neuron_list=neuron_list[t]
        x_matrix=x_matrix[t,:]
        y_matrix=y_matrix[t,:]
        x_matrix=x_matrix[:,t]
        y_matrix=y_matrix[:,t]
        x_l=x_l[t]
        y_l=y_l[t]
    
    data=[]
    for i in range(len(neuron_list)):
        for j in range(i+1,len(neuron_list)):
            if x_matrix[i,j]>100000 or y_matrix[i,j]>100000: # skip meaningless value
                continue
            data.append([x_matrix[i,j],y_matrix[i,j]])
    data=np.array(data)
    plt.scatter(data[:,0],data[:,1],s=1,c='#1f77b4',alpha=1,linewidth=0) 
    
    ### random bouton
    neuron_list=np.load("../Data/Temp_Data/TMD_bouton_random_list.npy",allow_pickle=True)
    neuron_type=np.array([cell_type[x] for x in neuron_list])
    x_l=np.load("../Data/Temp_Data/TMD_bouton_random_list.npy",allow_pickle=True)
    x_dict={str(x_l[i]):i for i in range(len(x_l))}
    y_l=np.load("../Data/Temp_Data/TMD_default_list.npy",allow_pickle=True)
    y_dict={str(y_l[i]):i for i in range(len(y_l))}
    
    x_matrix=np.load("../Data/Temp_Data/TMD_bouton_random.npy",allow_pickle=True)
    y_matrix=np.load("../Data/Temp_Data/TMD_default.npy",allow_pickle=True)
    
    ## keep the two matrices aligned
    if x_l.tolist()!=y_l.tolist():
        # print("neuron order not same")
        y_select=[y_dict[x] for x in x_l]
        y_select=np.array(y_select)
        y_l=y_l[y_select]
        y_matrix=y_matrix[y_select,:]
        y_matrix=y_matrix[:,y_select]
    
    ## select cell type
    if select_type!="all":
        t=np.where(neuron_type==select_type)[0]
        neuron_list=neuron_list[t]
        x_matrix=x_matrix[t,:]
        y_matrix=y_matrix[t,:]
        x_matrix=x_matrix[:,t]
        y_matrix=y_matrix[:,t]
        x_l=x_l[t]
        y_l=y_l[t]

    data_random=[]
    for i in range(len(neuron_list)):
        for j in range(i+1,len(neuron_list)):
            if x_matrix[i,j]>100000 or y_matrix[i,j]>100000: # skip meaningless value
                continue
            data_random.append([x_matrix[i,j],y_matrix[i,j]])
    data_random=np.array(data_random)
    plt.scatter(data_random[:,0],data_random[:,1],s=1,c="#d62728",alpha=1,linewidth=0)
    
    # cruve fitting
    z1 = np.polyfit(data[:,0],data[:,1],1)
    p1 = np.poly1d(z1)
    fit_y=p1(data[:,0])
    plt.plot([np.min(data[:,0]),np.max(data[:,0])],[np.min(fit_y),np.max(fit_y)],c='#1f77b4',linewidth=3,label="Predicted")
    
    z1 = np.polyfit(data_random[:,0],data_random[:,1],1)
    p1 = np.poly1d(z1)
    fit_y=p1(data_random[:,0])
    plt.plot([np.min(data_random[:,0]),np.max(data_random[:,0])],[np.min(fit_y),np.max(fit_y)],c="#d62728",linewidth=3,label="Random")
    
    ## statistical tests
    p,t = pearsonr(data[:,0], data[:,1])
    print("Predicted pearsonr="+str(p)+'\t p='+str(t))
    p,t = pearsonr(data_random[:,0], data_random[:,1])
    print("Random pearsonr="+str(p)+'\t p='+str(t))

    plt.xlabel("TMD bouton distance")
    plt.ylabel("default TMD distance")
    plt.xticks(size=20,fontproperties='Calibri',weight='bold')
    plt.yticks(size=20,fontproperties='Calibri',weight='bold')#设置大小及加粗
    # ax.set_xticklabels([])
    # ax.set_yticklabels([])
    # plt.legend(prop={'family':'Calibri','weight':'bold','size':22},frameon=False)
    plt.tight_layout()
    # plt.savefig("real_"+select_type+'.jpg',dpi=300)