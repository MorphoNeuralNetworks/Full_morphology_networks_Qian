import numpy as np
import csv,os,shutil
import random

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

## 全脑网络的swc文件
'''
contents=[]
count=0
# 528 320 456 264 160 228
# start=[90,120,90]
# end=[421,211,361]
start=[60,60,60]
end=[481,301,421]
for i in range(start[0],end[0],60):
    for j in range(start[1],end[1],60):
        count+=1
        temp=str(count)+' 16 '+str(i)+' '+str(j)+' '+str(start[2])+' 1 -1\n'
        contents.append(temp)
        count+=1
        temp=str(count)+' 16 '+str(i)+' '+str(j)+' '+str(end[2])+' 1 '+str(count-1)+'\n'
        contents.append(temp)

for i in range(start[0],end[0],60):
    for j in range(start[2],end[2],60):
        count+=1
        temp=str(count)+' 16 '+str(i)+' '+str(start[1])+' '+str(j)+' 1 -1\n'
        contents.append(temp)
        count+=1
        temp=str(count)+' 16 '+str(i)+' '+str(end[1])+' '+str(j)+' 1 '+str(count-1)+'\n'
        contents.append(temp)

for i in range(start[1],end[1],60):
    for j in range(start[2],end[2],60):
        count+=1
        temp=str(count)+' 16 '+str(start[0])+' '+str(i)+' '+str(j)+' 1 -1\n'
        contents.append(temp)
        count+=1
        temp=str(count)+' 16 '+str(end[0])+' '+str(i)+' '+str(j)+' 1 '+str(count-1)+'\n'
        contents.append(temp)
f=open('test.swc','w+')
f.writelines(contents)
f.close()
'''

## 画实际神经元的部分
'''
connectmap=np.load('connectmap_bouton.npy', allow_pickle=True)
connectmap = connectmap[np.argsort(connectmap[:,3])[::-1]]

i_t=166
neuron_list=[str(connectmap[i_t,0]),str(connectmap[i_t,1])] # VPM SSp-bfd
print([cell_type[neuron_list[0]],cell_type[neuron_list[1]]])
cube=connectmap[i_t,2]
# #['17302_00040','18453_7188_x11060_y3637'] # LGd VISp
bouton_mark=['##n,orderinfo,name,comment,z,x,y, pixmax,intensity,sdev,volsize,mass,,,, color_r,color_g,color_b'+'\n']
count=1

# 投射神经元
file=neuron_list[0]
data1=[]
if os.path.exists('../Data/bouton_swc/'+file+'.swc'):
    with open(os.path.join('../Data/bouton_swc',file+'.swc')) as file_object:
        contents = file_object.readlines()
        file_object.close()
    for x in contents:
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        data1.append(t1)
    for i in range(len(contents)-1,-1,-1):
        x=contents[i]
        if x[0]=='0':
            del contents[i]
    for x in contents:
        x=x.split(' ')
        if x[1]=='5':
            t=str(count)+',,,,'+x[4]+','+x[2]+','+x[3]+',0.000,0.000,0.000,10,0.000,,,,0,255,0\n'
            bouton_mark.append(t)
            count+=1  
    new_contents=[]
    for x in contents:
        x=x.split(' ')
        t=x[0]+' '+x[1]+' '+str(float(x[2])/25)+' '+str(float(x[3])/25)+' '+str(float(x[4])/25)+' '+x[5]+' '+x[6]
        new_contents.append(t)
    f=open('./figure2/'+file+'.swc','w+')
    f.writelines(contents)
    f.close()
    f=open('./figure2/'+file+'_25x.swc','w+')
    f.writelines(new_contents)
    f.close()
else:
    print(i+' not exist')
    
f=open('./figure2/bouton_mark.apo','w+')
f.writelines(bouton_mark)
f.close() 

# 接收神经元
file=neuron_list[1]

if os.path.exists('../Data/bouton_swc/'+file+'.swc'):
    with open(os.path.join('../Data/bouton_swc',file+'.swc')) as file_object:
        contents = file_object.readlines()
        file_object.close()
    new_contents=[]
    for x in contents:
        x=x.split(' ')
        if x[0]=='0':
            continue
        t=x[0]+' '+x[1]+' '+str(float(x[2])/25)+' '+str(float(x[3])/25)+' '+str(float(x[4])/25)+' '+x[5]+' '+x[6]
        new_contents.append(t)
    f=open('./figure2/'+file+'_25x.swc','w+')
    f.writelines(new_contents)
    f.close()
    f=open('./figure2/'+file+'_origin.swc','w+')
    f.writelines(contents)
    f.close()
    data2=np.zeros((len(contents),8))
    for i in range(0,len(contents)):
        x=contents[i]
        x=x.strip("\n")
        t1=x.split( )
        data2[i,0:7]=np.array(list(map(float,t1)))
    data2[0,7]=1
    for i in range(0,len(contents)):
        if data2[i,1]==3 or data2[i,1]==4:
            t=i
            while data2[t,7]==0:
                data2[t,7]=1
                t=int(data2[t,6])-1
    data2=np.array(data2)
    for i in range(len(contents)-1,-1,-1):
        if data2[i,7]==0:
            del contents[i]
   
    f=open('./figure2/'+file+'.swc','w+')
    f.writelines(contents)
    f.close()
else:
    print(i+' not exist')
    
#根据cube生成一个矩形的swc文件
contents=[]
count=1
step=30
for x in cube:
    local=x.split('_')
    local=list(map(float,local))
    temp=temp=str(count)+' 16 '+str(local[0]*step)+' '+str(local[1]*step)+' '+str(local[2]*step)+' 1 -1\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step+step)+' '+str(local[1]*step)+' '+str(local[2]*step)+' 1 '+str(count-1)+'\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step)+' '+str(local[1]*step+step)+' '+str(local[2]*step)+' 1 '+str(count-2)+'\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step)+' '+str(local[1]*step)+' '+str(local[2]*step+step)+' 1 '+str(count-3)+'\n'
    count+=1
    contents.append(temp)
    
    temp=temp=str(count)+' 16 '+str(local[0]*step+step)+' '+str(local[1]*step+step)+' '+str(local[2]*step)+' 1 '+str(count-3)+'\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step+step)+' '+str(local[1]*step+step)+' '+str(local[2]*step)+' 1 '+str(count-3)+'\n'
    count+=1
    contents.append(temp)
    
    temp=temp=str(count)+' 16 '+str(local[0]*step+step)+' '+str(local[1]*step)+' '+str(local[2]*step+step)+' 1 '+str(count-5)+'\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step+step)+' '+str(local[1]*step)+' '+str(local[2]*step+step)+' 1 '+str(count-4)+'\n'
    count+=1
    contents.append(temp)
    
    temp=temp=str(count)+' 16 '+str(local[0]*step)+' '+str(local[1]*step+step)+' '+str(local[2]*step+step)+' 1 '+str(count-6)+'\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step)+' '+str(local[1]*step+step)+' '+str(local[2]*step+step)+' 1 '+str(count-6)+'\n'
    count+=1
    contents.append(temp)
    
    temp=temp=str(count)+' 16 '+str(local[0]*step+step)+' '+str(local[1]*step+step)+' '+str(local[2]*step+step)+' 1 -1\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step+step)+' '+str(local[1]*step+step)+' '+str(local[2]*step)+' 1 '+str(count-1)+'\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step+step)+' '+str(local[1]*step)+' '+str(local[2]*step+step)+' 1 '+str(count-2)+'\n'
    count+=1
    contents.append(temp)
    temp=temp=str(count)+' 16 '+str(local[0]*step)+' '+str(local[1]*step+step)+' '+str(local[2]*step+step)+' 1 '+str(count-3)+'\n'
    count+=1
    contents.append(temp)
f=open('./figure2/cube.swc','w+')
f.writelines(contents)
f.close()
'''
'''
## 最终生成的热力图
import numpy as np

connnect_map=np.load('D:/QPH/BrainNetwork_Plot/bouton_connection.npy',allow_pickle=True)
connnect_map=connnect_map[:,[0,1,3]]

pre_dic=dict()
pre_list=list(set(connnect_map[:,0].tolist()))
count=0
for x in pre_list:
    pre_dic[x]=count
    count+=1
count=0
post_dic=dict()
post_list=list(set(connnect_map[:,1].tolist()))
for x in post_list:
    post_dic[x]=count
    count+=1
mark=np.zeros((len(pre_dic.keys()),len(post_dic.keys())))
data=np.zeros((len(pre_dic.keys()),len(post_dic.keys())))
pre_list=np.array(pre_list)
post_list=np.array(post_list)
for x in connnect_map:
    i=pre_dic[str(x[0])]
    j=post_dic[str(x[1])]
    data[i,j]=np.log(float(x[2])+1)
    mark[i,j]=1

count=0
for i in range(0,1100):
    count+=1
    if count%50==0:
        print(count)
    temp=np.sum(mark,1)
    t=np.argsort(temp)[::-1]
    data = data[t,:]
    mark = mark[t,:]
    pre_list=pre_list[t]
    # 删除行
    # t=np.where(temp<11)[0]
    data=data[0:-1,:]
    mark=mark[0:-1,:]
    pre_list=pre_list[0:-1]
    
    temp=np.sum(mark,0)
    t=np.argsort(temp)[::-1]
    data = data[:,t]
    mark = mark[:,t]
    post_list=post_list[t]
    # 删除列
    # t=np.where(temp<1)[0]
    data=data[:,0:-1]
    mark=mark[:,0:-1]
    post_list=post_list[0:-1]

pre_region=[cell_type[x] for x in pre_list]
post_region=[cell_type[x] for x in post_list]

pre_region=np.array(pre_region)
post_region=np.array(post_region)


t=np.argsort(pre_region)[::-1]
data=data[t,:]
pre_region=pre_region[t]

t=np.argsort(post_region)[::-1]
data=data[:,t]
post_region=post_region[t]
np.save('temp.npy',[data,pre_region,post_region])
'''


temp=np.load('temp.npy',allow_pickle=True)
data,pre_region,post_region=temp[0],temp[1],temp[2]
# from sklearn.cluster import KMeans
# kmeans = KMeans(n_clusters=9, random_state=0).fit(data)
# labels=kmeans.labels_
# data = data[np.argsort(labels)]

# Cortex
# Thalamus VPM VPL VM VAL
# Striatum CP
# 387 CLA
pre_select=['VPM','VPL','AId','MOp','MOs','SSs','SSp-ul','SSp-n','SSp-m','CP']
pre_dict={str(x):0 for x in set(pre_region)}
for x in pre_region: pre_dict[x]+=1
post_select=['VPM','MOs','MOp','SSs','SSp-ul','SSp-un','SSp-n','SSp-m','SSp-bfd','CP']
post_dict={str(x):0 for x in set(post_region)}
for x in post_region: post_dict[x]+=1

color_dict=np.load("../Data/Other_Infomation/color_network.npy",allow_pickle=True).item()

t=[]
for x in pre_select:
    for i in range(0,len(pre_region)):
        if pre_region[i]==x:
            t.append(i)
data=data[t,:]
pre_region=pre_region[t]

t=[]
for x in post_select:
    for i in range(0,len(post_region)):
        if post_region[i]==x:
            t.append(i)
data=data[:,t]
post_region=post_region[t]


row_color=[color_dict[x] for x in pre_region]
xtick=[str(post_region[0])]
for i in range(1,len(post_region)-1):
    if post_region[i-1]!=post_region[i] or post_region[i+1]!=post_region[i]:
        xtick.append(str(post_region[i]))
    else:
        xtick.append('-')
xtick.append(str(post_region[-1]))

col_color=[color_dict[x] for x in post_region]
ytick=[str(pre_region[0])]
for i in range(1,len(pre_region)-1):
    if pre_region[i-1]!=pre_region[i] or pre_region[i+1]!=pre_region[i]:
        ytick.append(str(pre_region[i]))
    else:
        ytick.append('-')
ytick.append(str(pre_region[-1]))

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
plt.close('all')
sns.clustermap(data=data,figsize=(11,11),row_cluster=False,col_cluster=False,
               xticklabels=xtick,yticklabels=ytick,cmap=plt.get_cmap('OrRd'),
               row_colors=row_color,col_colors=col_color,square=True,
               cbar_kws={'shrink':0.4,'label':"Connection strength"})
plt.tight_layout()
plt.savefig('temp.jpg',dpi=300)
'''
'''



