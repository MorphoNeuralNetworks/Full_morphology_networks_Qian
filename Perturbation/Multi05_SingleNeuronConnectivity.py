## 使用多线程对每种参数组合进行网络连接的生成
import math
import os,csv
import numpy as np

global grid
grid=30 #由于映射误差大约为30um 由于grid过大，填充点似乎没有意义了

# DDA算法进行数据点填充
def DDALine(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    steps = 0
    # 斜率判断
    if abs(dx) == max([abs(dx),abs(dy),abs(dz)]):
        steps = abs(dx)
    elif abs(dy) == max([abs(dx),abs(dy),abs(dz)]):
        steps = abs(dy)
    elif abs(dz) == max([abs(dx),abs(dy),abs(dz)]):
        steps = abs(dz)
    # 必有一个等于1，一个小于1
    delta_x = float(dx / steps)
    delta_y = float(dy / steps)
    delta_z = float(dz / steps)
    # 四舍五入，保证x和y的增量小于等于1，让生成的直线尽量均匀
    x,y,z=x1,y1,z1
    temp=[str(x)+'_'+str(y)+'_'+str(z)]
    for i in range(0, int(steps-1)):
		# 绘制像素点
        x += delta_x
        y += delta_y
        z += delta_z
        s_t=str(math.floor(x))+'_'+str(math.floor(y))+'_'+str(math.floor(z))
        temp.append(s_t)
    return temp


# 读取raw文件，并构建对应axon dendrite的覆盖点列表
def PixelCount(pixel_axon_dir,pixel_dendrite_dir,path,name):
    with open(path) as file_object:
        contents = file_object.readlines()
        #print(len(contents))
        file_object.close()
    while contents[0][0]=='#':# 删除注释
        del contents[0]
    for lineid in range(0,len(contents)):
        x=contents[lineid]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        t1[2],t1[3],t1[4]=t1[2]/grid,t1[3]/grid,t1[4]/grid #标度修正
        if t1[0]==0: #无效数据
            continue
        if t1[0]==t1[-1]: #修正版本的数据会出现自己导向自己的情况，得处理这个问题
            print('Circle Warning!!! ')
            continue
        #对坐标进行取scale
        t1[2:5]=list(map(math.floor,t1[2:5]))
        # 非soma区域
        if int(t1[-1])!=-1:
            t2=contents[int(t1[-1])-1].split( )
            t2=list(map(float,t2))
            t2[2],t2[3],t2[4]=t2[2]/grid,t2[3]/grid,t2[4]/grid #标度修正
            #对坐标进行取scale
            t2[2:5]=list(map(math.floor,t2[2:5]))
            linelen=math.sqrt((t1[2]-t2[2])*(t1[2]-t2[2])+(t1[3]-t2[3])*(t1[3]-t2[3])+(t1[4]-t2[4])*(t1[4]-t2[4]))
            if t1[1]==2: #需要取axon的覆盖区域
                #如果距离大于1，则需要补充点
                if linelen<-1:
                    temp=DDALine(t1[2],t1[3],t1[4],t2[2],t2[3],t2[4])
                    for x in temp:
                        pixel_axon_dir[name].append(x)
                else:
                    #如果距离小于1，则把该点纳入list
                    x=str(t1[2])+'_'+str(t1[3])+'_'+str(t1[4])
                    pixel_axon_dir[name].append(x)
            elif t1[1]==3 or t1[1]==4: #dendrite覆盖区域 
               #如果距离大于1，则需要补充点
               if linelen<-1:
                   temp=DDALine(t1[2],t1[3],t1[4],t2[2],t2[3],t2[4])
                   for x in temp:
                       pixel_dendrite_dir[name].append(x)
               else:
                   #如果距离小于1，则把该点纳入list
                   x=str(t1[2])+'_'+str(t1[3])+'_'+str(t1[4])
                   pixel_dendrite_dir[name].append(x)
    return pixel_axon_dir,pixel_dendrite_dir

def BoutonCount(path,pixel_bouton_dir):
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(path, file)) as file_object:
                contents = file_object.readlines()
                #print(len(contents))
                file_object.close()
                name=file.split('.')[0]
                pixel_bouton_dir[name]=[]
            for lineid in range(0,len(contents)):
                if contents[lineid][0]=='#':# 跳过注释
                    continue  
                x=contents[lineid]
                x=x.strip("\n")
                t1=x.split( )
                t2=list(map(float,t1))
                t2[0],t2[1],t2[2]=t2[0]/grid,t2[1]/grid,t2[2]/grid 
                t2=list(map(math.floor,t2)) #标度修正
                x=str(t2[0])+'_'+str(t2[1])+'_'+str(t2[2])
                pixel_bouton_dir[name].append(x)
    return pixel_bouton_dir

# 需要实现的功能
def GenerateNpy(folderpath):
    path='.\\Pertubation\\'+folderpath
    # 构建数据索引
    pixel_axon_dir=dict()
    pixel_dendrite_dir=dict()
    pixel_bouton_dir=dict()
    
    # 统计pixel覆盖范围
    for root, dirs, files in os.walk(path):
        for f in files:
            name=f.split('.')[0]
            pixel_axon_dir[name]=[]
            pixel_dendrite_dir[name]=[]
            pixel_axon_dir,pixel_dendrite_dir=PixelCount(pixel_axon_dir,pixel_dendrite_dir,os.path.join(root,f),name)
            
    np.save('.\\Pertubation_Temp\\'+folderpath+'_Axon.npy', pixel_axon_dir)
    np.save('.\\Pertubation_Temp\\'+folderpath+'_Dendrite.npy', pixel_dendrite_dir)
    
    # 构建每个文件的bouton数据的dict
    pixel_bouton_dir=BoutonCount('.\\Pertubation_Bouton\\'+folderpath,pixel_bouton_dir)
    np.save('.\\Pertubation_Temp\\'+folderpath+'_Bouton.npy', pixel_bouton_dir)

    # 判断一个cube内dendrite或者axon的数据量是否超过了限定范围 
    with open('.\\Pertubation_Temp\\'+folderpath+"_Dataset_Cube.csv") as f:
        reader = csv.reader(f)
        cube_data=np.array(list(reader)) #直接比较最大值就可以了
        f.close
    global cube_map
    cube_map=dict()
    for x in cube_data:
        if float(x[2])!=0:
            cube_map[str(x[0])]=[float(x[1]),float(x[2])]

    # 构建soma在每个cube内dendrite的字典
    with open('.\\Pertubation_Temp\\'+folderpath+"_Dataset_Soma.csv") as f:
        reader = csv.reader(f)
        cube_data=np.array(list(reader)) #直接比较最大值就可以了
        f.close
    global cube_dict
    cube_dict=dict()
    for x in cube_data:
        cube_dict[str(x[0])+'_'+x[1]]=[float(x[2]),float(x[3])]
    np.save('.\\Pertubation_Temp\\'+folderpath+"_Cube_Map.npy",cube_map)
    np.save('.\\Pertubation_Temp\\'+folderpath+"_Cube_Dict.npy",cube_dict)

def run__pool():  # main process

    from multiprocessing import Pool
    cpu_worker_num = 36
    
    folderpath = os.listdir(r'.\Pertubation')
    
    import time
    time_start = time.time()  # 记录开始时间
    with Pool(cpu_worker_num) as p:
        p.map(GenerateNpy, folderpath)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('Connectivity Npy file time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
     
    
    