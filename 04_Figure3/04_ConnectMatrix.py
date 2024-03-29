'''
Generate connection matrix
'''
import math,os,csv
import numpy as np

global bouton_density_p
bouton_density_p=0.061

def GenerateMatrix(folderpath):
    # build data indexes
    pixel_axon_dir=dict()
    pixel_dendrite_dir=dict()
    pixel_axon_set=dict()
    pixel_dendrite_set=dict()
    pixel_bouton_dir=dict()
    # Load data
    pixel_axon_dir = np.load('.\\Temp_Data\\'+folderpath+'_Axon.npy', allow_pickle=True).item()
    pixel_dendrite_dir = np.load('.\\Temp_Data\\'+folderpath+'_Dendrite.npy', allow_pickle=True).item()
    pixel_bouton_dir = np.load('.\\Temp_Data\\'+folderpath+'_Bouton.npy', allow_pickle=True).item()

    cube_map = np.load('.\\Temp_Data\\'+folderpath+'_Cube_Map.npy', allow_pickle=True).item()
    cube_dict = np.load('.\\Temp_Data\\'+folderpath+'_Cube_Dict.npy', allow_pickle=True).item()
    if len(pixel_axon_dir)==0:
        print(folderpath+" axon no data")
    if len(pixel_dendrite_dir)==0:
        print(folderpath+" dendrite no data")
    if len(pixel_bouton_dir)==0:
        print(folderpath+" bouton no data")

    # convert to set
    for k in pixel_axon_dir:
        pixel_axon_set[k]=set(pixel_axon_dir[k])
    for k in pixel_dendrite_dir:
        pixel_dendrite_set[k]=set(pixel_dendrite_dir[k])
        
    # calculate the overlapping list between two sets
    connectmap=[]
    for root, dirs, files in os.walk('./Out_Data_'+folderpath):
        for f1 in files:
            for f2 in files:
                if f1==f2:
                    continue
                n1=f1.split('.')[0]
                n2=f2.split('.')[0]
                t1=pixel_axon_set[n1]
                t2=pixel_dendrite_set[n2]
                if len(t1)==0 or len(t2)==0:
                    print('no data')
                    continue
                total=list(t1 & t2)
                if len(total)!=0:
                    connectmap.append([n1,n2,total]) 
                   
    connectmap_new=[]
    # calculate the connection strength based on the overlapping cubes
    # count the number of boutons in the corresponding cubes
    for i in range(0,len(connectmap)):
        from_area=connectmap[i][0]
        to_area=connectmap[i][1]
        if from_area in pixel_bouton_dir.keys():
            count=0
            t1=pixel_bouton_dir[from_area]
            for k in connectmap[i][2]:
                dendrite_l=cube_dict[to_area+'_'+k][1]
                dendrite_p=cube_map[k][1]
                count+=t1.count(k)*dendrite_l/dendrite_p # the number of boutons
            if count>0:
                temp=0
                temp=connectmap[i]
                temp.append(count)
                connectmap_new.append(temp)
    np.save(folderpath+'_connection.npy',np.array(connectmap_new,dtype=list))

def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 4 # set the number of CPUs in parallel
    
    folderpath = ['bouton','boutondensity_all','boutondensity_each']
    
    import time
    time_start = time.time()  # record start time
    with Pool(cpu_worker_num) as p:
        p.map(GenerateMatrix, folderpath)
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Connectivity Matrix time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
    
   
    