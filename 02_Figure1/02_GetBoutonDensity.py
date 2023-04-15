'''
Curve fitting to obtain bouton density of each neuron and cell type
'''
import numpy as np

soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
cell_type={key:soma_info[key][0] for key in soma_info.keys()}
cell_count=dict()
for key in cell_type:
    t=cell_type[key]
    if t not in cell_count:
        cell_count[t]=1
    else:
        cell_count[t]+=1

## calculate the bouton density of cell type
sholl_result=np.load('../Data/Temp_Data/sholl_result.npy', allow_pickle=True).item()
sholl_result_density=np.load('../Data/Temp_Data/sholl_result_density_all.npy', allow_pickle=True).item()
best_par=dict()
for name in cell_count.keys():
    maxlen=0
    count=0
    if cell_count[name]<0:
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
    # traverse to find the optimal ratio
    bouton_result=np.mean(sholl_data[0,:,:],0)
    boutondensity=np.mean(sholl_data[3,:,:],0)
    st=round(np.mean(boutondensity)/np.mean(bouton_result),3)*10000-50000
    end=round(np.mean(boutondensity)/np.mean(bouton_result),3)*10000+10000
    record=[]
    for k in range(int(st),int(end)):
        boutondensity_new=boutondensity*k/10000
        res=bouton_result-boutondensity_new
        loss=np.sum(np.square(res))
        record.append(loss)
    # plt.plot(range(int(st),int(end)),record)
    best_par[name]=(st+record.index(min(record)))/10000
    np.save('../Data/Other_Infomation/best_density.npy',best_par)

## calculate the bouton density of neuron
count=1
for key in sholl_result.keys():
    if count%100==0:
        print(count)
    count+=1
    maxlen=max(len(sholl_result[key][0,:]),len(sholl_result_density[key]))
    sholl_data=np.zeros((2,maxlen))
    sholl_data[0,0:len(sholl_result[key][0,:])]=sholl_result[key][0,:]
    sholl_data[1,0:len(sholl_result_density[key])]=sholl_result_density[key]
    # traverse to find the optimal ratio
    bouton_result=sholl_data[0,:]
    boutondensity=sholl_data[1,:]
    st=round(np.mean(boutondensity)/np.mean(bouton_result),3)*10000-50000
    end=round(np.mean(boutondensity)/np.mean(bouton_result),3)*10000+50000
    record=[]
    for k in range(int(st),int(end)):
        boutondensity_new=boutondensity*k/10000
        res=bouton_result-boutondensity_new
        loss=np.sum(np.square(res))
        record.append(loss)
    # plt.plot(range(int(st),int(end)),record)
    best_par[key]=(st+record.index(min(record)))/10000
    np.save('../Data/Other_Infomation/best_density_neuron.npy',best_par)
