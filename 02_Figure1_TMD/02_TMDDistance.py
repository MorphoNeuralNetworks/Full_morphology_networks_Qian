'''
## Analysis of structure and bouton distribution using TMD functions

# The following function needs to be added to the tmd/Tree/method.py file
def get_point_radial_enclosed_boutons(self, point=None, dim="xyz"):
    if point is None:
        point = []
        for d in dim:
            point.append(getattr(self, d)[0])

    bouton_distances = np.zeros(0, dtype=float)

    is_bouton = (getattr(self, "t") == 5)
    for i in range(size(self)):
        bouton_dest = []
        if is_bouton[i] == True:
            for d in dim:
                bouton_dest.append(getattr(self, d)[i])
            bouton_distances = np.append(bouton_distances,_rd(point, bouton_dest))

    radial_distances = np.zeros(size(self), dtype=float)
    radial_boutons = np.zeros(size(self), dtype=float)

    for i in range(size(self)):
        point_dest = []
        for d in dim:
            point_dest.append(getattr(self, d)[i])
        radial_distances[i] = _rd(point, point_dest)
        radial_boutons[i] = sum(bouton_distances<=radial_distances[i])

    return np.log10(radial_boutons+1)
# and declare this function in the tmd/Tree/Tree.py file
from tmd.Tree.methods import get_point_radial_enclosed_boutons

# Change the return value of 
get_point_radial_distances(self, point=None, dim='xyz'):
    ......
    return radial_distances
# to
get_point_radial_distances(self, point=None, dim='xyz'):
    ......
    return np.log10(radial_distances+1)
'''

import tmd
import os,shutil
import numpy as np

## TMD analysis of the bouton
def GetPhDataBouton(par):
    try:
        name,path,write_path=par[0],par[1],par[2]
        dict_types ={
        1:"soma",
        2:"axon",
        3:"basal_dendrite",
        4:"apical_dendrite",
        5:"axon"
        }
        nrn = tmd.io.load_neuron(path+name,user_tree_types=dict_types)
        ph = tmd.methods.get_ph_neuron(nrn, neurite_type="axon", feature="radial_enclosed_boutons")
        np.save(write_path+name.split(".")[0]+'.npy',ph)
    except:
        print(par)

## TMD analysis of the whole structure
def GetPhDataDefault(par):
    try:
        name,path,write_path=par[0],par[1],par[2]
        dict_types ={
        1:"soma",
        2:"axon",
        3:"basal_dendrite",
        4:"apical_dendrite",
        5:"bouton"
        }
        nrn = tmd.io.load_neuron(path+name,user_tree_types=dict_types)
        ph = tmd.methods.get_ph_neuron(nrn, neurite_type="axon")
        np.save(write_path+name.split(".")[0]+'.npy',ph)
    except:
        print(par)

def run_GetPhData_pool(method="default"):  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    
    if method=="default":
        path=r'./bouton_swc_nobouton/'
    elif method=="bouton":
        path=r'./bouton_swc/'
    elif method=="bouton_random":
        path=r'./bouton_swc_random/'
    write_path=r'./bouton_ph_temp/'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    par_list=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([file,path,write_path])
    with Pool(cpu_worker_num) as p:
        if method=="default":
            p.map(GetPhDataDefault, par_list)
        elif method=="bouton" or method=="bouton_random":
            p.map(GetPhDataBouton, par_list)
            
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Get TMD data time: '+str(time_sum))      


## the following functions are taken from the TMD code
## https://github.com/BlueBrain/TMD
import copy
from scipy import stats
def collapse(ph_list):
    """Collapses a list of ph diagrams into a single instance for plotting."""
    return [list(pi) for p in ph_list for pi in p]

def get_limits(phs_list, coll=True):
    """Returns the x-y coordinates limits (min, max) for a list of persistence diagrams."""
    if coll:
        ph = collapse(phs_list)
    else:
        ph = copy.deepcopy(phs_list)
    xlim = [min(np.transpose(ph)[0]), max(np.transpose(ph)[0])]
    ylim = [min(np.transpose(ph)[1]), max(np.transpose(ph)[1])]
    return xlim, ylim

def get_persistence_image_data(ph, norm_factor=None, xlim=None, ylim=None, bw_method=None):
    """Create the data for the generation of the persistence image.
    Args:
        ph: persistence diagram.
        norm_factor: persistence image data are normalized according to this.
            If norm_factor is provided the data will be normalized based on this,
            otherwise they will be normalized to 1.
        xlim: The image limits on x axis.
        ylim: The image limits on y axis.
        bw_method: The method used to calculate the estimator bandwidth for the gaussian_kde.
    If xlim, ylim are provided the data will be scaled accordingly.
    """
    if xlim is None or xlim is None:
        xlim, ylim = get_limits(ph, coll=False)

    X, Y = np.mgrid[xlim[0] : xlim[1] : 100j, ylim[0] : ylim[1] : 100j]

    values = np.transpose(ph)
    kernel = stats.gaussian_kde(values, bw_method=bw_method)
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(kernel(positions).T, X.shape)

    if norm_factor is None:
        norm_factor = np.max(Z)

    return Z / norm_factor

def get_average_persistence_image(ph_list, xlim=None, ylim=None, norm_factor=None, weighted=False):
    """Plot the gaussian kernel of a population as an average of the ph diagrams that are given."""
    im_av = False
    k = 1
    if weighted:
        weights = [len(p) for p in ph_list]
        weights = np.array(weights, dtype=float) / np.max(weights)
    else:
        weights = [1 for _ in ph_list]

    for weight, ph in zip(weights, ph_list):
        if not isinstance(im_av, np.ndarray):
            try:
                im = get_persistence_image_data(ph, norm_factor=norm_factor, xlim=xlim, ylim=ylim)
                if not np.isnan(np.sum(im)):
                    im_av = weight * im
            except BaseException:  # pylint: disable=broad-except
                pass
        else:
            try:
                im = get_persistence_image_data(ph, norm_factor=norm_factor, xlim=xlim, ylim=ylim)
                if not np.isnan(np.sum(im)):
                    im_av = np.add(im_av, weight * im)
                    k = k + 1
            except BaseException:  # pylint: disable=broad-except
                pass
    return im_av / k

def get_image_diff_data(Z1, Z2, normalized=True):
    """Get the difference of two images from the gaussian kernel plotting function."""
    if normalized:
        Z1 = Z1 / Z1.max()
        Z2 = Z2 / Z2.max()
    return Z1 - Z2 

## calculate the distance between two files in parallel and save it as a file
def compute_distances(par):
    name1, name2=par[0],par[1]
    phs_1=np.load('./bouton_ph_temp/'+name1+'.npy',allow_pickle=True)
    phs_2=np.load('./bouton_ph_temp/'+name2+'.npy',allow_pickle=True)
    if len(phs_1)==0 or len(phs_2)==0: # set a large value to an empty file
        #print([name1,name2])
        dist=1000000
    else:
        phs1,phs2=[phs_1],[phs_2]
        """Compute distances."""
        # Normalize the limits
        xlim, ylim = get_limits(phs1 + phs2)
        
        # Create average images for populations
        IMG1 = get_average_persistence_image(phs1, xlim=xlim, ylim=ylim)
        IMG2 = get_average_persistence_image(phs2, xlim=xlim, ylim=ylim)
        if type(IMG1)==float or type(IMG2)==float: # set a large value to an invalid file
            #print([name1,name2])
            dist=1000000
        else:
            DIMG = get_image_diff_data(IMG1, IMG2)
            dist = np.sum(np.abs(DIMG))
    
    f=open('./TMD_dis/'+name1+'-'+name2+'.txt','w+')
    f.write(str(dist))
    f.close()

def get_distance():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 38 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    path=r'./bouton_ph_temp/'
    write_path='./TMD_dis/'
    # empty folder
    if  os.path.exists(write_path):
        shutil.rmtree(write_path)  
    os.mkdir(write_path)

    par_list=[]
    for root, dirs, files in os.walk(path):
        for i in range(len(files)):
            for j in range(i+1,len(files)):
                par_list.append([files[i].split('.')[0],files[j].split('.')[0]])
    with Pool(cpu_worker_num) as p:
        p.map(compute_distances, par_list)
       
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Distance Get: '+str(time_sum))  

## stitch each row of the matrix in parallel
def Combine_files(par):
    write_path,neuron_list,i=par[0],par[1],par[2]
    temp=np.ones(len(neuron_list))
    for j in range(0,len(neuron_list)):
        if j==i:
            continue
        if j<i:
            n1,n2=j,i
        else:
            n1,n2=i,j
        name1,name2=neuron_list[n1],neuron_list[n2]
        if os.path.exists('./TMD_dis/'+name1+'-'+name2+'.txt'): # set a large value to a non-existent file
            with open('./TMD_dis/'+name1+'-'+name2+'.txt') as file_object:
                contents = file_object.readlines()
                file_object.close()
            t=float(contents[0])
            temp[j]=t
        else:
            temp[j]=1000000
    np.save(write_path+neuron_list[i]+".npy",temp)

def run_combine(method):
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
    
    write_path='./combine_temp/'
    # empty folder
    if  os.path.exists(write_path):
        shutil.rmtree(write_path)  
    os.mkdir(write_path)
    
    # combine matrix
    if method=="default":
        path=r'./bouton_swc_nobouton/'
    elif method=="bouton":
        path=r'./bouton_swc/'
    elif method=="bouton_random":
        path=r'./bouton_swc_random/'
    for root, dirs, files in os.walk(path):
        neuron_list=[x.split('.')[0] for x in files]
    par_list=[[write_path,neuron_list,i] for i in range(len(neuron_list))]
    with Pool(cpu_worker_num) as p:
        p.map(Combine_files, par_list)
        
    for root, dirs, files in os.walk(path):
        neuron_list=[x.split('.')[0] for x in files]
        np.save("TMD_"+method+"_list.npy",neuron_list)
        heatmap=np.ones((len(files),len(files)))
        for i in range(len(neuron_list)):
              if i%100==0:
                  print(i)
              temp=np.load("./combine_temp/"+neuron_list[i]+".npy",allow_pickle=True)
              heatmap[:,i]=temp
        np.save(method+"_default.npy",heatmap)
        
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Combine file: '+str(time_sum))

if __name__ =='__main__':
    method="default" # "bouton","bouton_random"
    run_GetPhData_pool(method)
    get_distance()
    run_combine(method)
    