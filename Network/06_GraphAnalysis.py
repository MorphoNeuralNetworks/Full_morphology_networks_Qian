import numpy as np
import csv,os,random
import matplotlib.pyplot as plt
import BasicFunction as BF

import igraph as ig
import cairo
import cv2
import math
import seaborn as sns


# connectmap=np.load('bouton_connection.npy',allow_pickle=True)
# data1=connectmap[:,3].astype(np.float64)
# connectmap=np.load('boutondensity_each_connection.npy',allow_pickle=True)
# data2=connectmap[:,3].astype(np.float64)

# plt.close()
# fig,ax=plt.subplots(figsize=(10,4))
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# sns.histplot([data1,data2],alpha=0.8,log_scale=(False, True),bins=60,edgecolor=None)
# # plt.legend(['Uniform','Predicted'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False)
# # plt.ylim([0,5])
# # # plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],fontsize=12)
# plt.xticks([100,200,300,400,500],['100','200','300','400','500'],size=14,fontproperties='Calibri',weight='bold')
# plt.yticks([1,10,100,1000,10000,100000],['1','10','1e2','1e3','1e4','1e5'],size=14,fontproperties='Calibri',weight='bold')
# plt.xlabel('Connection Strength',fontsize=22,fontproperties='Calibri',weight='bold')
# plt.ylabel('Times(log)',fontsize=22,fontproperties='Calibri',weight='bold')
# plt.tight_layout()
# # plt.savefig('Connection Strength.png', dpi=300)

connectmap=np.load('boutondensity_all_connection.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)

t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络
g_da = ig.Graph(directed=True)
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
    
g_da.add_vertices(node_list)
g_da.add_edges(edge_list)
g_da.es['weight']=edge_weight
g_da.vs['label'] = node_list

connectmap=np.load('boutondensity_each_connection.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络
g_de = ig.Graph(directed=True)
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
    
g_de.add_vertices(node_list)
g_de.add_edges(edge_list)
g_de.es['weight']=edge_weight
g_de.vs['label'] = node_list


connectmap=np.load('bouton_connection.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)

t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# 生成网络

## igraph 画图
g = ig.Graph(directed=True)
node_list=[]
edge_list=[]
edge_weight=[]

region_count=dict()
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


## 网络degree分布
degree_dis=g.degree_distribution()
x=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
y=[]
for t in degree_dis._bins:
    y.append(t+1)
x=np.log10(x)
y=np.log10(y)

## 网络degree分布
degree_dis_da=g_da.degree_distribution()
x_da=np.array(range(int(degree_dis_da._min)+1,int(degree_dis_da._max)+1))
y_da=[]
for t in degree_dis_da._bins:
    y_da.append(t+1)
x_da=np.log10(x_da)
y_da=np.log10(y_da)

degree_dis_de=g_de.degree_distribution()
x_de=np.array(range(int(degree_dis_de._min)+1,int(degree_dis_de._max)+1))
y_de=[]
for t in degree_dis_de._bins:
    y_de.append(t+1)
x_de=np.log10(x_de)
y_de=np.log10(y_de)

# ER
g_er=ig.GraphBase.Erdos_Renyi(len(node_list),m=len(edge_list),directed=True,loops=False)
# g_er=ig.GraphBase.Erdos_Renyi(1660,m=17397,directed=True,loops=False)
degree_list_er=g_er.degree()
dd=plt.hist(degree_list_er,bins=max(degree_list_er)-min(degree_list_er))
x_er=[]
y_er=[]
for i in dd[1]:
    x_er.append(i+1)
for i in dd[0]:
    y_er.append(i+1)
x_er=x_er[1:]
x_er=np.log10(x_er)
y_er=np.log10(y_er)

# Small World
# g_ws=ig.GraphBase.Watts_Strogatz(1, len(node_list), 12, 0.02, loops=True) #density
g_ws=ig.GraphBase.Watts_Strogatz(1, len(node_list), 3, 0.02, loops=False) #bouton
g_ws.to_directed()
print("Small world:")
ig.summary(g_ws)
while g_ws.ecount() > g.ecount():
    k=random.randrange(0,g_ws.ecount()-1)
    temp=g_ws
    temp.delete_edges(k)
    if not temp.is_connected():
        continue
    else:
        g_ws.delete_edges(k)
ig.summary(g_ws)
degree_list_ws=g_ws.degree()
dd=plt.hist(degree_list_ws,bins=max(degree_list_ws)-min(degree_list_ws))
x_ws=[]
y_ws=[]
for i in dd[1]:
    x_ws.append(i+1)
for i in dd[0]:
    y_ws.append(i+1)
x_ws=x_ws[1:]
x_ws=np.log10(x_ws)
y_ws=np.log10(y_ws)

# Scale free
# g_ba=ig.GraphBase.Barabasi(n=len(node_list),m=12,directed=True) #density
g_ba=ig.GraphBase.Barabasi(n=len(node_list),m=7,directed=True) #bouton
print("Scale free:")
ig.summary(g_ba)
while g_ba.ecount() > g.ecount():
    k=random.randrange(0,g_ba.ecount()-1)
    temp=g_ba
    temp.delete_edges(k)
    if not temp.is_connected():
        continue
    else:
        g_ba.delete_edges(k)

degree_list_ba=g_ba.degree()
dd=plt.hist(degree_list_ba,bins=max(degree_list_ba)-min(degree_list_ba))
x_ba=[]
y_ba=[]
for i in dd[1]:
    x_ba.append(i+1)
for i in dd[0]:
    y_ba.append(i+1)
x_ba=x_ba[1:]
x_ba=np.log10(x_ba)
y_ba=np.log10(y_ba)

'''
plt.close()
fig,ax=plt.subplots(figsize=(6,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
alpha_value=0.7
plt.scatter(x,y,c='#1f77b4',s=34,alpha=alpha_value)
plt.scatter(x_de,y_de,c='#ff7f0e',s=34,alpha=alpha_value)
plt.scatter(x_da,y_da,c='#7f7f7f',s=34,alpha=alpha_value-0.1)
plt.scatter(x_er,y_er,marker='+',c='#2ca02c',s=60,alpha=alpha_value-0.1)
plt.scatter(x_ws,y_ws,marker='x',c='#d62728',s=40,alpha=alpha_value-0.15)
plt.scatter(x_ba,y_ba,marker='o',facecolors='none',edgecolors='#9467bd',s=30,alpha=alpha_value-0.2)
# plt.legend(['Predicted','Uniform','ER','Small world','Scale-Free'],prop={'family':'Calibri','weight':'bold','size':14},frameon=False)
# plt.legend(['Predicted','Uniform','Same density','ER','Small world','Scale-Free'],prop={'family':'Calibri','weight':'bold','size':14},frameon=False)
plt.xticks([0,1,2,3],['1','10','100','1000'],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([0,1,2,3],['1','10','100','1000'],size=14,fontproperties='Calibri',weight='bold')
plt.xlabel('Degrees(log)',fontsize=22,fontproperties='Calibri',weight='bold')
plt.ylabel('Frequency(log)',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('degree distribution.png', dpi=300)

from scipy.stats import ks_2samp
import scipy.stats as stats
print(ks_2samp(g.degree(),g_de.degree()))


print(stats.spearmanr(g.degree(),g_er.degree()))
print(stats.spearmanr(g.degree(),g_ws.degree()))
print(stats.spearmanr(g.degree(),g_ba.degree()))

print(stats.pearsonr(g.degree(),g_er.degree()))
print(stats.pearsonr(g.degree(),g_ws.degree()))
print(stats.pearsonr(g.degree(),g_ba.degree()))
'''


'''
## Triad census distribution
temp=[[],[],[],[],[],[]]
for x in g.triad_census():
    temp[0].append(np.log10(int(x)+1))
for x in g_da.triad_census():
    temp[1].append(np.log10(int(x)+1))
for x in g_de.triad_census():
    temp[2].append(np.log10(int(x)+1))
for x in g_er.triad_census():
    temp[3].append(np.log10(int(x)+1))
for x in g_ws.triad_census():
    temp[4].append(np.log10(int(x)+1))
for x in g_ba.triad_census():
    temp[5].append(np.log10(int(x)+1))

from scipy.stats import ks_2samp
import scipy.stats as stats
print(stats.spearmanr(g.triad_census(),g_de.triad_census()))
print(stats.spearmanr(g.triad_census(),g_er.triad_census()))
print(stats.spearmanr(g.triad_census(),g_ws.triad_census()))
print(stats.spearmanr(g.triad_census(),g_ba.triad_census()))

plt.close()
bar_width = 0.23
x=np.arange(1,17)
fig,ax=plt.subplots(figsize=(8,3))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.bar(x, temp[0], bar_width, align="center",color=['#1f77b4'])
plt.bar(x+bar_width*1, temp[2], bar_width, align="center",color=['#ff7f0e'])
plt.bar(x+bar_width*2, temp[1], bar_width, align="center",color=['#7f7f7f'])
plt.bar(x+bar_width*3, temp[3], bar_width, align="center",color=['#2ca02c'])
# plt.legend(['Predicted','Uniform','ER'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
# plt.legend(['Predicted','Uniform','Same density','ER'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([0,1,2,3,4,5,6,7,8,9],['1','10','1e2','1e3','1e4','1e5','1e6','1e7','1e8','1e9'],size=14,fontproperties='Calibri',weight='bold')
# plt.xlabel('States',fontsize=22,fontproperties='Calibri',weight='bold')
plt.ylabel('Number',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
# plt.savefig('traid census 1.png', dpi=300)
'''



## Triad census distribution

temp=[[],[],[],[],[],[]]
for x in g.triad_census():
    temp[0].append(x)
for x in g_de.triad_census():
    temp[1].append(x)
for x in g_da.triad_census():
    temp[2].append(x)
for x in g_er.triad_census():
    temp[3].append(x)
for x in g_ws.triad_census():
    temp[4].append(x)
for x in g_ba.triad_census():
    temp[5].append(x)
for i in range(0,len(temp[0])):
    temp[1][i]=temp[1][i]/temp[0][i]
    temp[2][i]=temp[2][i]/temp[0][i]
    temp[3][i]=temp[3][i]/temp[0][i]
    temp[4][i]=temp[4][i]/temp[0][i]
    temp[5][i]=temp[5][i]/temp[0][i]

def RatioChange(x):
    if x>=1:
        y=np.log10(x)
    elif x!=0:
        y=-np.log10(1/x)-0.25
    elif x<0.01:
        y=-0.25
    else:
        y=x-0.25
    return y

for i in range(len(temp)):
    for j in range(len(temp[i])):
        temp[i][j]=RatioChange(temp[i][j])

plt.close()
bar_width = 0.19
x=np.arange(1,17)
fig,ax=plt.subplots(figsize=(8,3))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.bar(x, temp[1], bar_width, align="center",color=['#ff7f0e'])
plt.bar(x+bar_width, temp[2], bar_width, align="center",color=['#7f7f7f'])
plt.bar(x+bar_width*2, temp[3], bar_width, align="center",color=['#2ca02c'])
plt.bar(x+bar_width*3, temp[4], bar_width, align="center",color=['#d62728'])
plt.bar(x+bar_width*4, temp[5], bar_width, align="center",color=['#9467bd'])
# plt.legend(['Uniform/Predicted','ER/Predicted','Small world/Predicted','Scale-Free/Predicted'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
# plt.legend(['Uniform/Predicted','Same density/Predicted','ER/Predicted','Small world/Predicted','Scale-Free/Predicted'],prop={'family':'Calibri','weight':'bold','size':22},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)

# plt.ylim([0,9])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],size=14,fontproperties='Calibri',weight='bold')
plt.yticks([-2.25,-1.25,-0.25,0,1],['0.01','0.1','0','1','10'],size=14,fontproperties='Calibri',weight='bold')
# plt.xlabel('States',fontsize=22,fontproperties='Calibri',weight='bold')
plt.ylabel('Times',fontsize=22,fontproperties='Calibri',weight='bold')
plt.tight_layout()
plt.savefig('traid census.png', dpi=300)
'''
'''
'''
## Triad census distribution network compare
bar_width = 0.3
temp=[[],[],[],[],[],[]]
for x in g.triad_census():
    temp[0].append(x)
for x in g_da.triad_census():
    temp[1].append(x)
for x in g_de.triad_census():
    temp[2].append(x)
for i in range(0,len(temp[0])):
    temp[1][i]=temp[1][i]/temp[0][i]
    temp[2][i]=temp[2][i]/temp[0][i]

plt.close()
x=np.arange(1,17)
plt.bar(x, temp[1], bar_width, align="center")
plt.bar(x+bar_width*1, temp[2], bar_width, align="center")
plt.legend(['uniform bouton for all/experimental bouton','uniform bouton for each/experimental bouton'])
# plt.ylim([0,9])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],fontsize=12)
# plt.yticks([0,1,2,3,4,5,6,7,8],['1','10','1e2','1e3','1e4','1e5','1e6','1e7','1e8'],fontsize=12)
plt.xlabel('States',fontsize=12)
plt.ylabel('Times',fontsize=12)

'''

