import numpy as np
import os,csv,math,shutil
## 检查某个特定网路中bouton连接的比例
def GetBoutonRatio(par):
    pixel_path,connect_path,name=par[0],par[1],par[2]
    pixel_bouton_dir=np.load(pixel_path, allow_pickle=True).item()
    connection_map=np.load(connect_path, allow_pickle=True)
    neruon_bouton_pixel={x:[] for x in list(set(connection_map[:,0]))}
    for x in connection_map:
        neruon_bouton_pixel[x[0]].extend(x[2])
    for key in neruon_bouton_pixel.keys():
        neruon_bouton_pixel[key]=list(set(neruon_bouton_pixel[key]))
    total_list=[len(pixel_bouton_dir[key]) for key in pixel_bouton_dir.keys()]
    total_length=np.sum(total_list)
    count=[]
    for key in neruon_bouton_pixel.keys():
        cc=[x for x in neruon_bouton_pixel[key] if x in pixel_bouton_dir[key]]
        count.append(len(cc))
    count_bouton=np.sum(count)
    np.save('./temp/'+name+'.npy',[count_bouton,total_length,count_bouton/total_length])
    
def run__pool():  # main process
      methods=["bouton","boutondensity_each"]
      for method in methods[0:1]:
          if os.path.exists('temp'):
              shutil.rmtree('temp')
          os.mkdir('temp')
          
          # par_list=[]
          # if method=="bouton":
          #     start_list='D:/QPH/BrainNetwork_Pertubation/'
          # elif method=="boutondensity_each":
          #     start_list='D:/QPH/BrainNetwork_Pertubation_density_each/'
          # folderpath = os.listdir(start_list+'Pertubation')
          
          # if method=="bouton":
          #     par_list.append(['D:/QPH/BrainNetwork/Temp_Data/bouton_Bouton.npy','D:/QPH/BrainNetwork/bouton_connection.npy','bouton'])
          # elif method=="boutondensity_each":
          #     par_list.append(['D:/QPH/BrainNetwork/Temp_Data/boutondensity_each_Bouton.npy','D:/QPH/BrainNetwork/boutondensity_each_connection.npy','boutondensity'])
          # for x in folderpath:
          #     t1=start_list+'Pertubation_Temp/'+x+'_Bouton.npy'
          #     if method=="bouton":
          #         t2=start_list+'Pertubation_Result/'+x+'_Bouton.npy'
          #     elif method=="boutondensity_each":
          #         t2=start_list+'Pertubation_Result/'+x+'_Boutondensity_each.npy'
          #     par_list.append([t1,t2,x])
          
          par_list=[['D:/QPH/BrainNetwork/Temp_Data/bouton_Bouton.npy','D:/QPH/BrainNetwork/bouton_connection.npy','normal'],
                    ['D:/QPH/BrainNetwork/Temp_Data/boutondensity_each_Bouton.npy','D:/QPH/BrainNetwork/boutondensity_each_connection.npy','normal_density'],
                    ['D:/QPH/BrainNetwork_Half/BrainNetwork_1/Temp_Data/bouton_Bouton.npy','D:/QPH/BrainNetwork_Half/BrainNetwork_1/bouton_connection.npy','half_1'],
                    ['D:/QPH/BrainNetwork_Half/BrainNetwork_2/Temp_Data/bouton_Bouton.npy','D:/QPH/BrainNetwork_Half/BrainNetwork_2/bouton_connection.npy','half_2'],
                    ['D:/QPH/BrainNetwork_Half/BrainNetwork_3/Temp_Data/bouton_Bouton.npy','D:/QPH/BrainNetwork_Half/BrainNetwork_3/bouton_connection.npy','half_3'],
                    ['D:/QPH/BrainNetwork_Half/BrainNetwork_4/Temp_Data/bouton_Bouton.npy','D:/QPH/BrainNetwork_Half/BrainNetwork_4/bouton_connection.npy','half_4'],
                    ['D:/QPH/BrainNetwork_Half/BrainNetwork_5/Temp_Data/bouton_Bouton.npy','D:/QPH/BrainNetwork_Half/BrainNetwork_5/bouton_connection.npy','half_5'],
                    ['D:/QPH/BrainNetwork_Pertubation/Pertubation_Temp/scale_0_prune_0_delete_0.5_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation/Pertubation_Result/scale_0_prune_0_delete_0.5_all_Bouton.npy','delete_1'],
                    ['D:/QPH/BrainNetwork_Pertubation_1/Pertubation_Temp/scale_0_prune_0_delete_0.5_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_1/Pertubation_Result/scale_0_prune_0_delete_0.5_all_Bouton.npy','delete_2'],
                    ['D:/QPH/BrainNetwork_Pertubation_2/Pertubation_Temp/scale_0_prune_0_delete_0.5_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_2/Pertubation_Result/scale_0_prune_0_delete_0.5_all_Bouton.npy','delete_3'],
                    ['D:/QPH/BrainNetwork_Pertubation_3/Pertubation_Temp/scale_0_prune_0_delete_0.5_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_3/Pertubation_Result/scale_0_prune_0_delete_0.5_all_Bouton.npy','delete_4'],
                    ['D:/QPH/BrainNetwork_Pertubation_4/Pertubation_Temp/scale_0_prune_0_delete_0.5_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_4/Pertubation_Result/scale_0_prune_0_delete_0.5_all_Bouton.npy','delete_5'],
                    ['D:/QPH/BrainNetwork_Pertubation/Pertubation_Temp/scale_0.5_prune_0_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation/Pertubation_Result/scale_0.5_prune_0_delete_0_all_Bouton.npy','scale_1'],
                    ['D:/QPH/BrainNetwork_Pertubation_1/Pertubation_Temp/scale_0.5_prune_0_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_1/Pertubation_Result/scale_0.5_prune_0_delete_0_all_Bouton.npy','scale_2'],
                    ['D:/QPH/BrainNetwork_Pertubation_2/Pertubation_Temp/scale_0.5_prune_0_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_2/Pertubation_Result/scale_0.5_prune_0_delete_0_all_Bouton.npy','scale_3'],
                    ['D:/QPH/BrainNetwork_Pertubation_3/Pertubation_Temp/scale_0.5_prune_0_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_3/Pertubation_Result/scale_0.5_prune_0_delete_0_all_Bouton.npy','scale_4'],
                    ['D:/QPH/BrainNetwork_Pertubation_4/Pertubation_Temp/scale_0.5_prune_0_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_4/Pertubation_Result/scale_0.5_prune_0_delete_0_all_Bouton.npy','scale_5'],
                    ['D:/QPH/BrainNetwork_Pertubation/Pertubation_Temp/scale_0_prune_0.5_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation/Pertubation_Result/scale_0_prune_0.5_delete_0_all_Bouton.npy','prune_1'],
                    ['D:/QPH/BrainNetwork_Pertubation_1/Pertubation_Temp/scale_0_prune_0.5_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_1/Pertubation_Result/scale_0_prune_0.5_delete_0_all_Bouton.npy','prune_2'],
                    ['D:/QPH/BrainNetwork_Pertubation_2/Pertubation_Temp/scale_0_prune_0.5_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_2/Pertubation_Result/scale_0_prune_0.5_delete_0_all_Bouton.npy','prune_3'],
                    ['D:/QPH/BrainNetwork_Pertubation_3/Pertubation_Temp/scale_0_prune_0.5_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_3/Pertubation_Result/scale_0_prune_0.5_delete_0_all_Bouton.npy','prune_4'],
                    ['D:/QPH/BrainNetwork_Pertubation_4/Pertubation_Temp/scale_0_prune_0.5_delete_0_all_Bouton.npy','D:/QPH/BrainNetwork_Pertubation_4/Pertubation_Result/scale_0_prune_0.5_delete_0_all_Bouton.npy','prune_5'],
                    ]
          
          from multiprocessing import Pool
          cpu_worker_num = 36
      
          import time
          time_start = time.time()  # 记录开始时间
          with Pool(cpu_worker_num) as p:
              p.map(GetBoutonRatio, par_list)
              
          time_end = time.time()  # 记录结束时间
          time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
          print('Get Bouton Ratio time: '+str(time_sum))
          BoutonCount=dict()
          files = os.listdir('./temp')
          for i in files:
              tt=np.load('./temp/'+i,allow_pickle=True)
              ii=i.split('.npy')[0]
              BoutonCount[ii]=tt.tolist()
          np.save('BoutonRatio_'+method,BoutonCount)
    

if __name__ =='__main__':
    run__pool()

    
