## 将含有bouton的文件转换为对应的均匀分布的数据
import os,math,shutil,csv
import numpy as np
import matplotlib.pyplot as plt 
global add_method
# add_method='Noregisted/' #决定是对noregist的数据，还是注册后的数据
add_method=''
global path
path=r'./'+add_method+'bouton_swc'
def BoutondensityChange(par):
    name,bouton_density_p,writepath=par[0],1/par[1],par[2]
    with open(os.path.join(path,name)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    data=[]
    while contents[0][0]=='#':# 删除注释
        del contents[0]
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        data.append(t1+[0,0])
    # 计算节点距离和数量
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
    # 重新赋值bouton
    for i in range(0,len(data)):
        if data[i,7]==0 and data[i,1]==2: #axon叶子节点
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
    # 获取神经元所在脑区的信息
    with open(r'..\Data\Other_Infomation\BoutonDataCellType.csv', 'r', newline='') as csvfile:
        t = csv.reader(csvfile)
        area_data=np.array(list(t))
        csvfile.close()
    cell_type=dict()
    for f in files:
        t=f.split('.')[0]
        tt=np.where(area_data[:,0]==t)
        if len(tt[0])==0:
            print(t+' out of file')
        else:
            cell_type[f]=str(area_data[tt[0],1][0])
    
    from multiprocessing import Pool
    cpu_worker_num = 36
    import time
    time_start = time.time()  # 记录开始时间
    
    bouton_density_p=0.061
    ## 所有cell type共用一个boutondensity
    writepath='./'+add_method+'boutondensity_all_swc'
    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)
    par_list=[]
    for x in file:
        par_list.append((x,bouton_density_p,writepath))
    
    with Pool(cpu_worker_num) as p:
        p.map(BoutondensityChange, par_list)
    
    ## 每个cell type有自己的boutondensity
    best_par=np.load(r'.\Other_Infomation\best_density.npy', allow_pickle=True).item()  
    writepath='./'+add_method+'boutondensity_each_swc'
    if os.path.exists(writepath):
        shutil.rmtree(writepath)  
    os.mkdir(writepath)
    par_list=[]
    for x in file:
        par_list.append((x,best_par[cell_type[x]]*bouton_density_p,writepath))

    with Pool(cpu_worker_num) as p:
        p.map(BoutondensityChange, par_list)
    
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Boutondensity Change time: '+str(time_sum))  

# 提取出bouton的坐标点
def GetBouton(par):
    file,bouton_path,bouton_write_path=par[0],par[1],par[2]
    with open(os.path.join(bouton_path, file)) as file_object:
        contents = file_object.readlines()
        #print(len(contents))
        file_object.close()
    new_content=[]
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# 跳过注释
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
    cpu_worker_num = 36
    import time
    time_start = time.time()  # 记录开始时间
    # 提取bouton位置
    bouton_path='./'+add_method+'bouton_swc'
    bouton_write_path=r'./'+add_method+'/bouton'
    if os.path.exists(bouton_write_path):
        shutil.rmtree(bouton_write_path)  
    os.mkdir(bouton_write_path)
    par_list=[]
    for root, dirs, files in os.walk(bouton_path):
        for file in files:
            par_list.append([file,bouton_path,bouton_write_path])
    with Pool(cpu_worker_num) as p:
        p.map(GetBouton, par_list)
    
    bouton_path=r'./'+add_method+'/boutondensity_all_swc'
    bouton_write_path=r'./'+add_method+'/boutondensity_all'
    if os.path.exists(bouton_write_path):
        shutil.rmtree(bouton_write_path)  
    os.mkdir(bouton_write_path) 
    par_list=[]
    for root, dirs, files in os.walk(bouton_path):
        for file in files:
            par_list.append([file,bouton_path,bouton_write_path])
    with Pool(cpu_worker_num) as p:
        p.map(GetBouton, par_list)
    
    bouton_path=r'./'+add_method+'/boutondensity_each_swc'
    bouton_write_path=r'./'+add_method+'/boutondensity_each'
    if os.path.exists(bouton_write_path):
        shutil.rmtree(bouton_write_path)  
    os.mkdir(bouton_write_path) 
    par_list=[]
    for root, dirs, files in os.walk(bouton_path):
        for file in files:
            par_list.append([file,bouton_path,bouton_write_path])
    with Pool(cpu_worker_num) as p:
        p.map(GetBouton, par_list)
    
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Boutondensity Change time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
    run_pool_Getbouton()
    
    
    