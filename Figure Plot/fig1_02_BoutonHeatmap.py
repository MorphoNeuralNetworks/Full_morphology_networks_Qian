## 需要使用CCFv3中的数据进行分析
import os,csv,math
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt 

global step
step=25.0
# 获取神经元所在脑区的信息
with open(r'..\Data\Other_Infomation\Allen_CellType_Detail.csv', 'r', newline='') as csvfile:
    t = csv.reader(csvfile)
    area_data=np.array(list(t))
    csvfile.close()
cell_type=dict()
for root, dirs, files in os.walk(r'..\Data\bouton_swc'):
    for file in files:
        t=file.split('.')[0]
        if '15257_' in t:
            t=t.replace('15257_', '210254_')
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

# # 构建每个neuron的boutonlist
# bouton_list=dict()
# path=r'..\Data\boutondensity'
# count=0
# for root,dirs,files in os.walk(path,topdown=True):
#     for name in files:
#         count+=1
#         if count%50==0:
#             print(count)
#         with open(os.path.join(path,name)) as file_object:
#             contents = file_object.readlines()
#             file_object.close()
#         data=[]
#         for x in contents:
#             t=list(map(float,x.split(' ')))
#             data.append(t)
#         bouton_list[name.split('.')[0]]=data
# np.save('boutondensity_list.npy',bouton_list)

bouton_list=np.load('bouton_list.npy', allow_pickle=True).item()
## 构建soma list
# soma_local=dict()
# path=r'..\Data\bouton_swc'
# count=0
# for root,dirs,files in os.walk(path,topdown=True):
#     for name in files:
#         count+=1
#         if count%50==0:
#             print(count)
#         with open(os.path.join(path,name)) as file_object:
#             contents = file_object.readlines()
#             file_object.close()
#         data=[]
#         for x in contents:
#             if x[0]=='#':
#                 continue            
#             t=list(map(float,x.split(' ')))
#             if t[6]==-1:
#                 soma_local[name.split('.')[0]]=t[2:5]
#                 break
# np.save('soma_location.npy',soma_local)      

soma_local=np.load('soma_location.npy', allow_pickle=True).item()
namelist=['VPM','CP','VPL','SSp-m','LGd','SSs','MOp','SSp-bfd','MG','MOs','RT','VISp','CLA','SSp-ul','SSp-n','RSPv','AId','all']

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import nrrd

data_path=r'./average_template_25_u8_xpad.v3draw.nrrd'
global CCFv3_model
CCFv3_model,options=nrrd.read(data_path)  # 读入 nrrd 文件
ccf=CCFv3_model.astype(np.float64)
ccf=np.mean(ccf,1)
plt.close('all')
fig=plt.figure(figsize=(5,5),dpi=300)
fig_ax=plt.subplot(111)
plt.imshow(ccf,cmap="Greys",alpha=0.8)
for name in namelist[16:17]:
    bouton_data=[]
    name_list=[]
    for key in bouton_list:
        if cell_type[key]==name or name=='all':
            name_list.append(key)
            temp=bouton_list[key]
            bouton_data.extend(temp)
temp=np.array(temp)
ana_show_boutons=temp[:,[0,2]]/25

# plt.ylim([0,nmt.annotation.array.shape[2]])
plt.scatter(x=ana_show_boutons[:,0],y=ana_show_boutons[:,1],s=1,marker='o')
plt.axis('off')
plt.xlabel('')
plt.ylabel('')
plt.legend("")

'''
# 全脑的点云
for name in namelist[17:18]:
    contents=['##n,orderinfo,name,comment,z,x,y, pixmax,intensity,sdev,volsize,mass,,,, color_r,color_g,color_b'+'\n']
    soma_con=['##n,orderinfo,name,comment,z,x,y, pixmax,intensity,sdev,volsize,mass,,,, color_r,color_g,color_b'+'\n']
    ## 直接标为红色生成文件
    count=1
    count_s=1
    bouton_data=[]
    name_list=[]
    for key in bouton_list:
        if cell_type[key]==name or name=='all':
            name_list.append(key)
            temp=bouton_list[key]
            soma_id=soma_local[key]
            t=str(count_s)+',,,,'+str(soma_id[2]/25.0)+','+str(soma_id[0]/25.0)+','+str(soma_id[1]/25.0)+',0.000,0.000,0.000,70,0.000,,,,0,0,255'+'\n'
            soma_con.append(t)
            count_s+=1
            bouton_data.extend(temp)
            for x in temp:
                t=str(count)+',,,,'+str(x[2]/25.0)+','+str(x[0]/25.0)+','+str(x[1]/25.0)+',0.000,0.000,0.000,0.1,0.000,,,,255,0,0'+'\n'
                contents.append(t)
                count+=1
    f=open('./heatmap/'+name+'_bouton.apo',"w+",newline='')
    f.writelines(contents)
    f.close()
    
    f=open('./heatmap/'+name+'_soma.apo',"w+",newline='')
    f.writelines(soma_con)
    f.close()
    
    bouton_data=np.array(bouton_data)
    
    methods=['x-y','x-z','y-z']
    for method in methods:
        plt.close('all')
        if method=='x-y':
            min_y=math.floor(min(bouton_data[:,1])/step)
            min_x=math.floor(min(bouton_data[:,0])/step)
            rows=math.ceil(max(bouton_data[:,1])/step)-min_y
            cols=math.ceil(max(bouton_data[:,0])/step)-min_x
            heatmap=np.zeros((rows+1,cols+1))
            for x in bouton_data:
                heatmap[math.ceil(x[1]/step)-min_y,math.ceil(x[0]/step)-min_x]+=1 
        elif method=='x-z':
            min_x=math.floor(min(bouton_data[:,0])/step)
            min_z=math.floor(min(bouton_data[:,2])/step)
            rows=math.ceil(max(bouton_data[:,0])/step)-min_x
            cols=math.ceil(max(bouton_data[:,2])/step)-min_z
            heatmap=np.zeros((rows+1,cols+1))
            for x in bouton_data:
                heatmap[math.ceil(x[0]/step)-min_x,math.ceil(x[2]/step)-min_z]+=1
        elif method=='y-z':
            min_y=math.floor(min(bouton_data[:,1])/step)
            min_z=math.floor(min(bouton_data[:,2])/step)
            rows=math.ceil(max(bouton_data[:,1])/step)-min_y
            cols=math.ceil(max(bouton_data[:,2])/step)-min_z
            heatmap=np.zeros((rows+1,cols+1))
            for x in bouton_data:
                heatmap[math.ceil(x[1]/step)-min_y,math.ceil(x[2]/step)-min_z]+=1
        plt.figure(figsize=(cols/50, rows/50))
        pic=sns.heatmap(data=heatmap,cbar=False,xticklabels=False,yticklabels=False,cmap=plt.get_cmap('OrRd'))
        plt.tight_layout()
        if method=='y-z':
            pic.invert_xaxis()
        # plt.savefig('./heatmap/'+name+'_'+method+'.png',dpi=300)
# plt.subplot(1,2,1)
# for i in range(0,len(new_data)):
#     if new_data[i,0]==0 or new_data[i,-1]==-1:
#         continue
#     t1=new_data[i]
#     t2=new_data[int(t1[-1])-1]
#     if t1[1]==3 or t1[1]==4:
#         plt.plot([t1[2],t2[2]],[t1[3],t2[3]],c='b',linewidth=0.6,alpha=0.6)
#     elif t1[1]==2:
#         plt.plot([t1[2],t2[2]],[t1[3],t2[3]],c='k',linewidth=0.6,alpha=0.6)
# plt.scatter(bouton_list[:,0],bouton_list[:,1],c='r',s=1)

# plt.subplot(1,2,2)
# sns.kdeplot(data=bouton_list,x=bouton_list[:,0],y=bouton_list[:,1],gridsize=200,fill=True)
'''
