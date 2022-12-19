## 按照顺序生成bouton文件+axon文件
import os,math,csv,nrrd,json
import numpy as np
import matplotlib.pyplot as plt 
import shutil

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

neuron_list=np.load('neruon_order.npy',allow_pickle=True)
files=[str(x)+'.swc' for x in neuron_list]
'''
outpath="./Correlation/"
if os.path.exists(outpath):
    shutil.rmtree(outpath)
os.mkdir(outpath)

folder="./similar_neuron/"
data_path=r'../Data/annotation_25.nrrd'
CCFv3_model,options=nrrd.read(data_path)  # 读入 nrrd 文件
for root,dirs,files in os.walk(folder,topdown=True):
    count=1
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
                t1.append(t)
                bouton_list.append(t1)
        np.save(outpath+str(count)+'_bouton.npy',bouton_list)
        count+=1

for root,dirs,files in os.walk(folder,topdown=True):
    count=1
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
                    t=Id2Celltype[t]
                    t=Celltype2Select[t]
                    tt=t1[2:5]
                    tt.append(t)
                    axon_list.append(tt)
        np.save(outpath+str(count)+'_axon.npy',np.array(axon_list,dtype=list))
        count+=1
'''
import random
from scipy.stats import pearsonr
from sklearn.cross_decomposition import CCA
import seaborn as sns
c_m=np.ones((len(neuron_list),len(neuron_list)))
p_m=np.ones((len(neuron_list),len(neuron_list)))
folder="./Correlation/"
for i in range(0,len(neuron_list)):
    f1=np.load(folder+str(i+1)+'_axon.npy',allow_pickle=True)
    for j in range(i+1,len(neuron_list)):
        f2=np.load(folder+str(j+1)+'_axon.npy',allow_pickle=True)
        if len(f1)>len(f2):
            random.shuffle(f1)
            f1=f1[0:len(f2)]
        elif len(f1)<len(f2):
            random.shuffle(f2)
            f2=f2[0:len(f1)]
        df1=f1[:,0:3].astype(np.float64)
        df2=f2[:,0:3].astype(np.float64)

        ca = CCA(n_components=1)
        xc,yc = ca.fit(df1, df2).transform(df1, df2)
        xc=np.squeeze(xc)
        yc=np.squeeze(yc)
        c_m[i,j],p_m[i,j]=pearsonr(xc,yc)
        c_m[j,i],p_m[j,i]=c_m[i,j],p_m[i,j]
        
labels=["n"+str(i) for i in range(1,16)]        
plt.close('all')
plt.figure(figsize=(4,4))
pic=sns.heatmap(data=c_m,cbar=True,yticklabels=labels,xticklabels=labels,square=True,vmax=1,
                annot=False, fmt=".0f",linewidths=.5,cmap=plt.get_cmap('OrRd'),
                cbar_kws={'shrink':0.8,'label':"Pearson correlation coefficient"},
                annot_kws={'fontsize':11})
pic.set_xticklabels(labels,fontsize=12,rotation=90)
pic.set_yticklabels(labels,fontsize=12)
cbar = pic.collections[0].colorbar
# here set the labelsize by 20
cbar.ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig('axon.png', dpi=300)



c_m=np.ones((len(neuron_list),len(neuron_list)))
p_m=np.ones((len(neuron_list),len(neuron_list)))
folder="./Correlation/"
for i in range(0,len(neuron_list)):
    f1=np.load(folder+str(i+1)+'_bouton.npy',allow_pickle=True)
    for j in range(i+1,len(neuron_list)):
        f2=np.load(folder+str(j+1)+'_bouton.npy',allow_pickle=True)
        if len(f1)>len(f2):
            random.shuffle(f1)
            f1=f1[0:len(f2)]
        elif len(f1)<len(f2):
            random.shuffle(f2)
            f2=f2[0:len(f1)]
        df1=f1[:,0:3].astype(np.float64)
        df2=f2[:,0:3].astype(np.float64)

        ca = CCA(n_components=1)
        xc,yc = ca.fit(df1, df2).transform(df1, df2)
        xc=np.squeeze(xc)
        yc=np.squeeze(yc)
        c_m[i,j],p_m[i,j]=pearsonr(xc,yc)
        c_m[j,i],p_m[j,i]=c_m[i,j],p_m[i,j]
        
plt.close('all')
plt.figure(figsize=(4,4))
pic=sns.heatmap(data=c_m,cbar=True,yticklabels=labels,xticklabels=labels,square=True,vmax=1,
                annot=False, fmt=".0f",linewidths=.5,cmap=plt.get_cmap('OrRd'),
                cbar_kws={'shrink':0.8,'label':"Pearson correlation coefficient"},
                annot_kws={'fontsize':11})
pic.set_xticklabels(labels,fontsize=12,rotation=90)
pic.set_yticklabels(labels,fontsize=12)
cbar = pic.collections[0].colorbar
# here set the labelsize by 20
cbar.ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig('bouton.png', dpi=300)

