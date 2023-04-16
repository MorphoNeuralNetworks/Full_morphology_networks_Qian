'''
Downsample the file to reduce the number of nodes for later TMD analysis
This process removes only the axon points and keeps all the bouton points
'''
import numpy as np
import time,copy
import os,shutil,random,math
from scipy.spatial.distance import cdist

global p_dis
p_dis=10 # downsample interval

## downsample and keep bouton
def DataGet(par):
    path,name,write_path=par[0],par[1],par[2]
    with open(os.path.join(path,name)) as file_object:
          contents = file_object.readlines()
          file_object.close()    
    while contents[0][0]=='#':# delete comments
        del contents[0]
    data=[]
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        data.append(t1+[0,0,0])
    
    data=np.array(data)
    for i in range(0,len(data)):
        if data[i,0]==0 or data[i,6]==-1:
            continue
        t1=data[i]
        t2=data[int(t1[6])-1]
        linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
        data[i,7]=linelen
        data[int(t1[6])-1,8]+=1
    for i in range(0,len(data)):
        if data[i,1]==0:
            data[i,9]=-1
        elif data[i,8]==0 or data[i,8]>1 or data[i,1]==5 or data[i,6]==-1:
            data[i,9]=1
    for t in range(0,len(data)):
        if data[t,9]==1:
            i=t
            tt=int(data[i,6])-1
            axonlen=0
            while data[tt,9]==0:
                tt=int(data[i,6])-1
                axonlen+=data[i,8]
                if axonlen>p_dis:
                    axonlen=0
                    data[i,9]=1
                i=tt
    for t in range(1,len(data)):
        if data[t,9]==1:
            i=t
            tt=int(data[i,6])-1
            while data[tt,9]!=1 and data[tt,6]!=-1:
                tt=int(data[i,6])-1
                i=tt
            data[t,6]=data[tt,0]
                
    new_content=[]
    for i in range(0,len(data)):
        if data[i,9]==1:
            temp=str(int(data[i,0]))+' '+str(int(data[i,1]))+' '+str(data[i,2])+' '+str(data[i,3])+' '+str(data[i,4])+' '+str(round(data[i,5]))+' '+str(round(data[i,6]))+'\n' #放大到原大
            new_content.append(temp)
    new_content=np.array(new_content)
    f=open(os.path.join(write_path, name),'w+')
    f.writelines(new_content)
    f.close()

## downsampling while generating files without bouton nodes
def DataGetNoBouton(par):
    path,name,write_path=par[0],par[1],par[2]
    with open(os.path.join(path,name)) as file_object:
          contents = file_object.readlines()
          file_object.close()    
    while contents[0][0]=='#': # delete comments
        del contents[0]
    data=[]
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        data.append(t1+[0,0,0])
    
    data=np.array(data)
    for i in range(0,len(data)):
        if data[i,0]==0 or data[i,6]==-1:
            continue
        if data[i,1]==5:
            data[i,1]=2
        t1=data[i]
        t2=data[int(t1[6])-1]
        linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
        data[i,7]=linelen
        data[int(t1[6])-1,8]+=1
    for i in range(0,len(data)):
        if data[i,1]==0:
            data[i,9]=-1
        elif data[i,8]==0 or data[i,8]>1 or data[i,6]==-1:
            data[i,9]=1
    for t in range(0,len(data)):
        if data[t,9]==1:
            i=t
            tt=int(data[i,6])-1
            axonlen=0
            while data[tt,9]==0:
                tt=int(data[i,6])-1
                axonlen+=data[i,8]
                if axonlen>p_dis:
                    axonlen=0
                    data[i,9]=1
                i=tt
    for t in range(1,len(data)):
        if data[t,9]==1:
            i=t
            tt=int(data[i,6])-1
            while data[tt,9]!=1 and data[tt,6]!=-1:
                tt=int(data[i,6])-1
                i=tt
            data[t,6]=data[tt,0]
                
    new_content=[]
    for i in range(0,len(data)):
        if data[i,9]==1:
            temp=str(int(data[i,0]))+' '+str(int(data[i,1]))+' '+str(data[i,2])+' '+str(data[i,3])+' '+str(data[i,4])+' '+str(round(data[i,5]))+' '+str(round(data[i,6]))+'\n' #放大到原大
            new_content.append(temp)
    new_content=np.array(new_content)
    f=open(os.path.join(write_path, name),'w+')
    f.writelines(new_content)
    f.close()

def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    time_start = time.time()  # record start time
   
    ## downsample with bouton
    par_list=[]
    path=r'./bouton_swc_raw'
    write_path=r'./bouton_swc'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])
    with Pool(cpu_worker_num) as p:
        p.map(DataGet, par_list)
    
    ## files with no bouton
    par_list=[]
    path=r'./bouton_swc_raw'
    write_path=r'./bouton_swc_nobouton'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])
    with Pool(cpu_worker_num) as p:
        p.map(DataGetNoBouton, par_list)
       
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Downsample get: '+str(time_sum))  

# reorder the ids of all nodes
def resort_id(par):
    path,file,write_path=par[0],par[1],par[2]
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    x=int(contents[-1].split( )[0])
    if x==len(contents):
        # print("Good")
        return
    data=[]
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# skip comments
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        data.append(t2)
    data=np.array(data)
    dic_id={int(data[i,0]):i+1 for i in range(len(data))}
    dic_id[-1]=-1
    for lineid in range(0,len(data)):
        data[lineid,0]= dic_id[data[lineid,0]]
        data[lineid,6]= dic_id[data[lineid,6]]
    new_content=[]
    for x in data:
        temp=str(int(x[0]))+' '+str(int(x[1]))+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(round(x[5]))+' '+str(int(x[6]))+'\n'
        new_content.append(temp)
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
    
def run_resortid():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    
    par_list=[]
    path=r'./bouton_swc'
    write_path=r'./bouton_swc'
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])
    path=r'./bouton_swc_nobouton'
    write_path=r'./bouton_swc_nobouton'
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])
    
    with Pool(cpu_worker_num) as p:
        p.map(resort_id, par_list)
    
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('File resortid time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
    run_resortid()            

    



    
    
        
        