import numpy as np
import os,csv
import leidenalg
import matplotlib.pyplot as plt

# method='bouton'
# method='boutondensity_each'
method='boutondensity_all'
connectmap=np.load(method+'_connection.npy',allow_pickle=True)

data=connectmap[:,3].astype(np.float64)

# 对连接强度的简单统计
# print(max(data))
t=np.where(data<0)
connect_map = np.delete(connectmap,t,0)
# plt.hist(data,bins=19)


# 匹配soma坐标文件和对应的脑区
soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
soma_list=[]
path='../Data/'+method+'_swc'
for root, dirs, files in os.walk(path):
    for f in files: soma_list.append(f.split('.')[0])
    
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

area_color=np.load(r'..\Data\Other_Infomation\color_network.npy', allow_pickle=True).item()

import nrrd
data_path=r'../Data/average_template_25_u8_xpad.v3draw.nrrd'
CCFv3_model,options=nrrd.read(data_path)  # 读入 nrrd 文件
pic=np.mean(CCFv3_model,1)
pic=pic[20:-20,:]
pic=pic*(255/np.max(pic))
plt.close('all')
plt.figure(figsize=(5.28,4.56))
plt.imshow(pic.T,cmap="Greys")
plt.xticks([])  # 去掉x轴
plt.yticks([])  # 去掉y轴
plt.axis('off')  # 去掉坐标轴
plt.tight_layout()
# plt.savefig('background.png', dpi=300)
# k.set_xticks([])


import igraph as ig
import cairo
import cv2
import math

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

# node_list.append('empty point_up')
# node_list.append('empty point_down')

area_color=np.load(r'..\Data\Other_Infomation\color_network.npy', allow_pickle=True).item()
node_local_1=[]
node_local_2=[]
node_local_3=[]
node_color=[]
for x in node_list:
    if 'empty point' in x:
        continue
    node_local_1.append((np.floor(soma_info[x][1][0]),np.floor(soma_info[x][1][1])))
    node_local_2.append((np.floor(soma_info[x][1][0]),np.floor(soma_info[x][1][2])))
    node_local_3.append((np.floor(soma_info[x][1][2]),np.floor(soma_info[x][1][1])))
    node_color.append(area_color[soma_info[x][0]])
# node_local.append((0,0))
# node_local.append((456*25,528*25))

node_type=[cell_type[x] for x in node_list]
g.add_vertices(node_list)
g.add_edges(edge_list)
g.es['weight']=edge_weight
record_1=dict()
record_2=dict()
'''
for tt in range(1):
    # seed=random.randint(1,999999999)
    seed=2022
    res=leidenalg.find_partition(g,leidenalg.ModularityVertexPartition,weights=g.es['weight'],seed=seed)
    # res=g.community_edge_betweenness(directed=True, weights=g.es['weight'])
    # print(res.subgraphs)
    res_t=np.array({'node_list':node_list,'res':list(res)},dtype=dict)
    np.save(method+'_leiden.npy',res_t)
    
    g_t=g
    
    new_color_dic=np.load(r'..\Data\Other_Infomation\leiden_color.npy', allow_pickle=True).item()
    # new_color=['']*len(node_list)
    # for i in range(0,len(res)):
    #     temp=res[i]
    #     for j in temp:
    #         new_color[j]=new_color_dic[i]
    # g_t.vs['color'] = new_color
    # out=ig.plot(g_t,layout=node_local_2,bbox = (528*4, 456*4))
    # out.save('leiden_'+method+'.png')
    

    #获得每个分类下神经元的基本信息
    class_dic=dict()
    for i in range(0,len(res)):
        class_dic[i]=[]
    for i in range(0,len(res)):
        t=res[i]
        for j in t:
            class_dic[i].append([node_list[j],node_type[j]])
    
    #查看某一类内中包含了多少脑区，分别的数量
    for i in range(0,3):
        t=class_dic[i]
        if len(t)>30:
            # print("class "+str(i)+" size="+str(len(t)))
            list_t=[]
            for x in t:
                list_t.append(x[1])
            set_t=set(list_t)
            dict_t={}
            for item in set_t:
                dict_t.update({item:list_t.count(item)})
            y1 = {k: v for k, v in sorted(dict_t.items(), key=lambda item: item[1], reverse=True)}
            keys=list(y1.keys())
            # for k in keys[0:2]:
            #     print(f"{k}:{y1[k]}")
            # print('-------------------')
            t1=keys[0]+str(y1[keys[0]])+'_'+keys[1]+str(y1[keys[1]])
            t2=keys[0]+'_'+keys[1]
            if t1 not in record_1:
                record_1[t1]=1
            else:
                record_1[t1]+=1
            if t2 not in record_2:
                record_2[t2]=1
            else:
                record_2[t2]+=1

        plt.close()
        fig,ax=plt.subplots(figsize=(6,4))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        x=range(0,10)
        y=[y1[k] for k in keys[0:10]]
        # count=0
        # for k in keys[0:10]: count+=y1[k]
        # y.append(len(t)-count)
        c_t=[area_color[k] for k in keys[0:10]]
        # c_t.append('#000000')
        label=keys[0:10]
        # label.append('Others')
        plt.bar(x,y,color=c_t)
        if i==0:
            plt.ylabel('Number of neurons',fontsize=22,fontproperties='Calibri',weight='bold')
        plt.xticks(range(0,10),label,fontsize=15,fontproperties='Calibri',weight='bold')
        plt.yticks(fontsize=15,fontproperties='Calibri',weight='bold')
        plt.tight_layout()
        plt.savefig('./Temp/'+method+'_cluster_'+str(i+1)+'_comp.jpg',dpi=300)
            

        g_t = ig.Graph(directed=True)
        g_t.add_vertices(node_list+['empty point_up','empty point_down'])
        g_t.add_edges(edge_list)
        g_t.es['width']=edge_width
        g_t.es['arrow_size']=1


        g_t.vs['color'] = node_color+["#FFFFFF","#FFFFFF"]
        g_t.vs['label'] = node_list
        g_t.vs['location']=node_local_2+[(0,0),(528*25,456*25)]
        g_t.vs['size']=15
        g_t.vs['label_size']=5
        ig.summary(g_t)
        t_l={x[0]:'0' for x in t}
        delete_list=[]
        # for i in range(0,len(g_t.vs['label']):
        for x in g_t.vs['label']:
            if x not in t_l.keys() or 'empty point' in x:
                delete_list.append(x)
        g_t.delete_vertices(delete_list)
        ig.summary(g_t)
        out=ig.plot(g_t,layout=g_t.vs['location'],bbox = (528*2.5,456*2.5))
        out.save('./Temp/'+method+'_leiden_cluster_'+str(i+1)+'.png')
        
        img1=cv2.imread('background.png')
        img2=cv2.imread('./Temp/'+method+'_leiden_cluster_'+str(i+1)+'.png')
        res = cv2.addWeighted(cv2.resize(img1,(528,456)), 0.35, cv2.resize(img2,(528,456)), 0.65, 0)
        # # 保存
        cv2.imencode('.png', res)[1].tofile('./Temp/'+method+'_leiden_cluster_'+str(i+1)+'_brain.png')
        # cv2.imshow('input_image', res)
        # cv2.waitKey(0)
'''