import os,math,csv
import numpy as np
import matplotlib.pyplot as plt 
import shutil

# 统计两个点之间的距离，用于辅助判断
def PointDistance(name):
    path=r'..\Data\bouton_swc_noregist'
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
    point_dis=[]
    for i in range(0,len(data)):
        if data[i,0]==0 or data[i,6]==-1:
            continue
        if data[i,1]==2:
            t1=data[i]
            t2=data[int(t1[6])-1]
            linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
            point_dis.append(linelen)
    point_dis=np.array(point_dis)
    np.save('./Point_Distance/'+name.split('.')[0]+'.npy',point_dis)
'''
# 如果使用boutondensity的情况
def BoutondensityStat(name):
    # name='17302_00048.swc' # branch order max
        # name='18457_00136.swc' # branch order max
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
                
    bouton_stat=[]
    # 统计bouton信息
    for x in data:
        if x[1]==5:
            x_t=x
            branch_count=0
            branch_order=1
            mark=0
            axonlen=0
            while x_t[6]!=-1:
                x_t=data[int(x[6])-1]
                if x_t[1]==5 and mark==0:
                    mark=1
                if mark==0 and x_t[7]>1:
                    branch_count+=1
                if x_t[7]>1:
                    branch_order+=1
                if axonlen<bouton_density_p: 
                    axonlen+=x[8]
                x=x_t
            if mark==1:
                bouton_stat.append([name.split('.')[0],branch_count,axonlen,branch_order])
    bouton_stat=np.array(bouton_stat)
    np.save('./Boutondensity_Stat/'+name.split('.')[0]+'.npy',bouton_stat)
'''
def BoutondensityStat(par):
    name,bouton_density_p=par[0],1/par[1]
    path=r'..\Data\Noregisted\boutondensity_each_swc'
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
    bouton_stat=[]
    # 统计bouton信息
    for x in data:
        if x[1]==5:
            x_t=x
            branch_count=0
            branch_order=1
            mark=0
            axonlen=0
            while x_t[6]!=-1:
                x_t=data[int(x[6])-1]
                if x_t[1]==5 and mark==0:
                    mark=1
                if mark==0 and x_t[7]>1:
                    branch_count+=1
                if x_t[7]>1:
                    branch_order+=1
                if axonlen<bouton_density_p: 
                    axonlen+=x[8]
                x=x_t
                # x_t=data[int(x[6])-1]
                # if x_t[1]==5 and mark==0:
                #     mark=1
                #     axonlen+=x[8]
                # if mark==0:
                #     axonlen+=x[8]
                # if mark==0 and x_t[7]>1:
                #     branch_count+=1
                # if x_t[7]>1:
                #     branch_order+=1
                # x=x_t
            if mark==1:
                bouton_stat.append([name.split('.')[0],branch_count,axonlen,branch_order])
    bouton_stat=np.array(bouton_stat)
    np.save('./Boutondensity_Stat/'+name.split('.')[0]+'.npy',bouton_stat)
    
def BoutonStat(name):
    path=r'..\Data\Noregisted\bouton_swc'
    # name='18457_00136.swc'
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
    bouton_stat=[]
    # 统计bouton信息
    for x in data:
        if x[1]==5:
            x_t=x
            branch_count=0
            axonlen=0
            branch_order=1
            mark=0
            while x_t[6]!=-1:
                x_t=data[int(x[6])-1]
                if x_t[1]==5 and mark==0:
                    mark=1
                    axonlen+=x[8]
                if mark==0:
                    axonlen+=x[8]
                if mark==0 and x_t[7]>1:
                    branch_count+=1
                if x_t[7]>1:
                    branch_order+=1
                x=x_t
            if mark==1:
                bouton_stat.append([name.split('.')[0],branch_count,axonlen,branch_order])
    bouton_stat=np.array(bouton_stat)
    np.save('./Bouton_Stat/'+name.split('.')[0]+'.npy',bouton_stat)

def run__pool():  # main process
    
    from multiprocessing import Pool
    cpu_worker_num = 36
    import time
    time_start = time.time()  # 记录开始时间
    
    path=r'..\Data\Noregisted\bouton_swc'
    for root,dirs,files in os.walk(path,topdown=True):
        file=files
    # with Pool(cpu_worker_num) as p:
    #     p.map(BoutonStat, file)
    
    path=r'..\Data\Noregisted\boutondensity_each_swc'
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
    bouton_density_p=0.061
    best_par=np.load(r'..\Data\Other_Infomation\best_density.npy', allow_pickle=True).item()
    par_list=[]
    for x in file:
        par_list.append((x,best_par[cell_type[x]]*bouton_density_p))
    
    with Pool(cpu_worker_num) as p:
        p.map(BoutondensityStat, par_list)
    # shutil.rmtree('./Point_Distance')
    # os.mkdir('./Point_Distance')
    # with Pool(cpu_worker_num) as p:
    #     p.map(PointDistance, file)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Bouton distribution time: '+str(time_sum))  

if __name__ =='__main__':
    
    # if os.path.exists('./Bouton_Stat'):
    #     shutil.rmtree('./Bouton_Stat')
    # os.mkdir('./Bouton_Stat')
    
    # if os.path.exists('./Boutondensity_Stat'):
    #     shutil.rmtree('./Boutondensity_Stat')
    # os.mkdir('./Boutondensity_Stat')
    # run__pool()
    # bouton_stat=[]
    # for root,dirs,files in os.walk('./Bouton_Stat',topdown=True):
    #     for f in files:
    #         temp=np.load('./Bouton_Stat/'+f,allow_pickle=True)
    #         bouton_stat=bouton_stat+temp.tolist()
    # bouton_stat=np.array(bouton_stat)
    # np.save('bouton_stat.npy',bouton_stat)
    
    # boutondensity_stat=[]
    # for root,dirs,files in os.walk('./Boutondensity_Stat',topdown=True):
    #     for f in files:
    #         temp=np.load('./Boutondensity_Stat/'+f,allow_pickle=True)
    #         boutondensity_stat=boutondensity_stat+temp.tolist()
    # bouton_stat=np.array(boutondensity_stat)
    # np.save('boutondensity_stat.npy',boutondensity_stat)
    
    # point_dis=[]
    # for root,dirs,files in os.walk('./Point_Distance',topdown=True):
    #     for f in files:
    #         temp=np.load('./Point_Distance/'+f,allow_pickle=True)
    #         point_dis=point_dis+temp.tolist()
    # point_dis=np.array(point_dis)
    # np.save('point_distance.npy',point_dis)
    # point_dis=np.load('point_distance.npy',allow_pickle=True)
    # db=plt.hist(point_dis,range=(0,200),bins=round(max(point_dis/10)))
    # x=[]
    # y=[]
    # for i in db[1]:
    #     x.append(i+1)
    # for i in db[0]:
    #     y.append(i+1)
    # x=x[1:]
    # # x=np.log10(x)
    # y=np.log10(y)
    
    # 获取神经元所在脑区的信息
    with open(r'..\Data\Other_Infomation\BoutonDataCellType.csv', 'r', newline='') as csvfile:
        t = csv.reader(csvfile)
        area_data=np.array(list(t))
        csvfile.close()
    cell_type=dict()
    for root, dirs, files in os.walk(r'..\Data\Noregisted\bouton_swc'):
        for file in files:
            t=file.split('.')[0]
            tt=np.where(area_data[:,0]==t)
            if len(tt[0])==0:
                print(t+' out of file')
            else:
                cell_type[file.split('.')[0]]=str(area_data[tt[0],1][0])
    
    bouton_stat=np.load('bouton_stat.npy',allow_pickle=True)
    boutondensity_stat=np.load('boutondensity_stat.npy',allow_pickle=True)
    bouton_name=bouton_stat[:,0]
    boutondensity_name=boutondensity_stat[:,0]
    name='SSp-m'
    t=[]
    for i in range(0,len(bouton_name)):
        if i%10000==0:
            print(i)
        if cell_type[str(bouton_name[i])]==name or name=='all':
            t.append(i)
    bouton_stat=bouton_stat[t,1:4].astype(np.float64)
    t=[]
    for i in range(0,len(boutondensity_name)):
        if i%10000==0:
            print(i)
        if cell_type[str(boutondensity_name[i])]==name or name=='all':
            t.append(i)
    boutondensity_stat=boutondensity_stat[t,1:4].astype(np.float64)

    db=plt.hist(bouton_stat[:,1],bins=round(max(bouton_stat[:,1])/10))
    x=[]
    y=[]
    for i in db[1]:
        x.append(i+1)
    for i in db[0]:
        y.append(i+1)
    x=x[1:]
    x=np.log10(x)
    y=np.log10(y)
    
    dbd=plt.hist(boutondensity_stat[:,1],bins=round(max(boutondensity_stat[:,1])/10))
    x_bd=[]
    y_bd=[]
    for i in dbd[1]:
        x_bd.append(i+1)
    for i in dbd[0]:
        y_bd.append(i+1)
    x_bd=x_bd[1:]
    x_bd=np.log10(x_bd)
    y_bd=np.log10(y_bd)
    
    from scipy.stats import ks_2samp
    print(ks_2samp(bouton_stat[:,1],boutondensity_stat[:,1]))
    
    plt.close()
    fig,ax=plt.subplots(figsize=(6,4))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.scatter(x,y,alpha=0.7)
    plt.scatter(x_bd,y_bd,alpha=0.7)
    plt.xticks([0,1,2,3,4],['1','10','100','1000','10000'],fontsize=18,fontproperties='Calibri',weight='bold')
    plt.yticks([0,1,2,3,4,5,6],['1','10','100','1e3','1e4','1e5','1e6'],fontsize=18,fontproperties='Calibri',weight='bold')
    # plt.legend(['Experimental bouton','Uniform bouton'],prop={'family':'Calibri','weight':'bold','size':16},frameon=False)
    # plt.xlabel('Path length(um)',fontsize=22,fontproperties='Calibri',weight='bold')
    # plt.ylabel('Frequency(log)',fontsize=22,fontproperties='Calibri',weight='bold')
    # plt.title('Distribution of path length betwen axon boutons',fontsize=14)
    plt.tight_layout()
    # plt.savefig(name+'_Distribution of path length betwen axon boutons.png', dpi=300)

    db=plt.hist(bouton_stat[:,0],bins=round(max(bouton_stat[:,0])))
    x=[]
    y=[]
    for i in db[1]:
        x.append(i+1)
    for i in db[0]:
        y.append(i+1)
    x=x[1:]
    # x=np.log10(x)
    y=np.log10(y)
    
    dbd=plt.hist(boutondensity_stat[:,0],bins=round(max(boutondensity_stat[:,0])))
    x_bd=[]
    y_bd=[]
    for i in dbd[1]:
        x_bd.append(i+1)
    for i in dbd[0]:
        y_bd.append(i+1)
    x_bd=x_bd[1:]
    # x_bd=np.log10(x_bd)
    y_bd=np.log10(y_bd)
    from scipy.stats import ks_2samp
    print(ks_2samp(bouton_stat[:,0],boutondensity_stat[:,0]))
    
    plt.close()
    fig,ax=plt.subplots(figsize=(6,4))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.scatter(x,y,alpha=0.7)
    plt.scatter(x_bd,y_bd,alpha=0.7)
    plt.xticks([0,5,10,15,20],['0','5','10','15','20'],fontsize=18,fontproperties='Calibri',weight='bold')
    plt.yticks([0,1,2,3,4,5,6],['1','10','100','1e3','1e4','1e5','1e6'],fontsize=18,fontproperties='Calibri',weight='bold')
    # plt.legend(['bouton','boutondensity'],fontsize=14)
    # plt.xlabel('number of branch points',fontsize=22,fontproperties='Calibri',weight='bold')
    # plt.ylabel('Frequency(log)',fontsize=14)
    # plt.title('Distribution of branch points between axon boutons',fontsize=14)
    plt.tight_layout()
    # plt.savefig(name+'_Distribution of branch points between axon boutons.png', dpi=300)

    db=plt.hist(bouton_stat[:,2],bins=round(max(bouton_stat[:,2])))
    x=[]
    y=[]
    for i in range(0,len(db[0])):
        if db[0][i]!=0:
            x.append(db[1][i+1]+1)
            y.append(db[0][i]+1)
    # x=np.log10(x)
    y=np.log10(y)
    
    dbd=plt.hist(boutondensity_stat[:,2],bins=round(max(boutondensity_stat[:,2])))
    x_bd=[]
    y_bd=[]
    for i in range(0,len(dbd[0])):
        if dbd[0][i]!=0:
            x_bd.append(dbd[1][i+1]+1)
            y_bd.append(dbd[0][i]+1)
    # x_bd=np.log10(x_bd)
    y_bd=np.log10(y_bd)
    from scipy.stats import ks_2samp
    print(ks_2samp(bouton_stat[:,1],boutondensity_stat[:,1]))
    
    plt.close()
    fig,ax=plt.subplots(figsize=(6,4))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.scatter(x,y)
    plt.scatter(x_bd,y_bd)
    plt.xticks([0,20,40,60,80,100,120],['0','20','40','60','80','100','120'],fontsize=18,fontproperties='Calibri',weight='bold')
    plt.yticks([0,1,2,3,4,5,6,7],['1','10','100','1e3','1e4','1e5','1e6','1e7'],fontsize=18,fontproperties='Calibri',weight='bold')
    # plt.legend(['bouton','boutondensity'],fontsize=14)
    # plt.xlabel('branch order',fontsize=22,fontproperties='Calibri',weight='bold')
    # plt.ylabel('Frequency(log)',fontsize=14)
    # plt.title('Distribution of axon boutons in function of branch order',fontsize=14)
    plt.tight_layout()
    # plt.savefig(name+'_Distribution of axon boutons in function of branch order.png', dpi=300)
'''
'''
    
    
    
    
    
    