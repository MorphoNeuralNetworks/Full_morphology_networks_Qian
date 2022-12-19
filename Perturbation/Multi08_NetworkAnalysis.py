### 对不同参数下的网络进行分析
import os
import numpy as np
import matplotlib.pyplot as plt
## 查看每种参数下weight的分布
# folderpath = os.listdir(r'.\Pertubation')
# for i in range(15,16):
#     folder=folderpath[i]
#     print(folder)
#     connectmap=np.load('.\\Pertubation_Result\\'+folder+'_Boutondensity.npy',allow_pickle=True)
#     data=connectmap[:,3].astype(np.float64)
#     t=np.where(data<0)
#     connect_map = np.delete(connectmap,t,0)
#     # plt.figure(i)
#     plt.hist(data,bins=19)

methods=['all','axon','dendrite']
name_list=['scale_all','scale_axon','scale_dendrite','prune_all','prune_axon','prune_dendrite','delete_all']

folderpath = os.listdir(r'.\Pertubation')
'''
feature_dict={}
cc=np.load('..\\BrainNetwork\\normal_bouton.npy',allow_pickle=True)
feature_dict['normal']=cc
for x in folderpath:
    cc=np.load('.\\graph_feature\\'+x+'_bouton.npy',allow_pickle=True)
    feature_dict[x]=cc

## 节点 边数量随三种参数的变化而变化
plt.close()
plt.subplot(1,3,1)
data_list=[]
for method in methods:
    temp=[]
    for x in range(5,10):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        temp.append(feature_dict[name][0][0])
    data_list.append(temp)
for method in methods:    
    temp=[]
    for x in range(5,10):
        name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
        temp.append(feature_dict[name][0][0])
    data_list.append(temp)
temp=[]
for x in range(5,10):
    name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
    temp.append(feature_dict[name][0][0])
data_list.append(temp)  
data_list=np.array(data_list) 
plt.title('Number of nodes')
plt.plot(data_list.T)
plt.legend(name_list)
plt.xticks(range(0,5),['0.5','0.6','0.7','0.8','0.9'])

plt.subplot(1,3,2)
data_list=[]
methods=['all','axon','dendrite']
for method in methods:
    temp=[]
    for x in range(5,10):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        temp.append(feature_dict[name][0][1])
    data_list.append(temp)
for method in methods:    
    temp=[]
    for x in range(5,10):
        name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
        temp.append(feature_dict[name][0][1])
    data_list.append(temp)
temp=[]
for x in range(5,10):
    name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
    temp.append(feature_dict[name][0][1])
data_list.append(temp)  
data_list=np.array(data_list) 
plt.title('Number of edges')
plt.plot(data_list.T)
plt.legend(name_list)
plt.xticks(range(0,5),['0.5','0.6','0.7','0.8','0.9'])

plt.subplot(1,3,3)
data_list=[]
methods=['all','axon','dendrite']
for method in methods:
    temp=[]
    for x in range(5,10):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        temp.append(feature_dict[name][0][1])
    # temp.append(feature_dict['normal'][0][1])
    for x in range(12,22,2):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        temp.append(feature_dict[name][0][1])
    data_list.append(temp)
    
data_list=np.array(data_list) 
plt.title('Number of edges')
plt.plot(data_list.T)
plt.legend(name_list[0:3])
plt.xticks(range(0,11),['0.5','0.6','0.7','0.8','0.9','1.0','1.2','1.4','1.6','1.8','2.0'])

## 点分布
plt.close()
plt.subplot(2,2,1)
data_list=[]
for method in methods[0:1]:
    temp=[]
    for x in range(5,10):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t=feature_dict[name][1]
        y_t=feature_dict[name][2]
        plt.scatter(x_t,y_t)
    # x_t=feature_dict['normal'][1]
    # y_t=feature_dict['normal'][2]
    # plt.scatter(x_t,y_t)
    for x in range(12,22,2):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t=feature_dict[name][1]
        y_t=feature_dict[name][2]
        plt.scatter(x_t,y_t)

plt.title('Degree distribution-Scale')
plt.legend(['0.5','0.6','0.7','0.8','0.9','1.0','1.2','1.4','1.6','1.8','2.0'])
plt.xticks([0,1,2,3],['1','10','100','1000'])
plt.yticks([0,1,2,3],['1','10','100','1000'])
plt.xlabel('Degrees(log)',fontsize=12)
plt.ylabel('Frequency(log)',fontsize=12)

plt.subplot(2,2,2)
data_list=[]
for method in methods[0:1]:
    temp=[]
    for x in range(5,10):
        name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
        x_t=feature_dict[name][1]
        y_t=feature_dict[name][2]
        plt.scatter(x_t,y_t)
plt.title('Degree distribution-Prune')
plt.legend(['0.5','0.6','0.7','0.8','0.9'])
plt.xticks([0,1,2,3],['1','10','100','1000'])
plt.yticks([0,1,2,3],['1','10','100','1000'])
plt.xlabel('Degrees(log)',fontsize=12)
plt.ylabel('Frequency(log)',fontsize=12)

plt.subplot(2,2,3)
data_list=[]
for x in range(5,10):
    name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
    x_t=feature_dict[name][1]
    y_t=feature_dict[name][2]
    plt.scatter(x_t,y_t)
plt.title('Degree distribution-delete')
plt.legend(['0.5','0.6','0.7','0.8','0.9'])
plt.xticks([0,1,2,3],['1','10','100','1000'])
plt.yticks([0,1,2,3],['1','10','100','1000'])
plt.xlabel('Degrees(log)',fontsize=12)
plt.ylabel('Frequency(log)',fontsize=12)


## 三元组普查
plt.close()
plt.subplot(2,2,1)
data_list=[]
bar_width=0.05
for method in methods[0:1]:
    temp=[]
    count=0
    for x in range(5,10):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t=feature_dict[name][3]
        plt.bar(np.arange(1,17)+bar_width*count, x_t, bar_width, align="center")
        count+=1
    # x_t=feature_dict['normal'][3]
    # plt.bar(np.arange(1,17)+bar_width*count, x_t, bar_width, align="center")
    count+=1
    for x in range(12,22,2):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t=feature_dict[name][3]
        plt.bar(np.arange(1,17)+bar_width*count, x_t, bar_width, align="center")
        count+=1
plt.title('Triad census-scale')
plt.legend(['0.5','0.6','0.7','0.8','0.9'])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],fontsize=12)
plt.xlabel('States',fontsize=12)
plt.ylabel('Times(log)',fontsize=12)

plt.subplot(2,2,2)
data_list=[]
bar_width=0.15
for method in methods[0:1]:
    temp=[]
    count=0
    for x in range(5,10):
        name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
        x_t=feature_dict[name][3]
        plt.bar(np.arange(1,17)+bar_width*count, x_t, bar_width, align="center")
        count+=1
plt.title('Triad census-prune')
plt.legend(['0.5','0.6','0.7','0.8','0.9'])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],fontsize=12)
plt.xlabel('States',fontsize=12)
plt.ylabel('Times(log)',fontsize=12)

plt.subplot(2,2,3)
data_list=[]
for x in range(5,10):
    name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
    x_t=feature_dict[name][3]
    plt.bar(np.arange(1,17)+bar_width*count, x_t, bar_width, align="center")
    count+=1
plt.title('Triad census-delete')
plt.legend(['0.5','0.6','0.7','0.8','0.9'])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],fontsize=12)
plt.xlabel('States',fontsize=12)
plt.ylabel('Times(log)',fontsize=12)

'''



feature_dict={}
cc=np.load('.\\Temp_Data\\CostStorageRouting_bouton.npy',allow_pickle=True)
for x in cc:
    t=str(x[0])
    t=t.replace('_bouton','')
    x[1]=float(x[1])/10000
    c=x[1:].astype(np.float64)
    feature_dict[t]=c.tolist()

## 单纯看数值
plt.close()
plt.subplot(2,2,1)
for method in methods:
    x_t=[]
    y_t=[]
    txt=[]
    for x in range(5,10):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t.append(feature_dict[name][2])
        y_t.append(feature_dict[name][1])  
        txt.append(str(x/10))
    x_t.append(feature_dict['normal'][2])
    y_t.append(feature_dict['normal'][1])
    txt.append(str(10/10))
    for x in range(12,22,2):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t.append(feature_dict[name][2])
        y_t.append(feature_dict[name][1]) 
        txt.append(str(x/10))
    for i in range(len(x_t)):
        plt.annotate(txt[i], (x_t[i], y_t[i])) # 这里xy是需要标记的坐标，xytext是对应的标签坐标
    plt.scatter(x_t,y_t)
# plt.xlim([0.07,0.12])
# plt.ylim([2.9,5.1])
plt.legend(name_list[0:3])
plt.xlabel('routing efficiency',fontsize=12)
plt.ylabel('storage capacity',fontsize=12)

plt.subplot(2,2,2)
for method in methods:
    x_t=[]
    y_t=[]
    txt=[]
    for x in range(5,10):
        name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
        x_t.append(feature_dict[name][2])
        y_t.append(feature_dict[name][1])  
        txt.append(str(x/10))
    x_t.append(feature_dict['normal'][2])
    y_t.append(feature_dict['normal'][1])
    txt.append(str(10/10))
    for i in range(len(x_t)):
        plt.annotate(txt[i], (x_t[i], y_t[i])) # 这里xy是需要标记的坐标，xytext是对应的标签坐标
    plt.scatter(x_t,y_t)
# plt.xlim([0.07,0.12])
# plt.ylim([2.9,5.1])
plt.legend(name_list[3:6])
plt.xlabel('routing efficiency',fontsize=12)
plt.ylabel('storage capacity',fontsize=12)


plt.subplot(2,2,3)
x_t=[]
y_t=[]
txt=[]
for x in range(5,10):
    name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
    x_t.append(feature_dict[name][2])
    y_t.append(feature_dict[name][1])  
    txt.append(str(round(x/10,1)))
x_t.append(feature_dict['normal'][2])
y_t.append(feature_dict['normal'][1])
txt.append(str(10/10))
for i in range(len(x_t)):
    plt.annotate(txt[i], (x_t[i], y_t[i])) # 这里xy是需要标记的坐标，xytext是对应的标签坐标
plt.scatter(x_t,y_t)

# plt.xlim([0.07,0.12])
# plt.ylim([2.9,5.1])
plt.legend(name_list[-1])
plt.xlabel('routing efficiency',fontsize=12)
plt.ylabel('storage capacity',fontsize=12)


## 除以cost
plt.close()
plt.subplot(2,2,1)
for method in methods:
    x_t=[]
    y_t=[]
    txt=[]
    for x in range(5,10):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t.append(feature_dict[name][2]/feature_dict[name][0])
        y_t.append(feature_dict[name][1]/feature_dict[name][0])  
        txt.append(str(x/10))
    x_t.append(feature_dict['normal'][2]/feature_dict['normal'][0])
    y_t.append(feature_dict['normal'][1]/feature_dict['normal'][0])
    txt.append(str(10/10))
    for x in range(12,22,2):
        name='scale_'+str(x/10)+'_prune_0_delete_0_'+method
        x_t.append(feature_dict[name][2]/feature_dict[name][0])
        y_t.append(feature_dict[name][1]/feature_dict[name][0]) 
        txt.append(str(x/10))
    for i in range(len(x_t)):
        plt.annotate(txt[i], (x_t[i], y_t[i])) # 这里xy是需要标记的坐标，xytext是对应的标签坐标
    plt.scatter(x_t,y_t)
# plt.xlim([0.07,0.12])
# plt.ylim([2.9,5.1])
plt.legend(name_list[0:3])
plt.xlabel('routing efficiency/cost',fontsize=12)
plt.ylabel('storage capacity/cost',fontsize=12)

plt.subplot(2,2,2)
for method in methods:
    x_t=[]
    y_t=[]
    txt=[]
    for x in range(5,10):
        name='scale_0_prune_'+str(x/10)+'_delete_0_'+method
        x_t.append(feature_dict[name][2]/feature_dict[name][0])
        y_t.append(feature_dict[name][1]/feature_dict[name][0])  
        txt.append(str(x/10))
    x_t.append(feature_dict['normal'][2]/feature_dict['normal'][0])
    y_t.append(feature_dict['normal'][1]/feature_dict['normal'][0])
    txt.append(str(10/10))
    for i in range(len(x_t)):
        plt.annotate(txt[i], (x_t[i], y_t[i])) # 这里xy是需要标记的坐标，xytext是对应的标签坐标
    plt.scatter(x_t,y_t)
# plt.xlim([0.07,0.12])
# plt.ylim([2.9,5.1])
plt.legend(name_list[3:6])
plt.xlabel('routing efficiency/cost',fontsize=12)
plt.ylabel('storage capacity/cost',fontsize=12)


plt.subplot(2,2,3)
x_t=[]
y_t=[]
txt=[]
for x in range(5,10):
    name='scale_0_prune_0_delete_'+str(x/10)+'_'+methods[0]
    x_t.append(feature_dict[name][2]/feature_dict[name][0])
    y_t.append(feature_dict[name][1]/feature_dict[name][0])  
    txt.append(str(round(x/10,1)))
x_t.append(feature_dict['normal'][2]/feature_dict['normal'][0])
y_t.append(feature_dict['normal'][1]/feature_dict['normal'][0])
txt.append(str(10/10))
for i in range(len(x_t)):
    plt.annotate(txt[i], (x_t[i], y_t[i])) # 这里xy是需要标记的坐标，xytext是对应的标签坐标
plt.scatter(x_t,y_t)

# plt.xlim([0.07,0.12])
# plt.ylim([2.9,5.1])
plt.legend(name_list[-1])
plt.xlabel('routing efficiency/cost',fontsize=12)
plt.ylabel('storage capacity/cost',fontsize=12)

















