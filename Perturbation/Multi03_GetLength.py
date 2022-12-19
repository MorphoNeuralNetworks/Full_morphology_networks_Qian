## 对进行过Pertubation的文件生成对应的bouton文件
import math
import shutil
import os,csv

global grid
grid=30

def GetLength(filepath):
    writepath=filepath.replace('Pertubation','Pertubation_Length')
    writepath=writepath.replace('.swc','.csv')
    empty=[]
    with open(filepath) as file_object:
        contents = file_object.readlines()
        # print(len(contents))
        file_object.close()
    while contents[0][0]=='#':# 删除注释
        del contents[0]
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        if t1[0]==0:
            continue
        if t1[0]==t1[-1]: #修正版本的数据会出现自己导向自己的情况，得处理这个问题
            print('Circle Warning!!!')
            continue
        if t1[1]!=5:
            # 计算到上一节点的长度
            t2=contents[int(t1[-1])-1].split( )
            t2=list(map(float,t2))
            linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
            t1[2],t1[3],t1[4]=t1[2]/grid,t1[3]/grid,t1[4]/grid #标度修正
            #对坐标进行取scale'
            t1[2:5]=list(map(math.floor,t1[2:5]))
            x=str(t1[2])+'_'+str(t1[3])+'_'+str(t1[4])
            empty.append(str(t1[1])+' '+x+' '+str(linelen))

    # 转换为csv
    data=[]
    for i in range(0,len(empty)):
        temp=empty[i].split()
        data.append(temp)
    with open(writepath,"w+",newline='') as f:
        csv_writer = csv.writer(f)
        for rows in data:
            csv_writer.writerow(rows)
        f.close()
    
def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 36
    
    folderlist = os.listdir(r'.\Pertubation')
    for folder in folderlist:
        writepath=os.path.join(r'.\Pertubation_Length',folder)
        if os.path.exists(writepath):
            shutil.rmtree(writepath)  
        os.mkdir(writepath) 
    filelist=[]
    for folder in folderlist:
        path=os.path.join(r'.\Pertubation',folder)
        for root, dirs, files in os.walk(path):
            for file in files:
                filelist.append(os.path.join(path,file))
            
    import time
    time_start = time.time()  # 记录开始时间
    with Pool(cpu_worker_num) as p:
        p.map(GetLength, filelist)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('GetLenght time: '+str(time_sum))  

if __name__ =='__main__':
    if not os.path.exists('./Pertubation_Length'):
        os.mkdir('./Pertubation_Length')
    run__pool()