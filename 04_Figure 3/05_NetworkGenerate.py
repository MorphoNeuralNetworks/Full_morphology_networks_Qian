'''
Visualizing the network
'''
import numpy as np
import os
method='bouton'
# method='boutondensity_each'
# method='boutondensity_all' # choose from three networks

connectmap=np.load(method+'_connection.npy',allow_pickle=True)
data=connectmap[:,3].astype(np.float64)
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)

soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()

## draw with igraph
import igraph as ig
import cairo
import cv2

g = ig.Graph(directed=True)
node_list=[]
node_color=[]
edge_list=[]
edge_weight=[]
edge_width=[]

for x in connect_map:
    if x[0] not in node_list:
        node_list.append(x[0])
    if x[1] not in node_list:
        node_list.append(x[1])
    edge_list.append((x[0],x[1]))
    edge_weight.append(x[3])
    edge_width.append(np.log(x[3]))

# node_list.append('empty point_up')
# node_list.append('empty point_down')

node_local_1=[]
node_local_2=[]
node_local_3=[]
node_area=[]
# area_color=dict()
area_color=np.load(r'..\Data\Other_Infomation\color_network.npy', allow_pickle=True).item()
area_count=dict()
for x in node_list:
    if 'empty point' in x:
        continue
    node_local_1.append((np.floor(soma_info[x][1][0]),np.floor(soma_info[x][1][1])))
    node_local_2.append((np.floor(soma_info[x][1][0]),np.floor(soma_info[x][1][2])))
    node_local_3.append((np.floor(soma_info[x][1][2]),np.floor(soma_info[x][1][1])))
    node_area.append(soma_info[x][0])
    if soma_info[x][0] not in area_count.keys():
        area_count[soma_info[x][0]]=0
    node_color.append(area_color[soma_info[x][0]])
    area_count[soma_info[x][0]]+=1
# node_local_1.append((0,0))
# node_local_1.append((528*25,320*25))

g.add_vertices(node_list)
g.add_edges(edge_list)
g.es['weight']=edge_weight
g.es['width']=edge_width
g.es['arrow_size']=1

g.vs['color'] = node_color
g.vs['label'] = node_list
g.vs['size']=15
g.vs['label_size']=5

print(ig.summary(g))
# # 528 320 456
out=ig.plot(g,layout=node_local_1,bbox = (528*4, 320*4))
out.save('Network_'+method+'_1.png')
out=ig.plot(g,layout=node_local_2,bbox = (528*4, 456*4))
out.save('Network_'+method+'_2.png')
out=ig.plot(g,layout=node_local_3,bbox = (456*4, 320*4))
out.save('Network_'+method+'_3.png')

## generate .dat files
contents=[str(len(node_list))+'\n']
for x in connect_map:
    t1=node_list.index(x[0])
    t2=node_list.index(x[1])
    # w_t=round(x[3])
    w_t=x[3]
    if w_t!=0:
        contents.append(str(t1)+' '+str(t2)+' '+str(w_t)+'\n')
f=open('network_'+method+'.dat','w+')
f.writelines(contents)
f.close()
