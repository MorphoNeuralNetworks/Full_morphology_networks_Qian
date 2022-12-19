import numpy as np
import csv,os,random
import matplotlib.pyplot as plt

import igraph as ig
import cairo
import cv2
import math
'''
connectmap=np.load('D:/QPH/BrainNetwork/bouton_connection.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络
g = ig.Graph(directed=True)
node_list=[]
edge_list=[]
edge_weight=[]
for x in connect_map:
    if x[0] not in node_list:
        node_list.append(x[0])
    if x[1] not in node_list:
        node_list.append(x[1])
    edge_list.append((x[0],x[1]))
    edge_weight.append(x[3])
    
g.add_vertices(node_list)
g.add_edges(edge_list)
g.es['weight']=edge_weight
g.vs['label'] = node_list


connectmap=np.load('D:/QPH/BrainNetwork/boutondensity_each_connection.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络
g_den = ig.Graph(directed=True)
node_list=[]
edge_list=[]
edge_weight=[]
for x in connect_map:
    if x[0] not in node_list:
        node_list.append(x[0])
    if x[1] not in node_list:
        node_list.append(x[1])
    edge_list.append((x[0],x[1]))
    edge_weight.append(x[3])
    
g_den.add_vertices(node_list)
g_den.add_edges(edge_list)
g_den.es['weight']=edge_weight
g_den.vs['label'] = node_list

g_h=[]
for id_t in range(1,6):
    connectmap=np.load('D:/QPH/BrainNetwork_Half/BrainNetwork_'+str(id_t)+'/bouton_connection.npy',allow_pickle=True)
    data=connectmap[:,3].astype(np.float64)
    t=np.where(data<0)
    connect_map = np.delete(connectmap,t,0)
    # 生成网络
    g_h_t = ig.Graph(directed=True)
    node_list=[]
    edge_list=[]
    edge_weight=[]
    for x in connect_map:
        if x[0] not in node_list:
            node_list.append(x[0])
        if x[1] not in node_list:
            node_list.append(x[1])
        edge_list.append((x[0],x[1]))
        edge_weight.append(x[3])
        
    g_h_t.add_vertices(node_list)
    g_h_t.add_edges(edge_list)
    g_h_t.es['weight']=edge_weight
    g_h_t.vs['label'] = node_list
    g_h.append(g_h_t)



g_d=[]
g_p=[]
g_s=[]
for id_t in ['','_1','_2','_3','_4']:
    connectmap=np.load('D:/QPH/BrainNetwork_Pertubation'+id_t+'/Pertubation_Result/scale_0_prune_0_delete_0.5_all_Bouton.npy',allow_pickle=True)
    data=connectmap[:,3].astype(np.float64)
    t=np.where(data<0)
    connect_map = np.delete(connectmap,t,0)
    # 生成网络
    g_d_t = ig.Graph(directed=True)
    node_list=[]
    edge_list=[]
    edge_weight=[]
    for x in connect_map:
        if x[0] not in node_list:
            node_list.append(x[0])
        if x[1] not in node_list:
            node_list.append(x[1])
        edge_list.append((x[0],x[1]))
        edge_weight.append(x[3])
    g_d_t.add_vertices(node_list)
    g_d_t.add_edges(edge_list)
    g_d_t.es['weight']=edge_weight
    g_d_t.vs['label'] = node_list
    g_d.append(g_d_t)
    
    connectmap=np.load('D:/QPH/BrainNetwork_Pertubation'+id_t+'/Pertubation_Result/scale_0.5_prune_0_delete_0_all_Bouton.npy',allow_pickle=True)
    data=connectmap[:,3].astype(np.float64)
    t=np.where(data<0)
    connect_map = np.delete(connectmap,t,0)
    # 生成网络
    g_s_t = ig.Graph(directed=True)
    node_list=[]
    edge_list=[]
    edge_weight=[]
    for x in connect_map:
        if x[0] not in node_list:
            node_list.append(x[0])
        if x[1] not in node_list:
            node_list.append(x[1])
        edge_list.append((x[0],x[1]))
        edge_weight.append(x[3])
    g_s_t.add_vertices(node_list)
    g_s_t.add_edges(edge_list)
    g_s_t.es['weight']=edge_weight
    g_s_t.vs['label'] = node_list
    g_s.append(g_s_t)
    
    connectmap=np.load('D:/QPH/BrainNetwork_Pertubation'+id_t+'/Pertubation_Result/scale_0_prune_0.5_delete_0_all_Bouton.npy',allow_pickle=True)
    data=connectmap[:,3].astype(np.float64)
    t=np.where(data<0)
    connect_map = np.delete(connectmap,t,0)
    # 生成网络
    g_p_t = ig.Graph(directed=True)
    node_list=[]
    edge_list=[]
    edge_weight=[]
    for x in connect_map:
        if x[0] not in node_list:
            node_list.append(x[0])
        if x[1] not in node_list:
            node_list.append(x[1])
        edge_list.append((x[0],x[1]))
        edge_weight.append(x[3])
    g_p_t.add_vertices(node_list)
    g_p_t.add_edges(edge_list)
    g_p_t.es['weight']=edge_weight
    g_p_t.vs['label'] = node_list
    g_p.append(g_p_t)



## 网络degree分布
degree_dis=g.degree_distribution()
x_n=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_n=[]
for t in degree_dis._bins:
    y_n.append(t+1)
# x_n=np.log10(x_n)
# y_n=np.log10(y_n)

degree_dis=g_den.degree_distribution()
x_den=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_den=[]
for t in degree_dis._bins:
    y_den.append(t+1)
# x_den=np.log10(x_den)
# y_den=np.log10(y_den)

x_degree_half=[]
y_degree_half=[]
for g_t in g_h:
    degree_dis=g_t.degree_distribution()
    x_h1=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
    y_h1=[]
    for t in degree_dis._bins:
        y_h1.append(t+1)
    # x_h1=np.log10(x_h1)
    # y_h1=np.log10(y_h1)
    x_degree_half.append(x_h1)
    y_degree_half.append(y_h1)

x_degree_delete=[]
y_degree_delete=[]
for g_t in g_d:
    degree_dis=g_t.degree_distribution()
    x_d1=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
    y_d1=[]
    for t in degree_dis._bins:
        y_d1.append(t+1)
    # x_d1=np.log10(x_d1)
    # y_d1=np.log10(y_d1)
    x_degree_delete.append(x_d1)
    y_degree_delete.append(y_d1)
    
x_degree_scale=[]
y_degree_scale=[]
for g_t in g_s:
    degree_dis=g_t.degree_distribution()
    x_s1=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
    y_s1=[]
    for t in degree_dis._bins:
        y_s1.append(t+1)
    # x_s1=np.log10(x_s1)
    # y_s1=np.log10(y_s1)
    x_degree_scale.append(x_s1)
    y_degree_scale.append(y_s1)

x_degree_prune=[]
y_degree_prune=[]
for g_t in g_p:
    degree_dis=g_t.degree_distribution()
    x_p1=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
    y_p1=[]
    for t in degree_dis._bins:
        y_p1.append(t+1)
    # x_p1=np.log10(x_p1)
    # y_p1=np.log10(y_p1)
    x_degree_prune.append(x_p1)
    y_degree_prune.append(y_p1)    


print('Normal:')
print([len(g.vs),len(g.es)])

print('Half Data:')
for g_t in g_h:
    print([len(g_t.vs),len(g_t.es)])

print('0.5 Bouton:')
for g_t in g_d:
    print([len(g_t.vs),len(g_t.es)])
    
print('0.5 Scale:')
for g_t in g_s:
    print([len(g_t.vs),len(g_t.es)])
    
print('0.5 Prune:')
for g_t in g_p:
    print([len(g_t.vs),len(g_t.es)])



tt=[len(x) for x in x_degree_half]
x_half=range(2,max(tt)+2)
tt=[len(x) for x in y_degree_half]
y_half=np.zeros((5,max(tt)))
cc=0
for y in y_degree_half:
    y_half[cc,0:len(y)]=y
    cc+=1
y_half=np.mean(y_half,0)

tt=[len(x) for x in x_degree_delete]
x_delete=range(2,max(tt)+2)
tt=[len(x) for x in y_degree_delete]
y_delete=np.zeros((5,max(tt)))
cc=0
for y in y_degree_delete:
    y_delete[cc,0:len(y)]=y
    cc+=1
y_delete=np.mean(y_delete,0)

tt=[len(x) for x in x_degree_scale]
x_scale=range(2,max(tt)+2)
tt=[len(x) for x in y_degree_scale]
y_scale=np.zeros((5,max(tt)))
cc=0
for y in y_degree_scale:
    y_scale[cc,0:len(y)]=y
    cc+=1
y_scale=np.mean(y_scale,0)

tt=[len(x) for x in x_degree_prune]
x_prune=range(2,max(tt)+2)
tt=[len(x) for x in y_degree_prune]
y_prune=np.zeros((5,max(tt)))
cc=0
for y in y_degree_prune:
    y_prune[cc,0:len(y)]=y
    cc+=1
y_prune=np.mean(y_prune,0)



plt.close()
size=20
alpha_value=0.7
plt.scatter(x_n,y_n,alpha=alpha_value)
plt.scatter(x_den,y_den,marker='o',alpha=alpha_value)
plt.scatter(x_half,y_half,marker='o',alpha=alpha_value)
plt.scatter(x_delete,y_delete,marker='x',alpha=alpha_value)
plt.scatter(x_scale,y_scale,marker='+',alpha=alpha_value)
plt.scatter(x_prune,y_prune,marker='*',alpha=alpha_value)
# plt.scatter(x_er,y_er,marker='+',c='#FF0000',alpha=alpha_value-0.1)
# plt.scatter(x_ws,y_ws,marker='x',c='#9400D3',alpha=alpha_value-0.15)
# plt.scatter(x_ba,y_ba,marker='o',facecolors='none',edgecolors='#A0522D',alpha=alpha_value-0.2)
plt.legend(['origin bouton','uniform bouton','half of neuron','0.5 bouton','0.5 Scale','0.5 Prune'],fontsize=11)
# plt.xticks([0,1,2],['1','10','100'])
# plt.yticks([0,1,2,3],['1','10','100','1000'])
plt.xlabel('Degrees',fontsize=16)
plt.ylabel('Frequency',fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
'''



'''
## Triad census distribution
bar_width = 0.15
temp=[[] for i in range(22)]
cc=0
# for x in g.triad_census():
#     temp[0].append(np.log10(int(x)+1))
# for x in g_den.triad_census():
#     temp[1].append(np.log10(int(x)+1))
# cc=2
# for g_t in g_h:
#     for x in g_t.triad_census():
#         temp[cc].append(np.log10(int(x)+1))
#     cc+=1
# for g_t in g_d:
#     for x in g_t.triad_census():
#         temp[cc].append(np.log10(int(x)+1))
#     cc+=1
# for g_t in g_s:
#     for x in g_t.triad_census():
#         temp[cc].append(np.log10(int(x)+1))
#     cc+=1
# for g_t in g_p:
#     for x in g_t.triad_census():
#         temp[cc].append(np.log10(int(x)+1))
#     cc+=1
for x in g.triad_census():
    temp[0].append(int(x))
for x in g_den.triad_census():
    temp[1].append(int(x))
cc=2
for g_t in g_h:
    for x in g_t.triad_census():
        temp[cc].append(int(x))
    cc+=1
for g_t in g_d:
    for x in g_t.triad_census():
        temp[cc].append(int(x))
    cc+=1
for g_t in g_s:
    for x in g_t.triad_census():
        temp[cc].append(int(x))
    cc+=1
for g_t in g_p:
    for x in g_t.triad_census():
        temp[cc].append(int(x))
    cc+=1

for i in range(1,len(temp)):
    for j in range(0,len(temp[0])):
        temp[i][j]=temp[i][j]/temp[0][j]


x_h=np.mean(temp[2:7],0)
std_h=np.std(temp[2:7],0)
x_d=np.mean(temp[7:12],0)
std_d=np.std(temp[7:12],0)
x_s=np.mean(temp[12:17],0)
std_s=np.std(temp[12:17],0)
x_p=np.mean(temp[17:22],0)
std_p=np.std(temp[17:22],0)


## log value
# plt.close()
# x=np.arange(1,17)
# plt.bar(x, temp[0], bar_width,alpha=0.7)
# plt.bar(x+bar_width*1, temp[1], bar_width, align="center",alpha=0.7)
# plt.bar(x+bar_width*2, x_h, bar_width, align="center",alpha=0.7,yerr=std_h)
# plt.bar(x+bar_width*3, x_d, bar_width, align="center",alpha=0.7,yerr=std_d)
# plt.bar(x+bar_width*4, x_s, bar_width, align="center",alpha=0.7,yerr=std_s)
# plt.bar(x+bar_width*5, x_p, bar_width, align="center",alpha=0.7,yerr=std_p)
# plt.legend(['origin bouton','uniform bouton','half of neuron','0.5 bouton','0.5 Scale','0.5 Prune'])
# plt.ylim([0,9])
# plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],fontsize=12)
# plt.yticks([0,1,2,3,4,5,6,7,8],['1','10','1e2','1e3','1e4','1e5','1e6','1e7','1e8'],fontsize=12)
# plt.xlabel('States',fontsize=12)
# plt.ylabel('Times(log)',fontsize=12)

## Ratio
plt.close()
x=np.arange(1,17)
plt.bar(x+bar_width*0, temp[1], bar_width, align="center",alpha=0.7)
plt.bar(x+bar_width*1, x_h, bar_width, align="center",alpha=0.7,yerr=std_h)
plt.bar(x+bar_width*2, x_d, bar_width, align="center",alpha=0.7,yerr=std_d)
plt.bar(x+bar_width*3, x_s, bar_width, align="center",alpha=0.7,yerr=std_s)
plt.bar(x+bar_width*4, x_p, bar_width, align="center",alpha=0.7,yerr=std_p)
plt.legend(['uniform bouton','half of neuron','0.5 bouton','0.5 Scale','0.5 Prune'])
# plt.ylim([0,9])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],fontsize=12)
# plt.yticks([0,1,2,3,4,5,6,7,8],['1','10','1e2','1e3','1e4','1e5','1e6','1e7','1e8'],fontsize=12)
plt.xlabel('States',fontsize=12)
plt.ylabel('Ratio',fontsize=12)

'''



'''
properties=np.load('CostStorageRouting_confirm.npy',allow_pickle=True)

results=[]
for i in properties:
    x=i.tolist()
    x[0]=1
    x=list(map(float,x))
    temp=dict()
    temp['Cost(1e5)']=x[1]/100000
    temp['Storage_capacity(1e2)']=x[2]/100
    temp['Routing_efficiency']=x[3]
    # temp['Storage/Cost(1e-3)']=x[2]/x[1]*1000
    # temp['Routing/Cost(1e-5)']=x[3]/x[1]*100000
    results.append(temp)
    

data_length = len(results[0])
# 将极坐标根据数据长度进行等分
angles = np.linspace(0, 2*np.pi, data_length, endpoint=False)
labels = [key for key in results[0].keys()]
score = [[v for v in result.values()] for result in results]
# 使雷达图数据封闭
score_d = np.concatenate((score[0], [score[0][0]]))
score_h = np.concatenate((score[5], [score[5][0]]))
score_n = np.concatenate((score[10], [score[10][0]]))
score_nd = np.concatenate((score[11], [score[11][0]]))
score_p = np.concatenate((score[12], [score[12][0]]))
score_s = np.concatenate((score[17], [score[17][0]]))
angles = np.concatenate((angles, [angles[0]]))
labels = np.concatenate((labels, [labels[0]]))
# 设置图形的大小
plt.close('all')
fig = plt.figure(figsize=(8, 6), dpi=100)
# 新建一个子图
ax = plt.subplot(111, polar=True)
# 绘制雷达图
ax.plot(angles, score_n)
ax.plot(angles, score_nd)
ax.plot(angles, score_h)
ax.plot(angles, score_d)
ax.plot(angles, score_s)
ax.plot(angles, score_p)
# 设置雷达图中每一项的标签显示
ax.set_thetagrids(angles*180/np.pi, labels)
# 设置雷达图的0度起始位置
ax.set_theta_zero_location('N')
# 设置雷达图的坐标刻度范围
# ax.set_rlim(0, 100)
# 设置雷达图的坐标值显示角度，相对于起始角度的偏移量
ax.set_rlabel_position(270)
plt.legend(['origin bouton','uniform bouton','half of neuron','0.5 bouton','0.5 Scale','0.5 Prune'])
plt.show()
'''



'''
BoutonRatio=np.load('BoutonRatio_bouton.npy',allow_pickle=True).item()
BoutonRatio=[[key,BoutonRatio[key]] for key in BoutonRatio.keys()]
results=[]
for i in BoutonRatio:
    x=i[1]
    x=list(map(float,x))
    temp=dict()
    temp['Connected Bouton(1e4)']=x[0]/10000
    temp['Total Bouton(1e6)']=x[1]/1000000
    temp['Connected Ratio(1e-2)']=x[2]*100
    results.append(temp)
    

data_length = len(results[0])
# 将极坐标根据数据长度进行等分
angles = np.linspace(0, 2*np.pi, data_length, endpoint=False)
labels = [key for key in results[0].keys()]
score = [[v for v in result.values()] for result in results]
# 使雷达图数据封闭
score_d = np.concatenate((score[0], [score[0][0]]))
score_h = np.concatenate((score[5], [score[5][0]]))
score_n = np.concatenate((score[10], [score[10][0]]))
score_nd = np.concatenate((score[11], [score[11][0]]))
score_p = np.concatenate((score[12], [score[12][0]]))
score_s = np.concatenate((score[17], [score[17][0]]))
angles = np.concatenate((angles, [angles[0]]))
labels = np.concatenate((labels, [labels[0]]))
# 设置图形的大小
plt.close('all')
fig = plt.figure(figsize=(8, 6), dpi=100)
# 新建一个子图
ax = plt.subplot(111, polar=True)
# 绘制雷达图
ax.plot(angles, score_n)
ax.plot(angles, score_nd)
ax.plot(angles, score_h)
ax.plot(angles, score_d)
ax.plot(angles, score_s)
ax.plot(angles, score_p)
# 设置雷达图中每一项的标签显示
ax.set_thetagrids(angles*180/np.pi, labels)
# 设置雷达图的0度起始位置
ax.set_theta_zero_location('N')
# 设置雷达图的坐标刻度范围
# ax.set_rlim(0, 100)
# 设置雷达图的坐标值显示角度，相对于起始角度的偏移量
ax.set_rlabel_position(270)
plt.legend(['origin bouton','uniform bouton','half of neuron','0.5 bouton','0.5 Scale','0.5 Prune'])
'''

