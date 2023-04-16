'''
Find the brain region where each point is located
'''
import os,csv,nrrd
import numpy as np
import shutil
global brain_info

data_path=r'../Data/Other_Infomation/annotation_25.nrrd'
global CCFv3_model
CCFv3_model,options=nrrd.read(data_path)
CCFv3_model=CCFv3_model.astype(np.float64)

def ReturnRegionId(l):
    if l[0]>527 or l[1]>319 or l[2]>456:
        return -1
    else:
        return CCFv3_model[l[0],l[1],l[2]]

## restore the unaligned swc file according to the given brain resolution size
with open('../Data/Other_Infomation/all_brain_metainfo.csv') as f:
    brain_info=list(csv.reader(f))
    f.close()
del brain_info[0]

# build brain resolution
global brain_re
brain_re=dict()
for x in brain_info:
    brain_re[x[0]]=[float(x[2]),float(x[3]),float(x[4])]

def RawInfoRegist(par):
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
    new_content=['0 0 0 0 0 0 0\n']*int(t2[0])
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# skip comments
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        ## get the brain area from the coordinates after registration
        location=list(map(round,[t2[12]/25,t2[13]/25,t2[14]/25]))    
        temp=str(round(t2[0]))+' '+str(round(t2[1]))+' '+\
            str(round(t2[2]*resolution[0],4))+' '+str(round(t2[3]*resolution[1],4))+' '+str(round(t2[4]*resolution[2],4))+' '+\
                str(round(t2[12],4))+' '+str(round(t2[13],4))+' '+str(round(t2[14],4))+' '+\
                str(round(t2[5]))+' '+str(round(t2[6]))+' '+str(int(ReturnRegionId(location)))+'\n'
        new_content[int(t2[0])-1]=temp
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
            

def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    
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
       
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('File Change time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
