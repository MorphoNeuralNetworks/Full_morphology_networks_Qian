import os,csv,math,shutil
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from sklearn.decomposition import PCA
from sklearn import manifold
from sklearn.cluster import KMeans
import matplotlib.mlab as mlab
from scipy.stats import norm
from scipy.optimize import curve_fit
import seaborn as sns 
from scipy.spatial.distance import pdist,cdist
from scipy.spatial.distance import squareform

import random
def randomcolor():
    colorArr=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color=""
    for i in range(6):
        color+=colorArr[random.randint(0,14)]
    return '#'+color

def Init_Data(data):
    # 标准化归一化
    X = data.astype(np.float64)
    # for i in range(0,17):# z-score
    #     X[:,i]=(X[:,i]-np.mean(X[:,i]))/np.std(X[:,i])
    for i in range(0,17):# 最小最大值归一化
        X[:,i]=(X[:,i]-np.min(X[:,i]))/(np.max(X[:,i])-np.min(X[:,i]))
    return X

feature_name=[
'Number of Stems','Number of Bifurcatons','Number of Branches',
'Number of Tips','Overall Width','Overall Height','Overall Depth',
'Total Length','Total Volume','Max Euclidean Distance',
'Max Path Distance','Max Branch Order','Average Contraction',
'Average Parent-daughter Ratio','Average Bifurcation Angle Local',
'Average Bifurcation Angle Remote','Hausdorff Dimension']

## 统计每种celltype的神经元数量
with open('Feature_Total.csv')as f:
    feature_data = list(csv.reader(f))
    del feature_data[0]
    f.close()
    data=np.array(feature_data)
    data=data[:,[0,1,10,11,12,13,14,15,16,18,20,21,22,23,24,26,27,28,29]]
soma_list=data[:,0]
feature_list=data[:,2:]
feature_data=Init_Data(feature_list)

from scipy.cluster.hierarchy import linkage, dendrogram

mergings=linkage(feature_data)
# dendrogram(mergings[0:51],leaf_rotation=0,leaf_font_size=10)
# plt.show()

id_list=dict()
base=len(feature_data)
count=0
for i in range(200):
    temp=[]
    if mergings[i,0]>=base and mergings[i,1]>=base:
        if len(id_list[mergings[i,0]])>=len(id_list[mergings[i,1]]):
            temp.extend(id_list[mergings[i,0]])
            temp.extend(id_list[mergings[i,1]])
        else:
            temp.extend(id_list[mergings[i,1]])
            temp.extend(id_list[mergings[i,0]])
    elif mergings[i,0]>=base and mergings[i,1]<base:
        temp.extend(id_list[mergings[i,0]])
        temp.append(mergings[i,1])
    elif mergings[i,0]<base and mergings[i,1]>=base:
        temp.extend(id_list[mergings[i,1]])
        temp.append(mergings[i,0])
    elif mergings[i,0]<base and mergings[i,1]<base:
        temp.append(mergings[i,0])
        temp.append(mergings[i,1])
    id_list[base+count]=temp
    count+=1
# tt=list(map(int,id_list[1850]))
# tt=list(map(int,id_list[1854]))
# tt=list(map(int,id_list[1855]))
tt=list(map(int,id_list[1861]))
# tt=list(map(int,id_list[1862]))
# tt=list(map(int,id_list[1885]))
# tt=list(map(int,id_list[1903]))
temp_data=data[tt,:] 

np.save('neruon_order.npy',data[tt,0])

folder="./similar_neuron/"
path='D:/QPH/Data/bouton_swc/'
if os.path.exists(folder):
    shutil.rmtree(folder)
os.mkdir(folder)

for x in temp_data:
    shutil.copyfile(path+x[0]+'.swc', folder+x[0]+'.swc')
    
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
for root,dirs,files in os.walk(folder):
    for f in files:
        name=f.split('.')[0]
        print(cell_type[name])

import nrrd,json
## 选择的区域
with open(r'..\Data\Other_Infomation\Selected_Regions.csv', 'r', newline='',encoding='utf8') as csvfile:
    t = csv.reader(csvfile)
    t=list(t)
    select_region=[x[2] for x in t[1:]]
    csvfile.close()

## 构建CCFv3结构
with open(r'..\Data\Other_Infomation\tree.json','r',encoding='utf_8_sig')as fp:
    json_data = json.load(fp)
    fp.close()
Celltype2Id={x['acronym']:x['id'] for x in json_data}
Id2Celltype={Celltype2Id[key]:key for key in Celltype2Id.keys()}

Celltype2Select=dict()
for x in json_data:
    mark=0
    for k in select_region:
        if Celltype2Id[k] in x['structure_id_path']:
            Celltype2Select[x['acronym']]=k
            mark=1
            break
    if mark==0:
        Celltype2Select[x['acronym']]=x['acronym']

##指定目录读取文件获得soma位置
outpath="./Bouton_Stat/"
if os.path.exists(outpath):
    shutil.rmtree(outpath)
os.mkdir(outpath)

data_path=r'../Data/annotation_25.nrrd'
CCFv3_model,options=nrrd.read(data_path)  # 读入 nrrd 文件
for root,dirs,files in os.walk(folder,topdown=True):
    for file in files:
        name=file.split('.')[0]
        bouton_list=[]
        with open(os.path.join('../Data/bouton',file)) as file_object:
            contents = file_object.readlines()
            file_object.close()
        for lineid in range(0,len(contents)):
            x=contents[lineid]
            x=x.strip("\n")
            t1=x.split( )
            t1=list(map(float,t1))
            if round(t1[0]/25)>=528 or round(t1[1]/25)>=320 or round(t1[2]/25)>=456:
                continue
            t=CCFv3_model[round(t1[0]/25),round(t1[1]/25),round(t1[2]/25)]
            if t==0:
                continue
            else:
                t=Id2Celltype[t]
                t=Celltype2Select[t]
                bouton_list.append(t)
        bouton_dict={x:0 for x in list(set(bouton_list))}
        for x in bouton_list: bouton_dict[x]+=1
        np.save(outpath+name+'_bouton.npy',bouton_dict)
def dist(A,B):
    temp=0
    for i in range(0,len(A)):
        temp+=(A[i]-B[i])*(A[i]-B[i])
    return math.sqrt(temp)

for root,dirs,files in os.walk(folder,topdown=True):
    for file in files:
        name=file.split('.')[0]
        axon_list=[]
        with open(os.path.join('../Data/bouton_swc',file)) as file_object:
            contents = file_object.readlines()
            file_object.close()
        for lineid in range(0,len(contents)):
            x=contents[lineid]
            x=x.strip("\n")
            t1=x.split( )
            t1=list(map(float,t1))
            if t1[0]==0:
                continue
            if t1[1]==2 or t1[1]==5:
                if round(t1[2]/25)>=528 or round(t1[3]/25)>=320 or round(t1[4]/25)>=456:
                    continue
                t=CCFv3_model[round(t1[2]/25),round(t1[3]/25),round(t1[4]/25)]
                if t==0:
                    continue
                else:
                    t2=contents[int(t1[6])-1]
                    t2=t2.strip("\n")
                    t2=t2.split( )
                    t2=list(map(float,t2))
                    length=dist(t1[2:5],t2[2:5])
                    t=Id2Celltype[t]
                    t=Celltype2Select[t]
                    axon_list.append((t,length))
        temp=[x[0] for x in axon_list]
        axon_dict={x:0 for x in list(set(temp))}
        for x in axon_list: axon_dict[x[0]]+=x[1]
        np.save(outpath+name+'_axon.npy',axon_dict)




