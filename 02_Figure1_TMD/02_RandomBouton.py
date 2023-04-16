'''
Take the same number of random bouton on axon as the source file
Compare the differences between the two cases
'''
import os,random,shutil
import numpy as np

def random_bouton(par):
    path,file,write_path=par[0],par[1],par[2]
    with open(os.path.join('./bouton_swc/', file)) as file_object:
        contents = file_object.readlines()
        file_object.close()
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
    bouton_list=np.where(data[:,1]==5)[0]
    b_num=len(bouton_list)
    
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        file_object.close()
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
    axon_list=np.where(data[:,1]==2)[0]
    if len(axon_list)<b_num:
        return
    new_b=random.sample(axon_list.tolist(), b_num)
    data[new_b,1]=5
    new_content=[]
    for x in data:
        temp=str(int(x[0]))+' '+str(int(x[1]))+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(round(x[5]))+' '+str(int(x[6]))+'\n' 
        new_content.append(temp)
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
    
def run_randombouton():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    par_list=[]
    path=r'./bouton_swc_nobouton'
    write_path=r'./bouton_swc_random'
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])

    with Pool(cpu_worker_num) as p:
        p.map(random_bouton, par_list)
    
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Random get time: '+str(time_sum))  
if __name__ =='__main__':
    run_randombouton()     
    
   