import numpy as np
import csv,os,random
import matplotlib.pyplot as plt
import BasicFunction as BF

import igraph as ig
import cairo
import cv2
import math

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

# connectmap=np.load('bouton_connection.npy',allow_pickle=True)
connectmap=np.load('boutondensity_each_connection.npy',allow_pickle=True)

data=[[cell_type[x[0]],cell_type[x[1]],x[3]] for x in connectmap]
data=np.array(data)
node_list=list(set(data[:,0].tolist()+data[:,1].tolist()))
edge_list=[(str(x[0]),str(x[1])) for x in data]
edge_list=list(set(edge_list))
weight_dict=dict()
for x in data:
    if (str(x[0]),str(x[1])) not in weight_dict.keys():
        weight_dict[(str(x[0]),str(x[1]))]=float(x[2])
    else:
        weight_dict[(str(x[0]),str(x[1]))]+=float(x[2])
edge_weight=[weight_dict[x] for x in edge_list]
edge_width=[np.log(weight_dict[x]+1)/3 for x in edge_list]

area_color=np.load(r'..\Data\Other_Infomation\color_network.npy', allow_pickle=True).item()
node_color=[area_color[x] for x in node_list]
edge_color=[area_color[x[0]] for x in edge_list]

g = ig.Graph(directed=True)
g.add_vertices(node_list)
g.add_edges(edge_list)
g.es['weight']=edge_weight
g.es['width']=edge_width
g.es['arrow_size']=0.1
g.es['color']=edge_color

g.vs['color'] = node_color
g.vs['label'] = node_list
g.vs['size']=30
g.vs['label_size']=30

# out=ig.plot(g,layout='circle',bbox = (1600, 1600))
# out.save('Network.png')


## rich club coefficient
def RichClubCoefficient(g):
    d_t=g.degree()
    node_temp=[[i,d_t[i]] for i in range(len(d_t))]
    node_temp=np.array(node_temp)
    node_temp=node_temp[np.argsort(-node_temp[:,1])]
    res={}
    for k in range(2,round(len(d_t)/4)):
        node_compare=node_temp[0:k,0]
        count=0
        for i in range(0,k):
            for j in range(i+1,k):
                if g.are_connected(i,j):
                    count+=1
        coe=2*count/(k*(k-1))
        res[k]=coe
    return res
RichClubCoe=RichClubCoefficient(g)
x=list(RichClubCoe.keys())
x=x[0:50]
y=[RichClubCoe[i] for i in x]
plt.plot(x,y)

## hubs and authorities
authority_score=g.authority_score(weights=g.es['weight'])
hub_score=g.hub_score(weights=g.es['weight'])
print('-----hub_score-----')
for x in range(0,len(hub_score)):
    if hub_score[x]> 0.1:
        print([g.vs['label'][x],hub_score[x]])
print('authority_score-----')
for x in range(0,len(authority_score)):
    if authority_score[x] > 0.1:
        print([g.vs['label'][x],authority_score[x]])
        
## hubs and authorities
# authority_score=g_da.authority_score(weights=g_da.es['weight'])
# hub_score=g_da.hub_score(weights=g_da.es['weight'])
# print('-----hub_score-----')
# for x in range(0,len(hub_score)):
#     if hub_score[x]> 0.01:
#         print([g_da.vs['label'][x],hub_score[x],cell_type[g_da.vs['label'][x]]])
# print('authority_score-----')
# for x in range(0,len(authority_score)):
#     if authority_score[x] > 0.01:
#         print([g_da.vs['label'][x],authority_score[x],cell_type[g_da.vs['label'][x]]])

