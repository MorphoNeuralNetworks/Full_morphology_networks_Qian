# 转换数据格式，添加每个节点的长度
import math
import os
import numpy as np
import csv
import shutil 

global grid
grid=30 #cube的大小

def filecalculation(par):
    root,name,wirtepath=par[0],par[1],par[2]
    empty=[]
    with open(os.path.join(root,name)) as file_object:
        contents = file_object.readlines()
        # print(len(contents))
        file_object.close()
        t=name.split('.')
        while contents[0][0]=='#':# 删除注释
            del contents[0]
        for lineid in range(0,len(contents)):
            x=contents[lineid]
            x=x.strip("\n")
            t1=x.split( )
            t1=list(map(float,t1))
            if t1[0]==0:
                continue
            if t1[0]==t1[-1]: #修正版本的数据会出现自己导向自己的情况，得处理这个问题
                print('Circle Warning!!! '+ t[0])
                continue
            if t1[1]!=5 and t1[1]!=1: #不统计bouton和soma的位置
                # 计算到上一节点的长度
                t2=contents[int(t1[-1])-1].split( )
                t2=list(map(float,t2))
                linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
                t1[2],t1[3],t1[4]=t1[2]/grid,t1[3]/grid,t1[4]/grid #标度修正
                #对坐标进行取scale
                t1[2:5]=list(map(math.floor,t1[2:5]))
                x=str(t1[2])+'_'+str(t1[3])+'_'+str(t1[4])
                empty.append(str(t1[1])+' '+x+' '+str(linelen))
        # 转换为csv
        data=[]
        for i in range(0,len(empty)):
            temp=empty[i].split()
            data.append(temp)
        with open(wirtepath+t[0]+".csv","w+",newline='') as f:
            csv_writer = csv.writer(f)
            for rows in data:
                csv_writer.writerow(rows)
            f.close()

def run_pool():  # main process
    
    from multiprocessing import Pool
    cpu_worker_num = 36
    
    import time
    time_start = time.time()  # 记录开始时间

    ## 对于bouton数据
    path='../Data/bouton_swc'
    writepath='./Out_Data_bouton/'
    # 清空文件夹
    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)
    # 构建参数组合
    par_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for file in files:
            par_list.append((path,file,writepath))
    
    with Pool(cpu_worker_num) as p:
        p.map(filecalculation, par_list)
    
    ## 对于boutondensity_all数据
    path='../Data/boutondensity_all_swc'
    writepath='./Out_Data_boutondensity_all/'
    # 清空文件夹
    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)
    # 构建参数组合
    par_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for file in files:
            par_list.append((path,file,writepath))
    
    with Pool(cpu_worker_num) as p:
        p.map(filecalculation, par_list)
    
    ## 对于boutondensity_each数据
    path='../Data/boutondensity_each_swc'
    writepath='./Out_Data_boutondensity_each/'
    # 清空文件夹
    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)
    # 构建参数组合
    par_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for file in files:
            par_list.append((path,file,writepath))
    
    with Pool(cpu_worker_num) as p:
        p.map(filecalculation, par_list)
    
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Perturbation time: '+str(time_sum))  


if __name__ == "__main__":
    run_pool()
    