'''
Extract the coordinate of boutons
'''
import os,shutil

global add_method
add_method=''
# add_method='Noregisted/' # decide whether the data is pre-registration or post-registration

def GetBouton(par):
    file,bouton_path,bouton_write_path=par[0],par[1],par[2]
    with open(os.path.join(bouton_path, file)) as file_object:
        contents = file_object.readlines()
        # print(len(contents))
        file_object.close()
    new_content=[]
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#': # skip comments
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        if t2[1]==5:
            temp=str(t2[2])+' '+str(t2[3])+' '+str(t2[4])+'\n' 
            new_content.append(temp)
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(bouton_write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
    
def run_pool_Getbouton():
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    
    ## real-used data
    bouton_path='../Data/'+add_method+'bouton_swc'
    bouton_write_path=r'../Data/'+add_method+'/bouton'
    if os.path.exists(bouton_write_path):
        shutil.rmtree(bouton_write_path)  
    os.mkdir(bouton_write_path)
    par_list=[]
    for root, dirs, files in os.walk(bouton_path):
        for file in files:
            par_list.append([file,bouton_path,bouton_write_path])
    with Pool(cpu_worker_num) as p:
        p.map(GetBouton, par_list)
    
    ## all cell types share the same bouton density
    bouton_path=r'../Data/'+add_method+'/boutondensity_all_swc'
    bouton_write_path=r'../Data/'+add_method+'/boutondensity_all'
    if os.path.exists(bouton_write_path):
        shutil.rmtree(bouton_write_path)  
    os.mkdir(bouton_write_path) 
    par_list=[]
    for root, dirs, files in os.walk(bouton_path):
        for file in files:
            par_list.append([file,bouton_path,bouton_write_path])
    with Pool(cpu_worker_num) as p:
        p.map(GetBouton, par_list)
    
    ## each cell type has its own bouton density
    bouton_path=r'../Data/'+add_method+'/boutondensity_each_swc'
    bouton_write_path=r'../Data/'+add_method+'/boutondensity_each'
    if os.path.exists(bouton_write_path):
        shutil.rmtree(bouton_write_path)  
    os.mkdir(bouton_write_path) 
    par_list=[]
    for root, dirs, files in os.walk(bouton_path):
        for file in files:
            par_list.append([file,bouton_path,bouton_write_path])
    with Pool(cpu_worker_num) as p:
        p.map(GetBouton, par_list)
    
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Get bouton time: '+str(time_sum))  

if __name__ =='__main__':
    run_pool_Getbouton()
    
    
    