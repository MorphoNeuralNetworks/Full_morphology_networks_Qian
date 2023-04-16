'''
Extract the data from the original eswc file and convert all the neurons in the right hemisphere to the left
'''
import os,shutil
import numpy as np
global z_half
z_half=456*25/2
def RawInfoRegist(par):
    path,file,write_path=par[0],par[1],par[2]
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        file_object.close()
     # flip
    soma_local=[]
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# skip comments
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        if t2[6]==-1:
            soma_local=t2[12:15]
            break    
    new_content=[]
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# skip comments
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        if soma_local[2]>z_half:
            temp=str(round(t2[0]))+' '+str(int(t2[1]))+' '+str(t2[12])+' '+str(t2[13])+' '+str(z_half*2-t2[14])+' '+str(round(t2[5]))+' '+str(round(t2[6]))+'\n' #放大到原大
        else:
            temp=str(round(t2[0]))+' '+str(int(t2[1]))+' '+str(t2[12])+' '+str(t2[13])+' '+str(t2[14])+' '+str(round(t2[5]))+' '+str(round(t2[6]))+'\n' #放大到原大
        new_content.append(temp)
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()

def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    
    soma_info=np.load("Soma_info.npy",allow_pickle=True).item()
    cell_type={key:soma_info[key][0] for key in soma_info.keys()}
    neuron_list=[key for key in soma_info.keys()]
    for key in cell_type.keys():
        if "SSp-" in cell_type[key]:
            cell_type[key]="SSp"
    select_type="all" # set the range of data, a specific cell type or all data
    neuron_list=[key for key in soma_info.keys()]    
    select_id=[]
    for i in range(len(neuron_list)):
        if cell_type[neuron_list[i]]==select_type or select_type=="all":
            select_id.append(neuron_list[i]+".eswc")  
    par_list=[]

    path=r'../Data/bouton_raw'
    write_path=r'./bouton_swc_raw'
    # empty folder
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    for file in select_id:
        par_list.append([path,file,write_path])
    with Pool(cpu_worker_num) as p:
        p.map(RawInfoRegist, par_list)
    
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Data get time: '+str(time_sum))  

def resort_id(par):
    path,file,write_path=par[0],par[1],par[2]
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    x=int(contents[-1].split( )[0])
    if x==len(contents):
        print("Good")
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
        temp=str(int(x[0]))+' '+str(int(x[1]))+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(round(x[5]))+' '+str(int(x[6]))+'\n' #放大到原大
        new_content.append(temp)
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()

## reorder the ids of all nodes
def run_resortid():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    par_list=[]

    path=r'./bouton_swc_raw'
    write_path=r'./bouton_swc_raw'
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
    