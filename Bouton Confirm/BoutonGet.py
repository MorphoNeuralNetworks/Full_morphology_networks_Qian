import os,csv,math,shutil
import numpy as np
import matplotlib.pyplot as plt

folder="./plot_files/"
if os.path.exists(folder):
    shutil.rmtree(folder)
os.mkdir(folder)
temp_data=np.load('neruon_order.npy',allow_pickle=True)
path='./similar_neuron/'
count=1
for x in temp_data:
    shutil.copyfile(path+x+'.swc', folder+str(count)+'.swc')
    count+=1

## 提取bouton文件
for root, dirs, files in os.walk(folder):
    for name in files:
        if ".swc" in name:
            with open(os.path.join(folder,name)) as file_object:
                contents = file_object.readlines()
                # print(len(contents))
                file_object.close()
                t=name.split('.swc')[0]
                while contents[0][0]=='#':# 删除注释
                    del contents[0]
                content=['##n,orderinfo,name,comment,z,x,y, pixmax,intensity,sdev,volsize,mass,,,, color_r,color_g,color_b'+'\n']
                count=1
                for lineid in range(0,len(contents)):
                    x=contents[lineid]
                    x=x.strip("\n")
                    t1=x.split( )
                    t1=list(map(float,t1))
                    if t1[1]==5:
                        temp=str(count)+',,,,'+str(t1[4])+','+str(t1[2])+','+str(t1[3])+',0.000,0.000,0.000,1000,0.000,,,,0,255,0\n'
                        content.append(temp)
                        count+=1
                f=open('./plot_files/'+t+'.apo',"w+",newline='')
                f.writelines(content)
                f.close()
'''
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

node_color={'SSp-bfd':5,'fiber tracts':6,'SSs':8,'VPL':9,'VPM':10}
data_path=r'../Data/annotation_25.nrrd'
CCFv3_model,options=nrrd.read(data_path)  # 读入 nrrd 文件
import os
for root, dirs, files in os.walk('./similar_neuron/'):
    for name in files:
        if ".swc" in name:
            with open(os.path.join('./similar_neuron/',name)) as file_object:
                contents = file_object.readlines()
                # print(len(contents))
                file_object.close()
                file_name=name.split('.swc')[0]
                while contents[0][0]=='#':# 删除注释
                    del contents[0]
                count=1
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
                            if t in node_color.keys():
                                id_t=node_color[t]
                                temp=str(int(t1[0]))+" "+str(id_t)+" "+str(t1[2])+" "+str(t1[3])+" "+str(t1[4])+" "+str(int(t1[5]))+" "+str(int(t1[6]))+"\n"
                                contents[lineid]=temp
                            else:
                                id_t=1
                                temp=str(int(t1[0]))+" "+str(id_t)+" "+str(t1[2])+" "+str(t1[3])+" "+str(t1[4])+" "+str(int(t1[5]))+" "+str(int(t1[6]))+"\n"
                                contents[lineid]=temp
                f=open('./plot_files/'+'No_bouton_'+file_name+'.swc',"w+",newline='')
                f.writelines(contents)
                f.close()
'''