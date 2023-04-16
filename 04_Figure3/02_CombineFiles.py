'''
## Count the length of axon and dendrite for each neuron within each cube 
# Dataset_Soma.csv
# soma_id | cube_local | axon length type=2 | dendrite length type=3,4

## the total length of axon and dendrite within each cube
# Dataset_Cube.csv
'''
import os,csv
import numpy as np

def CombineFile(par):
    path,folder=par[0],par[1]
    empty=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for name in files:          
            with open(os.path.join(root,name)) as file_object:
                soma=name.split('.')[0]
                contents = file_object.readlines()
                file_object.close()
                
            cube_set=[]
            for lines in contents:
                x=lines.split(',')
                cube_set.append(x[1])
            cube_set=list(set(cube_set))
            # length statistics
            count_list=[];
            for i in range(0,len(cube_set)):
                count_list.append([0,0])
            for x in contents:
                t1=x.split(',')
                t=cube_set.index(t1[1])
                if float(t1[0])==2:
                    count_list[t][0]=count_list[t][0]+float(t1[2]);
                elif float(t1[0])==3 or float(t1[0])==4:
                    count_list[t][1]=count_list[t][1]+float(t1[2]);
            for i in range(0,len(cube_set)):
                empty.append([soma,cube_set[i],count_list[i][0],count_list[i][1]])
    
    with open(".\\Temp_Data\\Dataset_Soma_"+folder+".csv","w+",newline='') as f:
        csv_writer = csv.writer(f)
        for rows in empty:
            csv_writer.writerow(rows)
        f.close()
    
    # get the length of axon and dendrite in each cube
    data=np.array(empty)
    data = data[np.argsort(data[:,1])]
    lineid=0
    re_list=[]
    local_id=data[0,1]
    count_axon=0
    count_dend=0
    while lineid<len(data):
        if local_id!=data[lineid,1]:
            re_list.append([str(local_id),count_axon,count_dend])
            local_id=data[lineid,1]
            count_axon=0
            count_dend=0
        else:
            count_axon+=data[lineid,2].astype(np.float64)
            count_dend+=data[lineid,3].astype(np.float64)
            lineid+=1
    re_list.append([str(local_id),count_axon,count_dend])
    
    with open(".\\Temp_Data\\Dataset_Cube_"+folder+".csv","w+",newline='') as f:
        csv_writer = csv.writer(f)
        for rows in re_list:
            csv_writer.writerow(rows)
        f.close()

def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 4 # set the number of CPUs in parallel
    
    par_list = [('./Out_Data_bouton','bouton'),
                ('./Out_Data_boutondensity_all','boutondensity_all'),
                ('./Out_Data_boutondensity_each','boutondensity_each')]
    
    import time
    time_start = time.time()  # record start time
    with Pool(cpu_worker_num) as p:
        p.map(CombineFile, par_list)
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Combine File time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()





















