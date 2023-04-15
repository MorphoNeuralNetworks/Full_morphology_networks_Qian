'''
Get sholl analysis results for all neurons
'''
import navis,os,math
import matplotlib.pyplot as plt 
import numpy as np
import shutil

global step
step=100 # set the interval distance of sholl analysis
global method
method="each"
# method="all" # decide whether to use the respective boutondensity or the same

## calculation of bouton's sholl analysis
def BoutonShollAnalyse(content,step):
    contents=content
    while contents[0][0]=='#': # delete comments
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
    # build dictionary
    hist=plt.hist(bouton_distance,range=(0,math.ceil(max(bouton_distance)/step)*step),bins=math.ceil(max(bouton_distance)/step))
    # print(max(bouton_distance))
    plt.close()
    return hist[0]

## remove zero lines and dendrite for Navis sholl analysis
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

## results of sholl analysis for real data
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

## for uniform case only get the bouton sholl analysis
def ShollAnalysisDensity(name):
    with open(os.path.join('../Data/Noregisted/boutondensity_'+method+'_swc',name)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    bouton_sholl=BoutonShollAnalyse(contents,step)
    np.save('./sholl_temp/'+name.replace('.swc','.npy'),bouton_sholl)

def run_pool():
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    
    ## real data
    path=r'..\Data\Noregisted\bouton_swc'
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
    
    ## uniform case
    path=r'../Data/Noregisted/boutondensity_'+method+'_swc'
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
    for root,dirs,files in os.walk(r'../Data/Noregisted/boutondensity_'+method+'_swc',topdown=True):
        with Pool(cpu_worker_num) as p:
            p.map(ShollAnalysisDensity, files)     
    
    ## summarize the data
    sholl_result=dict()
    for root,dirs,files in os.walk(r'.\sholl_temp',topdown=True):
        for f in files:
            temp=np.load('./sholl_temp/'+f, allow_pickle=True)
            sholl_result[f.split('.')[0]]=temp
    np.save('../Data/Temp_Data/sholl_result_density_'+method+'.npy',sholl_result)

if __name__ =='__main__':
    run_pool()
    