## 对进行过Pertubation的文件生成对应的bouton文件
import shutil
import os

def GetBouton(filepath):
    writepath=filepath.replace('Pertubation','Pertubation_Bouton')
    
    with open(filepath) as file_object:
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
            temp=str(t2[2])+' '+str(t2[3])+' '+str(t2[4])+'\n' #放大到原大小
            new_content.append(temp)
    f=open(writepath,'w+')
    f.writelines(new_content)
    f.close()
    
def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 36
    
    folderlist = os.listdir(r'.\Pertubation')
    for folder in folderlist:
        writepath=os.path.join(r'.\Pertubation_Bouton',folder)
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
        p.map(GetBouton, filelist)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('GetBouton time: '+str(time_sum))  

if __name__ =='__main__':
    if not os.path.exists('./Pertubation_Bouton'):
        os.mkdir('./Pertubation_Bouton')
    run__pool()