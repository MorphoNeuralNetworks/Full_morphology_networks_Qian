'''
Extract the swc file before and after registration from the raw eswc file
'''
import os,csv
import shutil
global brain_info
import numpy as np
## restore the unaligned swc file according to the given brain resolution size
with open('../Data/Other_Infomation/all_brain_metainfo.csv') as f:
    brain_info=list(csv.reader(f))
    f.close()
del brain_info[0]

# create brain resolution dictionary
global brain_re
brain_re=dict()
for x in brain_info:
    brain_re[x[0]]=[float(x[2]),float(x[3]),float(x[4])]

## extract files that are not registered to CCFv3 based on raw files
def RawInfoNoregist(par):
    path,file,write_path=par[0],par[1],par[2]
    brain_name=file.split('_')[0]
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
    new_content=[]
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# skip comments
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        temp=str(int(t2[0]))+' '+str(int(t2[1]))+' '+str(round(t2[2]*resolution[0],4))+' '+str(round(t2[3]*resolution[1],4))+' '+str(round(t2[4]*resolution[2],4))+' '+str(t2[5])+' '+str(int(t2[6]))+'\n'
        new_content.append(temp)
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
        
## extract the file registered to CCFv3 from the raw file
def RawInfoRegist(par):
    path,file,write_path=par[0],par[1],par[2]
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        #print(len(contents))
        file_object.close()
    x=contents[-1]
    x=x.strip("\n")
    t1=x.split( )
    t2=list(map(float,t1))
    new_content=[]
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# skip comments
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        temp=str(int(t2[0]))+' '+str(int(t2[1]))+' '+str(t2[12])+' '+str(t2[13])+' '+str(t2[14])+' '+str(t2[5])+' '+str(int(t2[6]))+'\n'
        new_content.append(temp)
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
        
def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time() # record start time
    
    # extract files that are not registered to CCFv3 based on raw files
    path=r'../Data/bouton_raw'
    write_path=r'../Data/Noregisted/bouton_swc_noadd'
    # empty the folder
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
        p.map(RawInfoNoregist, par_list)
    
    # extract the file registered to CCFv3 from the raw file 
    path=r'../Data/bouton_raw'
    write_path=r'../Data/bouton_swc_noadd'
    # empty the folder
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
    
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Extract swc files time: '+str(time_sum))  

## rearrange the serial numbers of the nodes in the swc file
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
        if contents[lineid][0]=='#':# 跳过注释
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
        data[lineid,0]=dic_id[data[lineid,0]]
        data[lineid,6]=dic_id[data[lineid,6]]
    new_content=[]
    for x in data:
        temp=str(int(x[0]))+' '+str(int(x[1]))+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(x[5])+' '+str(int(x[6]))+'\n' #放大到原大
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
    # empty the folder
    path=r'../Data/bouton_swc_noadd'
    write_path=r'../Data/bouton_swc_noadd'
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])
    path=r'../Data/Noregisted/bouton_swc_noadd'
    write_path=r'../Data/Noregisted/bouton_swc_noadd'
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])

    with Pool(cpu_worker_num) as p:
        p.map(resort_id, par_list)
    
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Resort id time: '+str(time_sum)) 

if __name__ =='__main__':
    run__pool()
    run_resortid()   

   