import numpy as np
import csv,os,random
import matplotlib.pyplot as plt
import BasicFunction as BF
import igraph as ig
import cairo
import cv2
import math

def NetworkFeature(folder):
    connectmap=np.load('.\\Pertubation_Result\\'+folder+'_Bouton.npy',allow_pickle=True)
    data=connectmap[:,3].astype(np.float64)

    # 对连接强度的简单统计
    # print(max(data))
    t=np.where(data<0)
    connect_map = np.delete(connectmap,t,0)
    # plt.hist(data,bins=19)

    # 匹配soma坐标文件和对应的脑区
    soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
    soma_list=[]
    path=r'.\\Pertubation\\'+folder
    for root, dirs, files in os.walk(path):
        for f in files: soma_list.append(f.split('.')[0])

    ## igraph 画图
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

    node_local=[]
    node_area=[]

    area_color = np.load('../Data/Other_Infomation/color_network.npy', allow_pickle=True).item()
    area_count=dict()
    for x in node_list:
        if 'empty point' in x:
            continue
        node_local.append((np.floor(soma_info[x][1][0]),np.floor(soma_info[x][1][2])))
        node_area.append(soma_info[x][0])
        if soma_info[x][0] not in area_count.keys():
            area_count[soma_info[x][0]]=0
        node_color.append(area_color[soma_info[x][0]])
        area_count[soma_info[x][0]]+=1
    
    g.add_vertices(node_list)
    g.add_edges(edge_list)
    g.es['weight']=edge_weight
    g.es['width']=edge_width
    g.es['arrow_size']=1
    
    g.vs['color'] = node_color
    g.vs['label'] = node_list
    g.vs['size']=15
    g.vs['label_size']=5
    
    # layout=g.layout("fr")
    layout=node_local
    out=ig.plot(g,layout=layout,bbox = (2000, 1600))
    out.save('.\\graph\\'+folder+'_bouton.png')
    
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
    np.save('.\\graph_feature\\'+folder+'_bouton.npy',np.array(result,dtype=list))

    # 生成.dat文件
    contents=[str(len(node_list))+'\n']
    for x in connect_map:
        t1=node_list.index(x[0])
        t2=node_list.index(x[1])
        # w_t=round(x[3])
        w_t=x[3]
        if w_t!=0:
            contents.append(str(t1)+' '+str(t2)+' '+str(w_t)+'\n')
    f=open('.\\graph_feature\\'+folder+'_bouton.dat','w+')
    f.writelines(contents)
    f.close()
    
def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 36
    
    folderpath = os.listdir(r'.\Pertubation')
    
    import time
    time_start = time.time()  # 记录开始时间
    with Pool(cpu_worker_num) as p:
        p.map(NetworkFeature, folderpath)
    # NetworkFeature('normal')
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Network Feature time: '+str(time_sum))  

if __name__ =='__main__':
    if not os.path.exists('./Pertubation_Result'):
        os.mkdir('./Pertubation_Result')
    run__pool()
    


