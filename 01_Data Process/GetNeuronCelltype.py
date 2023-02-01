## 为所有文件构建对应的cell type信息
import csv,os,json
import numpy as np
import nrrd

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
        
## 构建参考cell type
with open(r'..\Data\Other_Infomation\1780_cell_type.csv', 'r', newline='',encoding='utf8') as csvfile:
    t = csv.reader(csvfile)
    t=list(t)
    cell_type_refer={x[0]:x[1] for x in t}

##指定目录读取文件获得soma位置
path='./bouton_swc'
data_path=r'./annotation_25.nrrd'
CCFv3_model,options=nrrd.read(data_path)  # 读入 nrrd 文件
neuron_type=dict()
for root,dirs,files in os.walk(path,topdown=True):
    for file in files:
        name=file.split('.')[0]
        if name in cell_type_refer.keys():
            neuron_type[name]=cell_type_refer[name]
        else:
            # print(name + " not in refer")
            with open(os.path.join(path,file)) as file_object:
                contents = file_object.readlines()
                file_object.close()
            while contents[0][0]=='#':# 删除注释
                del contents[0]
            for lineid in range(0,len(contents)):
                x=contents[lineid]
                x=x.strip("\n")
                t1=x.split( )
                t1=list(map(float,t1))
                if t1[-1]==-1:
                    break
            if round(t1[2]/25)>=528 or round(t1[3]/25)>=320 or round(t1[4]/25)>=456:
                print(name+' Outside')
                continue
            t=CCFv3_model[round(t1[2]/25),round(t1[3]/25),round(t1[4]/25)]
            if t==0:
                neuron_type[name]="fiber tracts"
                print(name+' Id 0')
                continue
            t=Id2Celltype[t]
            t=Celltype2Select[t]
            neuron_type[name]=t

for key in neuron_type.keys():
    if neuron_type[key] not in select_region:
        print(key+' not in select regions:\t'+neuron_type[key])

neuron_list=[[key,neuron_type[key]] for key in neuron_type.keys()]
with open("./Other_Infomation/BoutonDataCellType.csv","w+",newline='') as f:
    csv_writer = csv.writer(f)
    for row in neuron_list:
        csv_writer.writerow(row)
    f.close()