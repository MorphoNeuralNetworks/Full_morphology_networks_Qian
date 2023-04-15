'''
Convert swc files containing boutons to the corresponding uniformly distributed data using the given bouton density
'''
import os,math,shutil
import numpy as np
global add_method
add_method=''
# add_method='Noregisted/' # decide whether the data is pre-registration or post-registration

global path
path=r'../Data/'+add_method+'bouton_swc'

def BoutondensityChange(par):
    name,bouton_density_p,writepath=par[0],1/par[1],par[2]
    with open(os.path.join(path,name)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    data=[]
    while contents[0][0]=='#': # delete comments
        del contents[0]
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        data.append(t1+[0,0])
    # calculate the distance and number of nodes
    data=np.array(data)
    for i in range(0,len(data)):
        if data[i,0]==0 or data[i,6]==-1:
            continue
        t1=data[i]
        t2=data[int(t1[6])-1]
        linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
        data[i,8]=linelen
        data[int(t1[6])-1,7]+=1
        if data[i,1]==5:
            data[i,1]=2
    visit=np.zeros((1,len(data)))
    visit[0,0]=1
    # reassign bouton
    for i in range(0,len(data)):
        if data[i,7]==0 and data[i,1]==2: # axon leaf node
            data[i,1]=5
            t=i
            tt=int(data[t,6])-1
            axonlen=0
            while visit[0,tt]==0 and (data[tt,1]!=3 or data[tt,1]!=4):
                visit[0,t]=1
                tt=int(data[t,6])-1
                axonlen+=data[t,8]
                if data[t,1]==5:
                    axonlen=0
                if axonlen>bouton_density_p:
                    axonlen=0
                    data[t,1]=5
                t=tt
    new_content=['0 0 0 0 0 0 0\n']*len(contents)
    for i in range(0,len(data)):
        t=data[i]
        temp=str(round(t[0]))+' '+str(round(t[1]))+' '+str(round(t[2],4))+' '+str(round(t[3],4))+' '+str(round(t[4],4))+' '+str(round(t[5]))+' '+str(round(t[6]))+'\n' #放大到原大小
        new_content[int(t[0])-1]=temp
    
    f=open(os.path.join(writepath, name),'w+')
    f.writelines(new_content)
    f.close()

def run__pool():  # main process           
    for root,dirs,files in os.walk(path,topdown=True):
        file=files
    # get cell-type of neurons
    soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
    cell_type={key:soma_info[key][0] for key in soma_info.keys()}
    
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    
    bouton_density_p=0.061
    ## all cell types share the same bouton density
    writepath='../Data/'+add_method+'boutondensity_all_swc'
    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)
    par_list=[]
    for x in file:
        par_list.append((x,bouton_density_p,writepath))
    
    with Pool(cpu_worker_num) as p:
        p.map(BoutondensityChange, par_list)
    
    ## each cell type has its own bouton density
    best_par=np.load(r'../Data/Other_Infomation/best_density.npy', allow_pickle=True).item()  
    writepath='../Data/'+add_method+'boutondensity_each_swc'
    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)
    par_list=[]
    for x in file:
        par_list.append((x,best_par[cell_type[x]]*bouton_density_p,writepath))

    with Pool(cpu_worker_num) as p:
        p.map(BoutondensityChange, par_list)
    
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Boutondensity Change time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()

    
    