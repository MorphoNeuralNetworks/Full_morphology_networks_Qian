# 使用noregist的数据进行分析
import navis,os,math,csv
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
import shutil
global step
step=100

def BoutonShollAnalyse(content,step): # 得补0后的文件
    contents=content
    while contents[0][0]=='#':# 删除注释
        del contents[0]
    data=np.zeros((len(contents),8))
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
    bouton_distance=[]
    for i in data:
        if i[1]==5:
            length=0
            t=i
            tt=t
            while tt[6]!=-1:
                t=tt
                length+=t[7]
                tt=data[int(t[6])-1,:]
            bouton_distance.append(length)
    # 构建字典
    hist=plt.hist(bouton_distance,range=(0,math.ceil(max(bouton_distance)/step)*step),bins=math.ceil(max(bouton_distance)/step))
    # print(max(bouton_distance))
    plt.close()
    return hist[0]

## 消除0行和dendrite用于sholl analysis
def TempFileInit(par):
    path,name=par[0],par[1]
    with open(os.path.join(path,name)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    new_contents=[]
    for i in range(0,len(contents)):
        x=contents[i]
        t1=x.split( )
        t1=list(map(float,t1))
        new_contents.append(t1)
    visited=np.zeros((1,len(contents)))
    for i in range(0,len(contents)):
        if visited[0,i]!=0:
            continue
        if new_contents[i][6]==-1:
            visited[0,i]=1
            continue
        if new_contents[i][1]==2 or new_contents[i][1]==5:
            visited[0,i]=1
            t1=i
            t2=int(new_contents[i][6])-1
            while visited[0,t2]==0:
                t1=t2
                visited[0,t1]=1
                t2=int(new_contents[t1][6])-1
    for i in range(len(contents)-1,-1,-1):
        if visited[0,i]==0:
            del contents[i]
    for i in range(len(contents)-1,-1,-1):
            if contents[i][0]=='0':
                del contents[i]
    f=open('./temp_data/'+name,'w+')
    f.writelines(contents)
    f.close()

## 所有神经元的均值分布
def ShollAnalysis(name):
    with open(os.path.join(r'..\Data\Noregisted\bouton_swc',name)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    bouton_sholl=BoutonShollAnalyse(contents,step)
    # sholl analysis
    s = navis.read_swc('./temp_data/'+name)
    s_sha = navis.sholl_analysis(s, center='root', radii=np.linspace(0, step*len(bouton_sholl), len(bouton_sholl)+1), geodesic=True, parallel=True)
    sholl_temp=np.array([bouton_sholl,s_sha.cable_length.values,s_sha.branch_points.values])
    np.save('./sholl_temp/'+name.replace('.swc','.npy'),sholl_temp)

def ShollAnalysisDensity(name):
    with open(os.path.join(r'..\Data\Noregisted\boutondensity_each_swc',name)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    bouton_sholl=BoutonShollAnalyse(contents,step)
    np.save('./sholl_temp/'+name.replace('.swc','.npy'),bouton_sholl)

def run_pool():
    from multiprocessing import Pool
    cpu_worker_num = 36
    
    path=r'..\Data\Noregisted\bouton_swc'
    # 去除0之后的文件 清空文件夹
    shutil.rmtree('./temp_data')  
    os.mkdir('./temp_data')
    shutil.rmtree('./sholl_temp')  
    os.mkdir('./sholl_temp')
    par_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for name in files:
            par_list.append((path,name))
    with Pool(cpu_worker_num) as p:
        p.map(TempFileInit, par_list)     
    # sholl analysis
    for root,dirs,files in os.walk(r'..\Data\Noregisted\bouton_swc',topdown=True):
        with Pool(cpu_worker_num) as p:
            p.map(ShollAnalysis, files)     
    
    sholl_result=dict()
    for root,dirs,files in os.walk(r'.\sholl_temp',topdown=True):
        for f in files:
            temp=np.load('./sholl_temp/'+f, allow_pickle=True)
            sholl_result[f.split('.')[0]]=temp
    np.save('sholl_result.npy',sholl_result)
    
    path=r'..\Data\Noregisted\boutondensity_each_swc'
    # 去除0之后的文件 清空文件夹
    shutil.rmtree('./temp_data')  
    os.mkdir('./temp_data')
    shutil.rmtree('./sholl_temp')  
    os.mkdir('./sholl_temp')
    par_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for name in files:
            par_list.append((path,name))
    with Pool(cpu_worker_num) as p:
        p.map(TempFileInit, par_list)     
    # sholl analysis
    for root,dirs,files in os.walk(r'..\Data\Noregisted\boutondensity_each_swc',topdown=True):
        with Pool(cpu_worker_num) as p:
            p.map(ShollAnalysisDensity, files)     
    
    sholl_result=dict()
    for root,dirs,files in os.walk(r'.\sholl_temp',topdown=True):
        for f in files:
            temp=np.load('./sholl_temp/'+f, allow_pickle=True)
            sholl_result[f.split('.')[0]]=temp
    np.save('sholl_result_density_each.npy',sholl_result)

if __name__ =='__main__':
    run_pool()
    # pass

    
    # # Plot one of the inhibitory neurons
    # plt.close('all')
    # name_list=[
    # '18455_00015.swc',
    # '18455_00020.swc',
    # '18455_00021.swc',
    # '18455_00022.swc',
    # '18455_00047.swc',
    # '18455_00048.swc',
    # '18455_00049.swc']
    # for name in name_list[0:2]:
    #     with open(os.path.join(r'..\Data\Noregisted\bouton_swc',name)) as file_object:
    #         contents = file_object.readlines()
    #         file_object.close()
    #     bouton_sholl=BoutonShollAnalyse(contents,step)
    #     # sholl analysis
    #     s = navis.read_swc('./temp_data/'+name)
    #     s_sha = navis.sholl_analysis(s, center='root', radii=np.linspace(0, step*len(bouton_sholl), len(bouton_sholl)+1), geodesic=True, parallel=True)
    #     ix = 0
    #     fig, ax = navis.plot2d(s, view=('x', 'y'), figsize=(12, 12), c='r', method='2d')
        
    #     cmap = plt.get_cmap('viridis')
        
    #     # Plot Sholl circles and color by number of intersections
    #     center = s.soma_pos
    #     norm = Normalize(vmin=0, vmax=(max(bouton_sholl) + 1))
    #     count=0
    #     for r in s_sha.index.values:
    #         ints = bouton_sholl[count]
    #         count+=1
    #         ints_norm = norm(ints)
    #         color = cmap(ints_norm)
        
    #         c=plt.Circle(xy=center[0,0:2], radius=r, ec=color,fc='none')
    #         ax.add_patch(p=c)
        
    #     # # # Add colorbar
    #     # divider = make_axes_locatable(ax)
    #     # cax = divider.append_axes("right", size="5%", pad=0.05)
    #     # plt.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cax, label='Boutons')
        
    #     # plt.show()
    