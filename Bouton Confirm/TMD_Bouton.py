## 提取一个文件中bouton pair的距离
import navis,os,math,csv,shutil
import matplotlib.pyplot as plt 
import numpy as np
import common 
def BoutonTMDAnalysis(par): # 得补0后的文件
    name,write_path=par[0],par[1]
    with open(os.path.join(r'..\Data\Noregisted\bouton_swc',name)) as file_object:
          contents = file_object.readlines()
          file_object.close()    
    while contents[0][0]=='#':# 删除注释
        del contents[0]
    data=np.zeros((len(contents),9))
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        data[lineid,0:7]=t1
    for i in range(0,len(contents)):
        if data[i,0]==0 or data[i,6]==-1:
            continue
        t1=data[i]
        t2=data[int(t1[6])-1]
        linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
        data[i,7]=linelen
    bouton_pair=dict()
    for k in range(len(data)):
        i=data[k]
        if i[0]==0:
            continue
        if i[1]==5:
            mark=0
            length=0
            t=i
            tt=t
            while tt[6]!=-1:
                t=tt
                length+=t[7]
                if t[1]==5 and t[0]!=i[0] and mark==0:
                    bouton_pair[int(i[0])]=int(t[0])
                    mark=1
                tt=data[int(t[6])-1,:]
            data[k,8]=length
    # res=[[data[bouton_pair[key]-1,8],data[key-1,8],data[key-1,8]-data[bouton_pair[key]-1,8]] for key in bouton_pair.keys()]
    res=[[data[bouton_pair[key]-1,8],data[key-1,8]] for key in bouton_pair.keys()]
    np.save(write_path+name.split(".")[0]+'.npy',res)
def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36
    import time
    time_start = time.time()  # 记录开始时间
    path=r'..\Data\Noregisted\bouton_swc'
    write_path='./TMD_temp/'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    par_list=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([file,write_path])

    with Pool(cpu_worker_num) as p:
        p.map(BoutonTMDAnalysis, par_list)
       
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('TMD get: '+str(time_sum))  


import copy
from scipy import stats
from matplotlib import cm
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

def compute_distances(par):
    name1, name2=par[0],par[1]
    phs_1=np.load('./TMD_temp/'+name1+'.npy',allow_pickle=True)
    phs_2=np.load('./TMD_temp/'+name2+'.npy',allow_pickle=True)
    phs1,phs2=[phs_1],[phs_2]
    """Compute distances."""
    # Normalize the limits
    xlim, ylim = get_limits(phs1 + phs2)

    # Create average images for populations
    IMG1 = get_average_persistence_image(phs1, xlim=xlim, ylim=ylim)

    IMG2 = get_average_persistence_image(phs2, xlim=xlim, ylim=ylim)

    # Create the difference between the two images
    # Subtracts IMG2 from IMG1 so anything red IMG1 has more of it and anything blue IMG2 has more
    # of it - or that's how it is supposed to be :)
    DIMG = get_image_diff_data(IMG1, IMG2)


    dist = np.sum(np.abs(DIMG))
    f=open('./TMD_dis/'+name1+'-'+name2+'.txt','w+')
    f.write(str(dist))
    f.close()

def get_distance():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36
    import time
    time_start = time.time()  # 记录开始时间
    path=r'..\Data\Noregisted\bouton_swc'
    write_path='./TMD_dis/'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)

    par_list=[]
    for root, dirs, files in os.walk(path):
        for i in range(len(files)):
            for j in range(i+1,len(files)):
               par_list.append([files[i].split('.')[0],files[j].split('.')[0]])
    with Pool(cpu_worker_num) as p:
        p.map(compute_distances, par_list)
       
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Distance Get: '+str(time_sum))  


if __name__ =='__main__':
    # run__pool()
    # get_distance()
    path=r'..\Data\Noregisted\bouton_swc'

    for root, dirs, files in os.walk(path):
        neuron_list=[x.split('.')[0] for x in files]
    #     heatmap=np.ones((len(files),len(files)))
    #     for i in range(len(files)):
    #         for j in range(i+1,len(files)):
    #             name1,name2=files[i].split('.')[0],files[j].split('.')[0]
    #             with open('./TMD_dis/'+name1+'-'+name2+'.txt') as file_object:
    #                 contents = file_object.readlines()
    #                 file_object.close()
    #             t=float(contents[0])
    #             heatmap[i,j]=t
    #             heatmap[j,i]=t
    # np.save("heatmap.npy",heatmap)
    heatmap=np.load('heatmap.npy',allow_pickle=True)
    soma_info=np.load("../Data/Other_Infomation/Soma_info.npy",allow_pickle=True).item()
    cell_type={key:soma_info[key][0] for key in soma_info.keys()}
    
   
    
    select_type=['VPM','CP','LGd','VPL','SSp-m','MOp']
    select_id=[]
    for i in range(len(neuron_list)):
        if cell_type[neuron_list[i]] in select_type:
            select_id.append(i)
    neuron_list=np.array(neuron_list)
    neuron_list=neuron_list[select_id]
    heatmap=heatmap[select_id,:]
    heatmap=heatmap[:,select_id]
    
    for i in range(len(heatmap)):
        heatmap[i,i]=1000000
    
    ## 统计最大的10对
    res=[]
    for step in range(100):
        tt=np.where(heatmap==heatmap.min())
        x=tt[0][0]
        y=tt[1][0]
        n1=neuron_list[x]
        n2=neuron_list[y]
        if n1.split("_")[0]==n2.split("_")[0]:
            res.append([neuron_list[x],cell_type[neuron_list[x]],neuron_list[y],cell_type[neuron_list[y]],heatmap[x,y]])
        heatmap[x,y]=1000000
        heatmap[y,x]=1000000
    res=np.array(res)    
    
    # type_set=list(set([cell_type[x] for x in cell_type.keys()]))
    # type_count={x:0 for x in type_set}
    # for x in cell_type.keys():
    #     t=cell_type[x]
    #     type_count[t]=type_count[t]+1
    # temp= sorted(type_count.items(), key=lambda d:d[1], reverse = True)
    
    # color_list = ["#FF0000","#00FF00","#0000FF","#FFFF00","#FF00FF","#00FFFF",
    #               "#FF8000","#80FF00","#8000FF","#FFFF80","#FF80FF","#80FFFF"]
    # color_dict=dict()
    # top_id=6
    # for i in range(len(temp)):
    #     if i < top_id:
    #         color_dict[temp[i][0]]=color_list[i]
    #     else:
    #         color_dict[temp[i][0]]="#FFFFFF"
    # row_colors = [color_dict[cell_type[x]] for x in neuron_list]
    # heatmap=np.log10(heatmap)
    # import seaborn as sns
    # plt.close('all')
    # sns.clustermap(heatmap, cmap='Oranges',method='median',row_colors=row_colors,col_colors=row_colors)
    # for i in range(top_id):
    #     plt.scatter([],[],s=100,c=color_list[i],label=temp[i][0])
    # plt.legend(frameon=False,loc=2, bbox_to_anchor=(1.2,1.0),borderaxespad = 0.)
    # plt.savefig('TMD distance.png', dpi=300)
    
            




