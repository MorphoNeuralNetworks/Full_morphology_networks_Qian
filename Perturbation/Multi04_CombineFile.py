## 对进行过Pertubation的文件生成对应的bouton文件
import math
import shutil
import os,csv
import numpy as np

def CombineFile(foldername):
    folderpath = os.path.join(r'.\Pertubation_Length',foldername)
    empty=[]
    for root,dirs,files in os.walk(folderpath,topdown=True):
        for name in files:
            with open(os.path.join(root,name)) as file_object:
                soma=name.split('.')[0]
                contents = file_object.readlines()
                file_object.close()
                
            cube_set=[]
            for lines in contents:
                x=lines.split(',')
                cube_set.append(x[1])
            cube_set=list(set(cube_set))
            #构建长度统计
            count_list=[];
            for i in range(0,len(cube_set)):
                count_list.append([0,0])
            for x in contents:
                t1=x.split(',')
                t=cube_set.index(t1[1])
                if float(t1[0])==2:
                    count_list[t][0]=count_list[t][0]+float(t1[2]);
                elif float(t1[0])==3 or float(t1[0])==4:
                    count_list[t][1]=count_list[t][1]+float(t1[2]);
            for i in range(0,len(cube_set)):
                empty.append([soma,cube_set[i],count_list[i][0],count_list[i][1]])

    with open(".\\Pertubation_Temp\\"+foldername+"_Dataset_Soma.csv","w+",newline='') as f:
        csv_writer = csv.writer(f)
        for rows in empty:
            csv_writer.writerow(rows)
        f.close()

    # 得到每个cube内axon和dendrite数量
    data=np.array(empty)
    data = data[np.argsort(data[:,1])]
    lineid=0
    re_list=[]
    local_id=data[0,1]
    count_axon=0
    count_dend=0
    while lineid<len(data):
        if local_id!=data[lineid,1]:
            re_list.append([str(local_id),count_axon,count_dend])
            local_id=data[lineid,1]
            count_axon=0
            count_dend=0
        else:
            count_axon+=data[lineid,2].astype(np.float64)
            count_dend+=data[lineid,3].astype(np.float64)
            lineid+=1
    re_list.append([str(local_id),count_axon,count_dend])

    with open(".\\Pertubation_Temp\\"+foldername+"_Dataset_Cube.csv","w+",newline='') as f:
        csv_writer = csv.writer(f)
        for rows in re_list:
            csv_writer.writerow(rows)
        f.close()
    
def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 36
    
    folderlist = os.listdir(r'.\Pertubation')
            
    import time
    time_start = time.time()  # 记录开始时间
    with Pool(cpu_worker_num) as p:
        p.map(CombineFile, folderlist)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Combine File time: '+str(time_sum))  

if __name__ =='__main__':
    if not os.path.exists('./Pertubation_Temp'):
        os.mkdir('./Pertubation_Temp')
    run__pool()