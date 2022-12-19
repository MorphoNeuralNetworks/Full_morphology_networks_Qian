## 改变文件格式
import os,csv,nrrd
import numpy as np
import shutil
global brain_info

data_path=r'../Data/annotation_25.nrrd'
global CCFv3_model
CCFv3_model,options=nrrd.read(data_path)  # 读入 nrrd 文件
CCFv3_model=CCFv3_model.astype(np.float64)

def ReturnRegionId(l):
    if l[0]>527 or l[1]>319 or l[2]>456:
        return -1
    else:
        return CCFv3_model[l[0],l[1],l[2]]

## 根据给定的脑分辨率大小，还原未配准前的swc文件
with open('../Data/Other_Infomation/all_brain_metainfo.csv') as f:
    brain_info=list(csv.reader(f))
    f.close()
del brain_info[0]

# 构建brain分辨率
global brain_re
brain_re=dict()
for x in brain_info:
    brain_re[x[0]]=[float(x[2]),float(x[3]),float(x[4])]

def RawInfoRegist(par):
    path,file,write_path=par[0],par[1],par[2]
    brain_name=file.split('_')[0]
    if brain_name=="15257":
        brain_name="210254"
    if brain_name not in brain_re.keys():
        print(brain_name)
    resolution=brain_re[brain_name]
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    x=contents[-1]
    x=x.strip("\n")
    t1=x.split( )
    t2=list(map(float,t1))
    new_content=['0 0 0 0 0 0 0\n']*int(t2[0])
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# 跳过注释
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        ## 给定坐标返回值
        location=list(map(round,t2[12:15]))    
        temp=str(round(t2[0]))+' '+str(round(t2[1]))+' '+\
            str(round(t2[2]*resolution[0],4))+' '+str(round(t2[3]*resolution[1],4))+' '+str(round(t2[4]*resolution[2],4))+' '+\
                str(round(t2[12],4))+' '+str(round(t2[13],4))+' '+str(round(t2[14],4))+' '+\
                str(round(t2[5]))+' '+str(round(t2[6]))+' '+str(int(ReturnRegionId(location)))+'\n' #放大到原大小
        new_content[int(t2[0])-1]=temp
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
            

def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36
    import time
    time_start = time.time()  # 记录开始时间
    
    path=r'../Data/bouton_raw'
    write_path=r'./File_Temp'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    par_list=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])
    with Pool(cpu_worker_num) as p:
        p.map(RawInfoRegist, par_list)
       
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('File Change time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
