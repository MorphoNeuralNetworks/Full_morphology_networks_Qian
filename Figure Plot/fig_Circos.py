### 获取circos所需要的基本信息
## 执行语句 ..\bin\circos -conf .\circos.conf
import numpy as np
import csv,os
method="bouton"
# method="boutondensity_each"
# method="boutondensity_all"
## 获取神经元所在脑区的信息
with open(r'..\Data\Other_Infomation\BoutonDataCellType.csv', 'r', newline='') as csvfile:
    t = csv.reader(csvfile)
    area_data=np.array(list(t))
    csvfile.close()
total_neuron_list=area_data[:,0]
total_cell_type=dict()
for root, dirs, files in os.walk(r'..\Data\Noregisted\bouton_swc'):
    for file in files:
        t=file.split('.')[0]
        tt=np.where(area_data[:,0]==t)
        if len(tt[0])==0:
            print(t+' out of file')
        else:
            total_cell_type[file.split('.')[0]]=str(area_data[tt[0],1][0])
## 寻找上层的种类
with open(r'..\Data\Other_Infomation\Dataset_Structure.csv', 'r', newline='') as csvfile:
    t = csv.reader(csvfile)
    structure=np.array(list(t))
    csvfile.close()
structure_dict={}
structure_list=structure[:,3]
for x in structure:
    t=x[1].split('/')
    structure_dict[str(x[3])]=t[1:-1]

## 1.生成neurons.conf 按照structure顺序
types=list(total_cell_type.values())
total_cell_count={x:types.count(x) for x in list(set(types))}
contents=[]
for x in structure_list:
    if x in total_cell_count.keys():
        temp="chr - "+x+" "+x+" 1 "+str(total_cell_count[x]+1)+" color-aibs-"+str.lower(x)+'\n'
        contents.append(temp)
with open(r'./MyCircos/circos/GenerateTool/neurons.conf',"w+",newline='') as f:
    f.writelines(contents)
    f.close()  

## 构建新的映射序列
type_count={x:1 for x in list(set(types))}
new_type={}
for x in total_neuron_list:
    type_t=total_cell_type[x]
    start=type_count[type_t]
    type_count[type_t]=type_count[type_t]+1
    new_type[str(x)]=type_t+' '+str(start)+' '+str(start+1)


# data=np.load(r'D:\QPH\BrainNetwork\bouton_connection.npy',allow_pickle=True)
data=np.load("D:/QPH/BrainNetwork/"+method+"_connection.npy",allow_pickle=True)
# data=np.load(r'D:\QPH\BrainNetwork_Pertubation\Pertubation_Result\scale_0_prune_0.5_delete_0_dendrite_Bouton.npy',allow_pickle=True)
neuron_list=list(set(data[:,0].tolist()+data[:,1].tolist()))
neuron_list=np.array(neuron_list)

## 2. 生成neuron link文件
contents=[]
for x in data:
    temp=new_type[x[0]]+' '+new_type[x[1]]+' color=color-aibs-'+str.lower(total_cell_type[x[0]])+'_a18'
    contents.append(temp+'\n')
with open(r'./MyCircos/circos/GenerateTool/neurons_link.txt',"w+",newline='') as f:
    f.writelines(contents)
    f.close() 

## 3. 生成上层大区域范围
upper_name={'315':'isocortex','549':'th','477':'str','703':'ctxsp','1089':'hpf'}  # '698':'olf','803':'pal','1065':'hb'
# isoCortex,Thalamus,Striatum,Cortical subplate,Hippocampal formation,Olfactory areas,Pallidum,Hindbrain
upper_area=[x for x in upper_name.keys()]
upper_area.append('Others')
upper_dict={x:[] for x in upper_area}

name_conf=[]
for key in upper_dict.keys():
    name_conf=name_conf+upper_dict[key]

for x in neuron_list:
    t=total_cell_type[x]
    path=structure_dict[t]
    mark=1
    for k in upper_area:
        if k in path:
            mark=0
            upper_dict[k].append(str(x))
    if mark==1:
        upper_dict['Others'].append(str(x))

## 4.生成neurons_source.conf文件
for k in upper_name.keys():
    name=upper_name[k]
    neruon_name=[new_type[x]+'\n' for x in upper_dict[k]]
    with open(r'./MyCircos/circos/GenerateTool/neurons_source_'+name+'.txt',"w+",newline='') as f:
        f.writelines(neruon_name)
        f.close() 

contents=[]
for k in upper_name.keys():
    name=upper_name[k]
    st="<plot>\ntype = highlight\nfile = ./neurons_source_"+name+\
        ".txt\nr0 = 0.880000r\nr1 = 0.800000r\nfill_color = color-aibs-"+name+\
        "\nstroke_thickness = 0p\nstroke_color = white\nz = 15\n</plot>\n"
    contents.append(st)
with open(r'./MyCircos/circos/GenerateTool/neurons_source.conf',"w+",newline='') as f:
    f.writelines(contents)
    f.close()  


## 生成颜色的额外文件
contents=[]
count=0
for i in range(1,8):
    t_c=round(255/i)
    contents.append('color-aibs-cluster'+str(count)+' = '+str(t_c)+',0,0\n')
    count+=1
    contents.append('color-aibs-cluster'+str(count)+' = 0,'+str(t_c)+',0\n')
    count+=1
    contents.append('color-aibs-cluster'+str(count)+' = 0,0,'+str(t_c)+'\n')
    count+=1
    contents.append('color-aibs-cluster'+str(count)+' = '+str(t_c)+','+str(t_c)+',0\n')
    count+=1
    contents.append('color-aibs-cluster'+str(count)+' = 0,'+str(t_c)+','+str(t_c)+'\n')
    count+=1
    contents.append('color-aibs-cluster'+str(count)+' = '+str(t_c)+',0,'+str(t_c)+'\n')
    count+=1
    # contents.append('color-aibs-cluster'+str(count)+' = '+str(t_c)+','+str(t_c)+','+str(t_c)+'\n')
    # count+=1
with open(r'./MyCircos/circos/GenerateTool/neurons_colors_add.conf',"w+",newline='') as f:
    f.writelines(contents)
    f.close() 


## 生成neurons clusters文件
threshold=40
import shutil
if os.path.exists(r'./MyCircos/circos/GenerateTool/clusters'):
    shutil.rmtree(r'./MyCircos/circos/GenerateTool/clusters')
os.mkdir(r'./MyCircos/circos/GenerateTool/clusters')

data=np.load('D:/QPH/BrainNetwork/'+method+'_leiden.npy',allow_pickle=True).item()
node_list=data['node_list']
clusters=data['res']
for i in range(0,3):#len(clusters)):
    if len(clusters[i])>threshold:
        neuron_cluster=[new_type[node_list[x]]+'\n' for x in clusters[i]]
        with open(r'./MyCircos/circos/GenerateTool/clusters/neurons_cluster'+str(i)+'.txt',"w+",newline='') as f:
            f.writelines(neuron_cluster)
            f.close() 
        
contents=[]
for i in range(0,3):#len(clusters)):
    if len(clusters[i])>threshold:
        st="<plot>\ntype = highlight\nfile = ./clusters/neurons_cluster"+str(i)+\
            ".txt\nr0 = 0.980000r\nr1 = 0.900000r\nfill_color = color-aibs-cluster"+str(i)+\
            "\nstroke_thickness = 0p\nstroke_color = white\nz = 15\n</plot>\n"
        contents.append(st)
    with open(r'./MyCircos/circos/GenerateTool/neurons_cluster.conf',"w+",newline='') as f:
        f.writelines(contents)
        f.close()  

