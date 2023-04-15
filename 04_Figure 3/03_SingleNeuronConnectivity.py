'''
Build the dictionary needed for the network connection
'''
import math,os,csv
import numpy as np

global grid
grid=30 # the registration error is about 30um

## read the swc file and construct a list of coverage nodes for axon and dendrite
def PixelCount(pixel_axon_dir,pixel_dendrite_dir,path,name):
    with open(path) as file_object:
        contents = file_object.readlines()
        #print(len(contents))
        file_object.close()
    while contents[0][0]=='#':# delete comments
        del contents[0]
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        t1[2],t1[3],t1[4]=t1[2]/grid,t1[3]/grid,t1[4]/grid
        if t1[0]==0: # invalid data
            continue
        if t1[0]==t1[-1]: # point to itself, reporting a warning
            print('Circle Warning!!! ')
            continue
        # take scale for coordinates
        t1[2:5]=list(map(math.floor,t1[2:5]))
        # non-soma areas
        if int(t1[-1])!=-1:
            if t1[1]==2: # coverage area of axon
                x=str(t1[2])+'_'+str(t1[3])+'_'+str(t1[4])
                pixel_axon_dir[name].append(x)
            elif t1[1]==3 or t1[1]==4: # coverage area of dendrite
                x=str(t1[2])+'_'+str(t1[3])+'_'+str(t1[4])
                pixel_dendrite_dir[name].append(x)
    return pixel_axon_dir,pixel_dendrite_dir

## construct a list of coverage bouton nodes
def BoutonCount(path,pixel_bouton_dir):
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(path, file)) as file_object:
                contents = file_object.readlines()
                #print(len(contents))
                file_object.close()
                name=file.split('.')[0]
                pixel_bouton_dir[name]=[]
            for lineid in range(0,len(contents)):
                if contents[lineid][0]=='#': # skip comments
                    continue  
                x=contents[lineid]
                x=x.strip("\n")
                t1=x.split( )
                t2=list(map(float,t1))
                t2[0],t2[1],t2[2]=t2[0]/grid,t2[1]/grid,t2[2]/grid 
                t2=list(map(math.floor,t2))
                x=str(t2[0])+'_'+str(t2[1])+'_'+str(t2[2])
                pixel_bouton_dir[name].append(x)
    return pixel_bouton_dir

## main function
def GenerateNpy(folderpath):
    path='../Data/'+folderpath+'_swc'
    # build data indexes
    pixel_axon_dir=dict()
    pixel_dendrite_dir=dict()
    pixel_bouton_dir=dict()
    
    # calculate axon and dendrite coverage
    for root, dirs, files in os.walk(path):
        for f in files:
            name=f.split('.')[0]
            pixel_axon_dir[name]=[]
            pixel_dendrite_dir[name]=[]
            pixel_axon_dir,pixel_dendrite_dir=PixelCount(pixel_axon_dir,pixel_dendrite_dir,os.path.join(root,f),name)
            
    np.save('.\\Temp_Data\\'+folderpath+'_Axon.npy', pixel_axon_dir)
    np.save('.\\Temp_Data\\'+folderpath+'_Dendrite.npy', pixel_dendrite_dir)
    
    # calculate bouton coverage
    pixel_bouton_dir=BoutonCount('../Data/'+folderpath,pixel_bouton_dir)
    np.save('.\\Temp_Data\\'+folderpath+'_Bouton.npy', pixel_bouton_dir)

    # length of dendrite or axon in a cube
    with open('.\\Temp_Data\\Dataset_Cube_'+folderpath+".csv") as f:
        reader = csv.reader(f)
        cube_data=np.array(list(reader))
        f.close
    global cube_map
    cube_map=dict()
    for x in cube_data:
        if float(x[2])!=0:
            cube_map[str(x[0])]=[float(x[1]),float(x[2])]

    # each neuron's dictionary of dendrite within each cube
    with open('.\\Temp_Data\\Dataset_Soma_'+folderpath+".csv") as f:
        reader = csv.reader(f)
        cube_data=np.array(list(reader))
        f.close
    global cube_dict
    cube_dict=dict()
    for x in cube_data:
        cube_dict[str(x[0])+'_'+x[1]]=[float(x[2]),float(x[3])]
    np.save('.\\Temp_Data\\'+folderpath+"_Cube_Map.npy",cube_map)
    np.save('.\\Temp_Data\\'+folderpath+"_Cube_Dict.npy",cube_dict)

def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 4 # set the number of CPUs in parallel
    
    folderpath = ['bouton','boutondensity_all','boutondensity_each']
    
    import time
    time_start = time.time()  # record start time
    with Pool(cpu_worker_num) as p:
        p.map(GenerateNpy, folderpath)
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Connectivity Npy file time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
     
    
    