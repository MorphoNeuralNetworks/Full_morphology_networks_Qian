import numpy as np
import csv,os,random
import matplotlib.pyplot as plt

import igraph as ig
import cairo
import cv2
import math

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

connectmap=np.load('D:/QPH/BrainNetwork_Half/bouton_connection.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络
g_h = ig.Graph(directed=True)
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
    
g_h.add_vertices(node_list)
g_h.add_edges(edge_list)
g_h.es['weight']=edge_weight
g_h.vs['label'] = node_list


connectmap=np.load('D:/QPH/BrainNetwork_Pertubation/Pertubation_Result/scale_0_prune_0_delete_0.5_all_Bouton.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络
g_d = ig.Graph(directed=True)
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
g_d.add_vertices(node_list)
g_d.add_edges(edge_list)
g_d.es['weight']=edge_weight
g_d.vs['label'] = node_list

connectmap=np.load('D:/QPH/BrainNetwork_Pertubation/Pertubation_Result/scale_0.5_prune_0_delete_0_all_Bouton.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络
g_s = ig.Graph(directed=True)
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
g_s.add_vertices(node_list)
g_s.add_edges(edge_list)
g_s.es['weight']=edge_weight
g_s.vs['label'] = node_list

connectmap=np.load('D:/QPH/BrainNetwork_Pertubation/Pertubation_Result/scale_0_prune_0.5_delete_0_all_Bouton.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络
g_p = ig.Graph(directed=True)
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
g_p.add_vertices(node_list)
g_p.add_edges(edge_list)
g_p.es['weight']=edge_weight
g_p.vs['label'] = node_list

'''
## 网络degree分布
degree_dis=g.degree_distribution()
x_n=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_n=[]
for t in degree_dis._bins:
    y_n.append(t+1)
x_n=np.log10(x_n)
y_n=np.log10(y_n)

degree_dis=g_den.degree_distribution()
x_den=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_den=[]
for t in degree_dis._bins:
    y_den.append(t+1)
x_den=np.log10(x_den)
y_den=np.log10(y_den)

degree_dis=g_h.degree_distribution()
x_h=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_h=[]
for t in degree_dis._bins:
    y_h.append(t+1)
x_h=np.log10(x_h)
y_h=np.log10(y_h)

degree_dis=g_d.degree_distribution()
x_d=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_d=[]
for t in degree_dis._bins:
    y_d.append(t+1)
x_d=np.log10(x_d)
y_d=np.log10(y_d)

degree_dis=g_s.degree_distribution()
x_s=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_s=[]
for t in degree_dis._bins:
    y_s.append(t+1)
x_s=np.log10(x_s)
y_s=np.log10(y_s)

degree_dis=g_p.degree_distribution()
x_p=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y_p=[]
for t in degree_dis._bins:
    y_p.append(t+1)
x_p=np.log10(x_p)
y_p=np.log10(y_p)  


print('Normal:')
print([len(g.vs),len(g.es)])

print('Half Data:')
print([len(g_h.vs),len(g_h.es)])

print('0.5 Bouton:')
print([len(g_d.vs),len(g_d.es)])
    
print('0.5 Scale:')
print([len(g_s.vs),len(g_s.es)])
    
print('0.5 Prune:')
print([len(g_p.vs),len(g_p.es)])


plt.close()
fig,ax=plt.subplots(figsize=(6,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
alpha_value=0.9
plt.scatter(x_n,y_n,alpha=alpha_value,c="#1f77b4")
plt.scatter(x_den,y_den,marker='o',alpha=alpha_value,c="#ff7f0e")
plt.scatter(x_h,y_h,marker='o',alpha=alpha_value,c="#8c564b")
# plt.scatter(x_d,y_d,marker='x',alpha=alpha_value)
# plt.scatter(x_s,y_s,marker='+',alpha=alpha_value)
# plt.scatter(x_p,y_p,marker='*',alpha=alpha_value)
# plt.scatter(x_er,y_er,marker='+',c='#FF0000',alpha=alpha_value-0.1)
# plt.scatter(x_ws,y_ws,marker='x',c='#9400D3',alpha=alpha_value-0.15)
plt.legend(['Predicted','Uniform','Half of predicted'],prop={'family':'Calibri','weight':'bold','size':14},frameon=False)
plt.xticks([0,1,2],['1','10','100'],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([0,1,2],['1','10','100'],size=14,fontproperties='Calibri',weight='bold')
plt.xlabel('Degrees',fontsize=22,fontproperties='Calibri',weight='bold')
plt.ylabel('Frequency',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
plt.savefig('degree compare.png', dpi=300)
'''

## Triad census distribution
temp=[[] for i in range(6)]
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
for x in g_h.triad_census():
    temp[2].append(int(x))
for x in g_d.triad_census():
    temp[3].append(int(x))
for x in g_s.triad_census():
    temp[4].append(int(x))
for x in g_p.triad_census():
    temp[5].append(int(x))

def RatioChange(x):
    if x>=1:
        y=np.log10(x)
    elif x!=0:
        y=-np.log10(1/x)-0.25
    else:
        y=x-0.25
    return y

for i in range(1,len(temp)):
    for j in range(0,len(temp[0])):
        temp[i][j]=RatioChange(temp[i][j]/temp[0][j])



## Ratio
plt.close()
bar_width = 0.2
x=np.arange(1,17)
fig,ax=plt.subplots(figsize=(8,3))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.bar(x+bar_width*0, temp[1], bar_width, align="center",color=["#ff7f0e"])
plt.bar(x+bar_width*1, temp[2], bar_width, align="center",color=["#8c564b"])
plt.bar(x+bar_width*2, temp[3], bar_width, align="center",color=["#9467bd"])
plt.bar(x+bar_width*3, temp[4], bar_width, align="center",color=["#d62728"])
plt.bar(x+bar_width*4, temp[5], bar_width, align="center",color=["#2ca02c"])
plt.legend(['Uniform/Predicted','Half/Predicted','Delete:0.5/Predicted','Scale:0.5/Predicted','Prune:0.5/Predicted'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
# plt.ylim([0,9])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([-2.25,-1.25,-0.25,0,1],['0.01','0.1','0','1','10'],size=14,fontproperties='Calibri',weight='bold')
# plt.xlabel('States',fontsize=12)
plt.ylabel('Times',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
plt.savefig('triad census.png', dpi=300)
