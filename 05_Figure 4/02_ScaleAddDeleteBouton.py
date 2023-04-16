'''
Add or remove nodes for bouton density changes caused by scale operations
'''
import shutil
import os,math,csv
import numpy as np

def ScaleAddDelete(par):
    name,ratio,path,writepath=par[0],par[1],par[2],par[3]
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
        data.append(t1+[0])
    
    bouton_num=0
    # node distance
    data=np.array(data)
    for i in range(0,len(data)):
        if data[i,0]==0 or data[i,6]==-1:
            continue
        t1=data[i]
        t2=data[int(t1[6])-1]
        linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
        data[i,7]=linelen
        if data[i,1]==5:
            bouton_num+=1
    bouton_pair=[]
    dis_list=[]
    # count boutons
    for t in data:
        x=t
        if x[1]==5:
            temp=[int(t[0])-1]
            x_t=data[int(x[6])-1]
            axonlen=x[7]
            mark=0
            while x_t[6]!=-1 and x_t[1]!=5:
                mark=1
                x_t=data[int(x[6])-1]
                axonlen+=x[7]
                x=x_t
                temp.append(int(x_t[0])-1)
            if mark==0:
                temp.append(int(x_t[0])-1)
            if x_t[1]==5:
                bouton_pair.append(temp)
                dis_list.append(axonlen)
    bouton_pair=np.array(bouton_pair,dtype=list)
    dis_list=np.array(dis_list)
    bouton_pair=bouton_pair[np.argsort(dis_list)]
    
    if ratio < 0: # delete nodes
        delete_num=round(-ratio*bouton_num)
        step=(len(bouton_pair)-1)/delete_num
        for i in range(0,delete_num):
            t=int(round(i*step))
            delete_id=bouton_pair[t][0]
            data[delete_id,1]=2
    else: # add nodes
        add_num=round(ratio*bouton_num)
        add_list=[0]*len(bouton_pair)
        if add_num>=len(bouton_pair): # add a round directly first
            add_num=add_num-len(bouton_pair)
            add_list=[1]*len(bouton_pair)
        if add_num!=0:
            step=len(bouton_pair)/add_num
            for i in range(0,add_num):
                t=int(round(i*step))
                add_list[t]+=1
        # start adding points
        for i in range(0,len(add_list)):
            if add_list[i]==0: # no need to add points
                continue
            if add_list[i]>2:
                f=open(name+'_error.log','w+')
                f.write(str(i))
                f.close()
                continue
            if len(bouton_pair[i])==3: # add only one point whatever one point or two points
                add_id=bouton_pair[i][1]
                data[add_id,1]=5
            elif len(bouton_pair[i])==2: # add one point or two points
                # pass
                linenum=len(data)+1
                if add_list[i]==1:
                    t1=bouton_pair[i][0]
                    t2=bouton_pair[i][-1]
                    delta=[(data[t2,2]-data[t1,2])/2,(data[t2,3]-data[t1,3])/2,(data[t2,4]-data[t1,4])/2]
                    data[t1,6]=linenum
                    temp=np.array([[linenum,data[t1,1],data[t1,2]+delta[0],data[t1,3]+delta[1],data[t1,4]+delta[2],1,data[t2,0],0]])
                    data=np.r_[data,temp]
                elif add_list[i]==2:
                    t1=bouton_pair[i][0]
                    t2=bouton_pair[i][-1]
                    delta=[(data[t2,2]-data[t1,2])/3,(data[t2,3]-data[t1,3])/3,(data[t2,4]-data[t1,4])/3]
                    data[t1,6]=linenum
                    temp=np.array([[linenum,data[t1,1],data[t1,2]+delta[0],data[t1,3]+delta[1],data[t1,4]+delta[2],1,linenum+1,0],
                                  [linenum+1,data[t1,1],data[t1,2]+delta[0]*2,data[t1,3]+delta[1]*2,data[t1,4]+delta[2]*2,1,data[t2,0],0]])
                    data=np.r_[data,temp]
            elif len(bouton_pair[i])>3: # choose the middle two or one point to add
                if add_list[i]==1:
                    t=int(round((len(bouton_pair[i])-2)/2)+1)
                    add_id=bouton_pair[i][t]
                    data[add_id,1]=5
                elif add_list[i]==2:
                    if len(bouton_pair[i])==4:
                        t1,t2=1,2
                    else:
                        t1=int(round((len(bouton_pair[i])-2)/3+1))
                        t2=int(round((len(bouton_pair[i])-2)*2/3+1))
                    add_id=bouton_pair[i][t1]
                    data[add_id,1]=5
                    add_id=bouton_pair[i][t2]
                    data[add_id,1]=5
               
    new_content=['0 0 0 0 0 0 0\n']*len(data)
    for i in range(0,len(data)):
        t=data[i]
        temp=str(round(t[0]))+' '+str(round(t[1]))+' '+str(round(t[2],4))+' '+str(round(t[3],4))+' '+str(round(t[4],4))+' '+str(round(t[5]))+' '+str(round(t[6]))+'\n' #放大到原大小
        new_content[int(t[0])-1]=temp
    
    f=open(os.path.join(writepath, name),'w+')
    f.writelines(new_content)
    f.close()

def run__pool():  # main process
 
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    import time
    time_start = time.time()  # record start time
        
    ## 设置参数组合
    folderlist = os.listdir(r'.\Pertubation')
    par_list=[]
    for folder in folderlist:
        t=folder.split('_')
        if float(t[1])>0: #只有放大的才需要resample
            path=os.path.join(r'.\Pertubation',folder)
            write_path=os.path.join(r'.\Pertubation',folder)
            if not os.path.exists(write_path):
                os.mkdir(write_path)
            for root, dirs, files in os.walk(path):
                for file in files:
                    par_list.append((file,float(t[1])-1,path,write_path))
    
    with Pool(cpu_worker_num) as p:
        p.map(ScaleAddDelete, par_list)
       
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('ScaleAddDelete Bouton time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()

   

    
    
    

    