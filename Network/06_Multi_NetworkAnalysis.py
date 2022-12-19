import numpy as np
import csv,os,random
import matplotlib.pyplot as plt
import BasicFunction as BF
import igraph as ig
import cairo
import cv2
import math


def NetworkFeature(path,method):
    connectmap=np.load(path,allow_pickle=True)
    data=connectmap[:,3].astype(np.float64)

    # 对连接强度的简单统计
    # print(max(data))
    t=np.where(data<0)
    connect_map = np.delete(connectmap,t,0)
    
    ## igraph 画图
    g = ig.Graph(directed=True)
    node_list=[]
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
    
    g.add_vertices(node_list)
    g.add_edges(edge_list)
    g.es['weight']=edge_weight
    g.es['width']=edge_width
    g.es['arrow_size']=1
    
    g.vs['size']=15
    g.vs['label_size']=5
    
    
    ## 网络分析
    degree_dis=g.degree_distribution()
    x=np.array(range(int(degree_dis._min)+1,int(degree_dis._max)+1))
    y=[]
    for t in degree_dis._bins:
        y.append(t+1)
    x=np.log10(x)
    y=np.log10(y)
    
    triad_census=[np.log(int(i)+1) for i in g.triad_census()]
    dyad_census=[np.log(int(i)+1) for i in g.dyad_census()]
    result=[[len(node_list),len(edge_list)],x.tolist(),y.tolist(),triad_census,dyad_census]
    np.save('normal_'+method+'.npy',np.array(result,dtype=list))

    
par=[(r'D:/QPH/BrainNetwork/bouton_connection.npy','bouton'),
     # ('D:/QPH/BrainNetwork/boutondensity_all_connection.npy','boutondensity_all'),
     ('D:/QPH/BrainNetwork/boutondensity_each_connection.npy','boutondensity_each')]
for x in par:
    NetworkFeature(x[0],x[1])



