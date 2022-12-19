## 对进行Scale>1的操作进行resample补点
import shutil
import os,math
import numpy as np

global p_dis
p_dis=10 #需要补点的最小间隔

def AddPoints(par):
    file,path,write_path=par[0],par[1],par[2]
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    data=[]
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        data.append(t1+[0])
    new_contents=[]
    # 计算节点距离并补充点
    linenum=len(contents)+1
    data=np.array(data)
    for i in range(0,len(data)):
        if data[i,0]==0 or data[i,6]==-1:
            continue
        t1=data[i]
        t2=data[int(t1[6])-1]
        linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
        data[i,7]=linelen
        if linelen>p_dis:
            node_num=math.ceil(linelen/p_dis)
            data[i,6]=linenum
            delta=[(t2[2]-t1[2])/node_num,(t2[3]-t1[3])/node_num,(t2[4]-t1[4])/node_num]
            for k in range(1,node_num-1):
                temp=str(round(linenum))+' '+str(int(t1[1]))+' '+str(round(t1[2]+delta[0]*k,2))+' '+str(round(t1[3]+delta[1]*k,2))+' '+str(round(t1[4]+delta[2]*k,2))+' 1 '+str(linenum+1)+'\n'
                new_contents.append(temp)
                linenum+=1
            temp=str(round(linenum))+' '+str(int(t1[1]))+' '+str(round(t1[2]+delta[0]*(node_num-1),2))+' '+str(round(t1[3]+delta[1]*(node_num-1),2))+' '+str(round(t1[4]+delta[2]*(node_num-1),2))+' 1 '+str(int(t2[0]))+'\n'
            new_contents.append(temp)
            linenum+=1
    new_file=file.split('.')[0]+'.swc'
    contents=[]
    for x in data:
        temp=str(round(x[0]))+' '+str(round(x[1]))+' '+str(round(x[2],2))+' '+str(round(x[3],2))+' '+str(round(x[4],2))+' '+str(round(x[5]))+' '+str(round(x[6]))+'\n'
        contents.append(temp)
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(contents)
    f.writelines(new_contents)
    f.close()

def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 36
    
    folderlist = os.listdir(r'.\Pertubation')
    par_list=[]
    for folder in folderlist:
        t=folder.split('_')
        if float(t[1])>1: #只有放大的才需要resample
            path=os.path.join(r'.\Pertubation',folder)
            write_path=os.path.join(r'.\Pertubation',folder)
            for root, dirs, files in os.walk(path):
                for file in files:
                    par_list.append([file,path,write_path])
            
    import time
    time_start = time.time()  # 记录开始时间
    with Pool(cpu_worker_num) as p:
        p.map(AddPoints, par_list)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Resample time: '+str(time_sum))  


if __name__ =='__main__':
    run__pool()
    