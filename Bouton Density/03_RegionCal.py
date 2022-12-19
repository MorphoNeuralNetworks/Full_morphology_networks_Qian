## 指定脑区统计bouton数量和axonlength长度
import os,csv,math,shutil
import numpy as np

global need_regions
global region
region="LGd"
with open('VPM.csv') as f:
    temp=csv.reader(f)
    need_regions=[int(x[0]) for x in temp]
    f.close()


def FileCount(par):
    path,file,write_path=par[0],par[1],par[2]
    bouton_count=0
    axon_length=0
    with open(os.path.join(path,file)) as file_object:
        contents = file_object.readlines()
        # print(len(contents))
        file_object.close()
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        if t1[1] in need_regions:
        # if t1[1] !=0:
            if t1[0]==5:
                bouton_count+=1
            elif t1[0]==2:
                axon_length+=t1[2]
    temp=str(bouton_count)+' '+str(axon_length)
    new_file=file.split('.')[0]+'.txt'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(temp)
    f.close()
def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36
    import time
    time_start = time.time()  # 记录开始时间
    
    path='./File_Info'
    write_path='./Temp'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    par_list=[]
    soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
    for root, dirs, files in os.walk(path):
        for file in files:
            if soma_info[file.split('.')[0]][0]==region or region=="All":
                par_list.append([path,file,write_path])
    with Pool(cpu_worker_num) as p:
        p.map(FileCount, par_list)
       
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('File Count time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
    
    for root, dirs, files in os.walk('./Temp'):
        data=[]
        for file in files:
            with open(os.path.join('./Temp',file)) as file_object:
                temp = file_object.readlines()
                file_object.close()
            t=temp[0].split( )
            t=list(map(float,t))
            if t[0]==0:
                continue
            data.append(t)
        data=np.array(data)
        print(np.sum(data,0))
        t=np.sum(data,0)
        print(t[0]/t[1])
























