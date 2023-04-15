'''
Convert the data format and add the length of each node
'''
import math,os,csv
import shutil 

global grid
grid=30 # set the size of the cube in brain

def filecalculation(par):
    root,name,wirtepath=par[0],par[1],par[2]
    empty=[]
    with open(os.path.join(root,name)) as file_object:
        contents = file_object.readlines()
        # print(len(contents))
        file_object.close()
        t=name.split('.')
        while contents[0][0]=='#':# delete comments
            del contents[0]
        for lineid in range(0,len(contents)):
            x=contents[lineid]
            x=x.strip("\n")
            t1=x.split( )
            t1=list(map(float,t1))
            if t1[0]==0:
                continue
            if t1[0]==t1[-1]: # point to itself, reporting a warning
                print('Circle Warning!!! '+ t[0])
                continue
            if t1[1]!=5 and t1[1]!=1: # not count bouton and soma
                # length to the parent node
                t2=contents[int(t1[-1])-1].split( )
                t2=list(map(float,t2))
                linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
                t1[2],t1[3],t1[4]=t1[2]/grid,t1[3]/grid,t1[4]/grid # take scale for coordinates
                t1[2:5]=list(map(math.floor,t1[2:5]))
                x=str(t1[2])+'_'+str(t1[3])+'_'+str(t1[4])
                empty.append(str(t1[1])+' '+x+' '+str(linelen))
        # convert to csv
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
    cpu_worker_num = 36 # set the number of CPUs in parallel
    
    import time
    time_start = time.time()  # record start time

    ## real-used data
    path='../Data/bouton_swc'
    writepath='./Out_Data_bouton/'

    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)

    par_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for file in files:
            par_list.append((path,file,writepath))
    
    with Pool(cpu_worker_num) as p:
        p.map(filecalculation, par_list)
    
    ## all cell types share the same bouton density
    path='../Data/boutondensity_all_swc'
    writepath='./Out_Data_boutondensity_all/'

    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)

    par_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for file in files:
            par_list.append((path,file,writepath))
    
    with Pool(cpu_worker_num) as p:
        p.map(filecalculation, par_list)
    
    ## each cell type has its own bouton density
    path='../Data/boutondensity_each_swc'
    writepath='./Out_Data_boutondensity_each/'

    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)

    par_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for file in files:
            par_list.append((path,file,writepath))
    
    with Pool(cpu_worker_num) as p:
        p.map(filecalculation, par_list)
    
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('File calculation time: '+str(time_sum))  

if __name__ == "__main__":
    run_pool()
    