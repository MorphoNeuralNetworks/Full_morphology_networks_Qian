## 调用global features from vaa3d plugin in获取结果
import subprocess
import re,os,csv
import json
import multiprocessing as mp
import numpy as np
'''
global path
path=r'D:\QPH\Data\bouton_swc'


def GetFeature(filename):
    readpath=path+'\\'+filename
    outpath='D:\\QPH\\Bouton_Confirm\\feature\\'+filename.split('.')[0]+'_feature.txt'
    
    cmd=r'D:\QPH\3.603c\vaa3d_msvc.exe /x D:\QPH\3.603c\plugins\neuron_utilities\global_neuron_feature\global_neuron_feature.dll /f compute_feature /i '+readpath
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # process.wait()
    command_output = process.stdout.read().decode()
    
    c1=re.search('compute Feature', command_output)
    c2=re.search('the plugin preprocessing takes', command_output)
    if c1 is None or c2 is None:
        print(filename+' no result')
        return
    res=command_output[c1.span()[1]+4:c2.span()[0]-6]
    with open(outpath,"w+",newline='') as f:
        f.write(res)
        f.close()

def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 20
    global filenames
    
    for root,dirs,files in os.walk(path,topdown=True):
        filenames=files
    for root,dirs,files in os.walk(r'D:\QPH\Bouton_Confirm\feature',topdown=True):
        for i in files:
            x=i.replace('_feature.txt','.swc')
            if x in filenames:
                t=filenames.index(x)
                del filenames[t]
        print(filenames)
        with Pool(cpu_worker_num) as p:
            p.map(GetFeature, filenames)
'''
def GetFeature(contents):
    temp=[]
    for x in contents:
        t=x.replace('\t','')
        t=t.replace('\n','')
        t=t.split(':')
        temp.append(float(t[1]))
    return temp
    
if __name__ =='__main__':
    # run__pool()

    # 构成所有数据的特征文件
    feature_map=[]
    soma_local={} #所有文件对应的soma坐标
    
   
    ## Allen数据
    with open(r'..\Data\Other_Infomation\BoutonDataCellType.csv', 'r', newline='') as csvfile:
        t = csv.reader(csvfile)
        neuron_data=np.array(list(t))
        csvfile.close()
    count=0

    for key in neuron_data:
        count+=1
        if count%100==0:
            print(count)
        t=key[0]
        x=t+'_feature.txt'
        if os.path.exists('.\\feature\\'+x):
            temp=[t,key[1]]
            with open('.\\feature\\'+x) as file_object:
                contents = file_object.readlines()
                file_object.close()
            temp.extend(GetFeature(contents))
            feature_map.append(temp)
        else:
            print(t+' no feature')

    # 对所有区域进行修正
    with open(r'..\Data\Other_Infomation\Dataset_Structure.csv')as f:
        structure = np.array(list(csv.reader(f)))
        f.close()
    with open(r'..\Data\Other_Infomation\Selected_Regions.csv','r',encoding='utf_8')as f:
        select_region =list(csv.reader(f))
        del select_region[0]
        select_region=np.array(select_region)
        f.close()
        select_list=select_region[:,0].tolist()
    # 构建映射区域
    change_dic=dict()
    change_dic={'HY':'HY','MB':'MB','TH':'TH','MY':'MY','unknown':'unknown','P':'P','CUL4 5':'CUL','HPF':'HPF','BS':'BS','PAL':'PAL',\
                'AId6':'AId','AIp6':'AIp','SSs6':'SSs','SSp6':'SSp','SSp-bfd6':'SSp-bfd','SSp-m6':'SSp-m','ADUv5':'AUDv',\
                'ACAd6':'ACAd','AUDv5':'AUDv','AUDv5':'AUDv','AUDv6':'AUDv','AUDv5':'AUDv','AUDpo6':'AUDpo','AUDp6':'AUDp','AUDd6':'AUDd',\
                'VISp6':'VISp','VISrl6':'VISrl','VISC6':'VISC','VISal6':'VISal','VISl6':'VISl','ECT6':'ECT','wholebrain':'root',\
                'MOs6':'MOs','MOs4':'MOs','MOp6':'MOp','MOp4':'MOp','TEa6':'TEa','GU6':'GU','AIp6':'AIp','ORBl6':'ORBl','ENTm2/3':'ENTm','SSp':'SSp','root':'root'}

    for x in structure:
        level_list=x[1].split('/')[1:-1]
        level_list.reverse()
        for k in level_list:
            if k in select_list:
                t=select_list.index(k)
                change_dic[str(x[3])]=str(select_region[t,2])
                break
    for i in range(0,len(feature_map)):
        x=feature_map[i]
        if x[1] not in change_dic.keys():
            print(x[1])
        else:
            feature_map[i][1]=change_dic[x[1]]
  
    # 保存为csv文件
    with open("Feature_Total.csv","w+",newline='') as f:
        csv_writer = csv.writer(f)
        t=['id','cell type','N_node','Soma_surface','N_stem','f0','f1','f2',\
            'Number of Nodes','Soma Surface','Number of Stems','Number of Bifurcatons',\
            'Number of Branches','Number of Tips','Overall Width','Overall Height',\
            'Overall Depth','Average Diameter','Total Length','Total Surface','Total Volume',\
            'Max Euclidean Distance','Max Path Distance','Max Branch Order','Average Contraction',\
            'Average Fragmentation','Average Parent-daughter Ratio','Average Bifurcation Angle Local',\
            'Average Bifurcation Angle Remote','Hausdorff Dimension']
        csv_writer.writerow(t)
        for rows in feature_map:
            csv_writer.writerow(rows)
        f.close()
    '''
    '''
