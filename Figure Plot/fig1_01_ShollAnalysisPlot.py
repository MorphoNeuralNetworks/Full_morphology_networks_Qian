import navis,os,math,csv
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
import shutil

from scipy.stats import ttest_rel,ttest_ind,levene,ks_2samp
global step
step=100

# 获取神经元所在脑区的信息
with open(r'..\Data\Other_Infomation\BoutonDataCellType.csv', 'r', newline='') as csvfile:
    t = csv.reader(csvfile)
    area_data=np.array(list(t))
    csvfile.close()
cell_type=dict()
for root, dirs, files in os.walk(r'..\Data\Noregisted\bouton_swc'):
    for file in files:
        t=file.split('.')[0]
        tt=np.where(area_data[:,0]==t)
        if len(tt[0])==0:
            print(t+' out of file')
        else:
            cell_type[file.split('.')[0]]=str(area_data[tt[0],1][0])
cell_count=dict()
for key in cell_type:
    t=cell_type[key]
    if t not in cell_count:
        cell_count[t]=1
    else:
        cell_count[t]+=1

## 计算cell type的均值
sholl_result=np.load('sholl_result.npy', allow_pickle=True).item()
sholl_result_density=np.load('sholl_result_density_all.npy', allow_pickle=True).item()
best_par=dict()
# for name in cell_count.keys():
#     maxlen=0
#     count=0
#     if cell_count[name]<20:
#         continue
#     for key in cell_type:
#         if cell_type[key]==name:
#             if len(sholl_result[key][0])>maxlen:
#                 maxlen=len(sholl_result[key][0])
#             if len(sholl_result_density[key])>maxlen:
#                 maxlen=len(sholl_result_density[key])
#             count+=1
#     sholl_data=np.zeros((4,count,maxlen))
    
#     count=0
#     for key in cell_type:
#         if cell_type[key]==name:
#             t=len(sholl_result[key][0])
#             sholl_data[0:3,count,0:t]=sholl_result[key]
#             t=len(sholl_result_density[key])
#             sholl_data[3,count,0:t]=sholl_result_density[key]
#             count+=1
#     # 找到每个cell type的bouton和boutondensity的最优参数
#     bouton_result=np.mean(sholl_data[0,:,:],0)
#     boutondensity=np.mean(sholl_data[3,:,:],0)
#     st=round(np.mean(boutondensity)/np.mean(bouton_result),3)*10000-50000
#     end=round(np.mean(boutondensity)/np.mean(bouton_result),3)*10000+10000
#     record=[]
#     for k in range(int(st),int(end)):
#         boutondensity_new=boutondensity*k/10000
#         res=bouton_result-boutondensity_new
#         loss=np.sum(np.square(res))
#         record.append(loss)
#     # plt.plot(range(int(st),int(end)),record)
#     best_par[name]=(st+record.index(min(record)))/10000
#     # np.save('best_density.npy',best_par)

# 计算每个cell typde的density
# count=1
# for key in sholl_result.keys():
#     if count%100==0:
#         print(count)
#     count+=1
#     maxlen=max(len(sholl_result[key][0,:]),len(sholl_result_density[key]))
#     sholl_data=np.zeros((2,maxlen))
#     sholl_data[0,0:len(sholl_result[key][0,:])]=sholl_result[key][0,:]
#     sholl_data[1,0:len(sholl_result_density[key])]=sholl_result_density[key]
#     # 找到每个cell type的bouton和boutondensity的最优参数
#     bouton_result=sholl_data[0,:]
#     boutondensity=sholl_data[1,:]
#     st=round(np.mean(boutondensity)/np.mean(bouton_result),3)*1000-10000
#     end=round(np.mean(boutondensity)/np.mean(bouton_result),3)*1000+1000
#     record=[]
#     for k in range(int(st),int(end)):
#         boutondensity_new=boutondensity*k/1000
#         res=bouton_result-boutondensity_new
#         loss=np.sum(np.square(res))
#         record.append(loss)
#     # plt.plot(range(int(st),int(end)),record)
#     best_par[key]=(st+record.index(min(record)))/1000
#     np.save('best_density_neuron.npy',best_par)
## 比较两个cell type的独立性
best_density_neuron=np.load("best_density_neuron.npy",allow_pickle=True).item()
name=['VPM','SSp-m']
t1,t2=[],[]
for key in cell_type:
    if cell_type[key]==name[0]:
        t1.append(best_density_neuron[key]*0.061)
    if cell_type[key]==name[1]:
        t2.append(best_density_neuron[key]*0.061)
print(ks_2samp(t1,t2))
'''
## 画图
sholl_result=np.load('sholl_result.npy', allow_pickle=True).item()
sholl_result_density=np.load('sholl_result_density_each.npy', allow_pickle=True).item()
for name in ['VPM','SSp-m']:#cell_count.keys():
    maxlen=0
    count=0
    if cell_count[name]<78:
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
    
    ## test ks_2samp,ttest_ind
    shade_list=[]
    for i in range(np.shape(sholl_data)[2]):
        # (_,tt)=levene(sholl_data[0,:,i],sholl_data[3,:,i])
        # if tt<0.1:
        #     (_,t)=ttest_ind(sholl_data[0,:,i],sholl_data[3,:,i],equal_var=False)
        # else:
        #     (_,t)=ttest_ind(sholl_data[0,:,i],sholl_data[3,:,i])
        (_,t)=ttest_rel(sholl_data[0,:,i],sholl_data[3,:,i])
        if t<0.005:
            shade_list.append(i*100+50)
    ax2.bar(shade_list,[max(np.mean(sholl_data[3,:,:],0))]*len(shade_list),width=100,align="center",color=['#A9A9A9'],alpha=0.7)
    # ax2.legend(['Predicted bouton','Branch points','Uniform bouton'],prop={'family':'Calibri','weight':'bold','size':20},frameon=False)
    # plt.title(name,fontsize=20,fontproperties='Calibri',weight='bold')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    # plt.savefig(name+'_all.png', dpi=300)
'''