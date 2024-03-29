'''
three kinds of perturbation
1. scale dendritic trees or axonal clusters
2. prune branches by removing segments from terminal points to branch points with some probability
3. remove a percentage of axon boutons
'''

import os,random,math
import numpy as np
import matplotlib.pyplot as plt
import shutil  

global path
path=r'..\Data\bouton_swc'

## distance between nodes
def NodeDistance(contents):
    distance_list=[0]*len(contents)
    for x in contents:
        if x[-1]==-1 or x[0]==0:
            distance_list[int(x[0])-1]=-1
            continue
        t=contents[int(x[-1])-1]
        distance_list[int(x[0])-1]=math.sqrt((x[2]-t[2])*(x[2]-t[2])+\
                                             (x[3]-t[3])*(x[3]-t[3])+\
                                                 (x[4]-t[4])*(x[4]-t[4]))
    return distance_list

## list of leaf nodes
def Nodeleaf(contents,distance_list,branch_num):    
    leaf_list=np.zeros((branch_num.count(0),3))
    count=0
    for i in range(0,len(contents)):
        if branch_num[i]==0:
            leaf_list[count,0]=i
            if contents[i,1]==2 or contents[i,1]==5:
                leaf_list[count,1]=2
            elif contents[i,1]==3 or contents[i,1]==4:
                leaf_list[count,1]=3
            t=i
            length=0
            while contents[t,-1]!=-1:
                length+=distance_list[t]
                t=int(contents[t,-1])-1
            leaf_list[count,2]=length
            count+=1
    return leaf_list

## scale function
def ScaleFunction(ratio,contents,target_local,proj_list):
    for i in proj_list:
        contents[i,2]=(contents[i,2]-target_local[0])*ratio+target_local[0]
        contents[i,3]=(contents[i,3]-target_local[1])*ratio+target_local[1]
        contents[i,4]=(contents[i,4]-target_local[2])*ratio+target_local[2]
    return contents

## Scaling of swc files 
# for dendrite directly connected to soma
# for other branches that are not main axon
# for boutons on axon
# support for separate/whole dendrite,axon
def ScaleNeuron(ratio,contents,method='all'): # axon dendrite all
    # soma, no data, and main axon set to -1
    branch_num=[0]*len(contents)
    for i in range(0,len(contents)):
        x=contents[i]
        if x[-1]==-1:
            continue
        elif x[0]==0:
            branch_num[i]=-1
        else:
            branch_num[int(x[-1])-1]+=1
    distance_list=NodeDistance(contents)
    leaf_list=Nodeleaf(contents,distance_list,branch_num)
    
    if method=='dendrite' or method=='all':
        ## all dendrite nodes connected to soma
        dendrite_list=[]
        tt=np.where(leaf_list[:,1]==3)[0]
        for t in tt:
            index=int(leaf_list[t,0])
            while index not in dendrite_list:
                dendrite_list.append(index)
                index=int(contents[index,-1])-1
                if contents[index,-1]==-1:
                    break
        soma_local=[]
        for x in contents:
            if x[-1]==-1:
                soma_local=x[2:5]
                break
        contents=ScaleFunction(ratio,contents,soma_local,dendrite_list)
    
    if method=='axon' or method=='all':
        # axons that are not main axon
        tt=np.where(leaf_list[:,1]==2)
        leaf_temp=leaf_list[tt]   
        tt=np.where(leaf_temp[:,2]==np.max(leaf_temp[:,2]))[0]
        # mark main axon as -1
        index=int(leaf_temp[tt,0])
        while contents[index,-1]!=-1:
            branch_num[index]=-1
            index=int(contents[index,-1])-1
        
        proj_list={}
        for x in leaf_temp:
            index=int(x[0])    
            temp_list=[]
            while contents[index,-1]!=-1 and branch_num[index]!=-1:
                # print(index)
                temp_list.append(index)
                index=int(contents[index,-1])-1
            if len(temp_list)==0:
                continue
            if index in proj_list.keys():
                temp_list.extend(proj_list[index])
                proj_list[index]=temp_list
            else:
                proj_list[index]=temp_list
        # scaling with root node
        for key in proj_list.keys():
            temp_list=list(set(proj_list[key]))
            target_local=contents[key,2:5]
            contents=ScaleFunction(ratio,contents,target_local,temp_list)
            
    return contents

## list of leaf nodes without distance
def NodeleafNoDistance(contents,branch_num):    
    leaf_list=np.zeros((branch_num.count(0),2))
    count=0
    for i in range(0,len(contents)):
        if branch_num[i]==0:
            leaf_list[count,0]=i
            if contents[i,1]==2 or contents[i,1]==5:
                leaf_list[count,1]=2
            elif contents[i,1]==3 or contents[i,1]==4:
                leaf_list[count,1]=3
            count+=1
    return leaf_list

## prune branches
# delete once and then do the next round of deletion
# support for separate/whole dendrite,axon
def DeleteBranch(delete_ratio,contents,method='all'): # axon dendrite all
    ratio=1-delete_ratio # percentage of retained
    # soma and no data set to -1
    branch_num=[0]*len(contents)
    for i in range(0,len(contents)):
        x=contents[i]
        if x[-1]==-1:
            continue
        elif x[0]==0:
            branch_num[i]=-1
        else:
            branch_num[int(x[-1])-1]+=1
    leaf_list=NodeleafNoDistance(contents,branch_num)
    
    step=-1
    while step>0 or step==-1:        
        # finding random non-zero nodes
        index=0
        if method=='all':
            t=random.randint(0, len(leaf_list)-1)
            index=int(leaf_list[t,0])
            
            if len(leaf_list)==0:
                print('no leaf node')
                break
            if step==-1:
                step=int(math.ceil(len(leaf_list)*ratio))-1
            else:
                step=step-1
            leaf_list=np.delete(leaf_list,t,0)
        
        elif method=='axon':
            tt=np.where(leaf_list[:,1]==2)[0]
            t=random.randint(0, len(tt)-1)
            index=int(leaf_list[tt[t],0])
            if len(tt)==0:
                print('no axon node')
                break
            if step==-1:
                step=int(math.ceil(len(tt)*ratio))-1
            else:
                step=step-1
            leaf_list=np.delete(leaf_list,tt[t],0)
        
        elif method=='dendrite':
            tt=np.where(leaf_list[:,1]==3)[0]
            t=random.randint(0, len(tt)-1)
            index=int(leaf_list[tt[t],0])
            if len(tt)==0:
                print('no dendrite node')
                break
            if step==-1:
                step=int(math.ceil(len(tt)*ratio))-1
            else:
                step=step-1
            leaf_list=np.delete(leaf_list,tt[t],0)
            
        # delete upwards from this node
        while branch_num[index]<2 and branch_num[index]!=-1:
            # print(index)
            index_t=int(contents[index,-1])-1
            contents[index]=[0,0,0,0,0,0,0]
            branch_num[index]=-1
            index=index_t
        branch_num[index]-=1
    return contents

## delete any ratio of bouton
def DeleteBouton(delete_ratio,contents):
    ratio=1-delete_ratio
    # find all bouton
    bouton_list=np.where(contents[:,1]==5)[0]
    if len(bouton_list)==0:
        print('No Bouton in file')
        return
    delete_list=random.sample(bouton_list.tolist(), round(len(bouton_list)*ratio))
    for node in delete_list:
        contents[node,1]=2
    return contents

## visualization
def DrawStructure(contents,num):
    # plt.close()
    plt.figure(num)
    ax = plt.axes(projection="3d") 
    color_dict={1:'k',2:'r',3:'y',4:'b',5:'g'}
    for x in contents:
        if x[-1]==-1 or x[0]==0:
            continue
        t=contents[int(x[-1])-1]
        ax.plot([x[2],t[2]], [x[3],t[3]], [x[4],t[4]],c=color_dict[x[1]],linewidth=2)

## analyze the parameters and process
def Changefile(compute_list):
    filename,scale_ratio,prune_raio,delete_ratio,method=compute_list[0],compute_list[1],compute_list[2],compute_list[3],compute_list[4]
    
    writepath='.\\Pertubation\\'+'scale_'+str(scale_ratio)+'_prune_'+str(prune_raio)+'_delete_'+str(delete_ratio)+'_'+method
    with open(os.path.join(path, filename)) as file_object:
        temp = file_object.readlines()
        file_object.close()
    contents=[]
            
    for x in temp:
        t=x.split(' ')
        t=list(map(float,t))
        contents.append(t)
    contents=np.array(contents)
    if scale_ratio!=0:
        contents=ScaleNeuron(scale_ratio,contents,method)
    if prune_raio!=0:
        contents=DeleteBranch(prune_raio,contents,method)
    if delete_ratio!=0:
        contents=DeleteBouton(delete_ratio,contents)
    new_contents=[]
    for x in contents:
        temp=str(int(x[0]))+' '+str(int(x[1]))+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(int(x[5]))+' '+str(int(x[6]))+'\n'
        new_contents.append(temp)
    with open(os.path.join(writepath,filename),"w+",newline='') as f:
        f.writelines(new_contents)
        f.close()
    
def run__pool():  # main process
    # parameter combinations
    para_list=[]
    method=['axon','dendrite','all']
    for x in method:
        for scale_ratio in range(5,10):
            para_list.append([scale_ratio/10.0,0,0,x])
        # for scale_ratio in range(12,22,2):
        #     para_list.append([scale_ratio/10.0,0,0,x])
        for prune_ratio in range(5,10):
            para_list.append([0,prune_ratio/10.0,0,x])
    for delete_ratio in range(5,10):
        para_list.append([0,0,delete_ratio/10.0,'all'])
    print(para_list)
    for x in para_list:
        writepath='./Pertubation/'+'scale_'+str(x[0])+'_prune_'+str(x[1])+'_delete_'+str(x[2])+'_'+x[3]
        if os.path.exists(writepath):
            shutil.rmtree(writepath)  
        os.mkdir(writepath) 
    print("parameters: "+str(len(para_list)))
    
    compute_list=[]
    for root,dirs,files in os.walk(path,topdown=True):
        for file in files:
            for x in para_list:
                compute_list.append([file,x[0],x[1],x[2],x[3]])  
    print("files: "+str(len(compute_list)))
    from multiprocessing import Pool
    cpu_worker_num = 36 # set the number of CPUs in parallel
    
    import time
    time_start = time.time()  # record start time
    with Pool(cpu_worker_num) as p:
        p.map(Changefile, compute_list)
    time_end = time.time()  # record end time
    time_sum = time_end - time_start  # time of program execution in seconds(s)
    print('Perturbation time: '+str(time_sum))  

if __name__ =='__main__':
    if not os.path.exists('./Pertubation'):
        os.mkdir('./Pertubation')
    run__pool()

    # path=r'./test'
    # for root, dirs, files in os.walk(path):
    #     for file in files[2:3]:
    #         with open(os.path.join(path, file)) as file_object:
    #             temp = file_object.readlines()
    #             #print(len(contents))
    #             file_object.close()
    #         contents=[]
            
    #         for x in temp:
    #             t=x.split(' ')
    #             t=list(map(float,t))
    #             contents.append(t)
    #         contents=np.array(contents)
    #         DrawStructure(contents,1)
    #         # contents=ScaleNeuron(3,contents,'axon')
    #         contents=DeleteBranch(ratio=0.6,contents=contents,method='all')            
    #         DrawStructure(contents,2)
        


        