import os,csv
import shutil
global brain_info
## 根据给定的脑分辨率大小，还原未配准前的swc文件
with open('./Other_Infomation/all_brain_metainfo.csv') as f:
    brain_info=list(csv.reader(f))
    f.close()
del brain_info[0]

# 构建brain分辨率
global brain_re
brain_re=dict()
for x in brain_info:
    brain_re[x[0]]=[float(x[2]),float(x[3]),float(x[4])]

# 根据raw文件提取出未注册到CCFv3的文件
def RawInfoNoregist(par):
    path,file,write_path=par[0],par[1],par[2]
    brain_name=file.split('_')[0]
    if brain_name=='15257':
        brain_name='210254'
    if brain_name not in brain_re.keys():
        print(brain_name)
    resolution=brain_re[brain_name]
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        file_object.close()
    x=contents[-1]
    x=x.strip("\n")
    t1=x.split( )
    t2=list(map(float,t1))
    new_content=['0 0 0 0 0 0 0\n']*int(t2[0])
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# 跳过注释
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        temp=str(round(t2[0]))+' '+str(round(t2[1]))+' '+str(round(t2[2]*resolution[0],4))+' '+str(round(t2[3]*resolution[1],4))+' '+str(round(t2[4]*resolution[2],4))+' '+str(round(t2[5]))+' '+str(round(t2[6]))+'\n' #放大到原大小
        new_content[int(t2[0])-1]=temp
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
        
# 根据raw文件提取出注册到CCFv3的文件 
# 存在缺失的情况，已经用0补全了
def RawInfoRegist(par):
    path,file,write_path=par[0],par[1],par[2]
    with open(os.path.join(path, file)) as file_object:
        contents = file_object.readlines()
        #print(len(contents))
        file_object.close()
    x=contents[-1]
    x=x.strip("\n")
    t1=x.split( )
    t2=list(map(float,t1))
    new_content=['0 0 0 0 0 0 0\n']*int(t2[0])
    for lineid in range(0,len(contents)):
        if contents[lineid][0]=='#':# 跳过注释
            continue  
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t2=list(map(float,t1))
        temp=str(round(t2[0]))+' '+str(round(t2[1]))+' '+str(round(t2[12]*25,2))+' '+str(round(t2[13]*25,2))+' '+str(round(t2[14]*25,2))+' '+str(round(t2[5]))+' '+str(round(t2[6]))+'\n' #放大到原大小
        new_content[int(t2[0])-1]=temp
    new_file=file.split('.')[0]+'.swc'
    f=open(os.path.join(write_path, new_file),'w+')
    f.writelines(new_content)
    f.close()
        
        
def run__pool():  # main process
    from multiprocessing import Pool
    cpu_worker_num = 36
    import time
    time_start = time.time()  # 记录开始时间
    
    # 根据raw文件提取出未注册到CCFv3的文件
    path=r'./bouton_raw'
    write_path=r'./Noregisted/bouton_swc_noadd'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    par_list=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])
    with Pool(cpu_worker_num) as p:
        p.map(RawInfoNoregist, par_list)
    
    # 根据raw文件提取出注册到CCFv3的文件 
    path=r'./bouton_raw'
    write_path=r'./bouton_swc_noadd'
    # 清空文件夹
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    else:
        shutil.rmtree(write_path)  
        os.mkdir(write_path)
    par_list=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            par_list.append([path,file,write_path])
    with Pool(cpu_worker_num) as p:
        p.map(RawInfoRegist, par_list)
    
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Bouton No Registed time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
   