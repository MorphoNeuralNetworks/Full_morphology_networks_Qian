'''
Draw the location and heatmap of boutons in the whole brain
'''
import os,math
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

global step
step=25.0 # set the interval distance of the heat map

soma_info=np.load("..\Data\Other_Infomation\Soma_info.npy",allow_pickle=True).item()
soma_local={key:soma_info[key][1] for key in soma_info.keys()}
cell_type={key:soma_info[key][0] for key in soma_info.keys()}

# a dictionary of bouton coordinates for each neuron
bouton_list=dict()
path=r'..\Data\bouton'
count=0
for root,dirs,files in os.walk(path,topdown=True):
    for name in files:
        count+=1
        if count%50==0:
            print(count)
        with open(os.path.join(path,name)) as file_object:
            contents = file_object.readlines()
            file_object.close()
        data=[]
        for x in contents:
            t=list(map(float,x.split(' ')))
            data.append(t)
        bouton_list[name.split('.')[0]]=data
np.save('../Data/Temp_Data/bouton_list.npy',bouton_list)

## plot heatmap and .apo files
bouton_list=np.load('../Data/Temp_Data/bouton_list.npy', allow_pickle=True).item()
namelist=['VPM','CP','VPL','SSp-m','LGd','SSs','MOp','SSp-bfd','MG','MOs','RT','VISp','CLA','SSp-ul','SSp-n','RSPv','AId','all']

for name in namelist:
    ## .apo file with red bouton dots and blue soma dots, which can be seen in Vaa3d
    contents=['##n,orderinfo,name,comment,z,x,y, pixmax,intensity,sdev,volsize,mass,,,, color_r,color_g,color_b'+'\n']
    soma_con=['##n,orderinfo,name,comment,z,x,y, pixmax,intensity,sdev,volsize,mass,,,, color_r,color_g,color_b'+'\n']
    count=1
    count_s=1
    bouton_data=[]
    name_list=[]
    for key in bouton_list:
        if cell_type[key]==name or name=='all':
            name_list.append(key)
            temp=bouton_list[key]
            soma_id=soma_local[key]
            t=str(count_s)+',,,,'+str(soma_id[2]/25.0)+','+str(soma_id[0]/25.0)+','+str(soma_id[1]/25.0)+',0.000,0.000,0.000,70,0.000,,,,0,0,255'+'\n'
            soma_con.append(t)
            count_s+=1
            bouton_data.extend(temp)
            for x in temp:
                t=str(count)+',,,,'+str(x[2]/25.0)+','+str(x[0]/25.0)+','+str(x[1]/25.0)+',0.000,0.000,0.000,0.1,0.000,,,,255,0,0'+'\n'
                contents.append(t)
                count+=1
    f=open('./heatmap/'+name+'_bouton.apo',"w+",newline='')
    f.writelines(contents)
    f.close()
    f=open('./heatmap/'+name+'_soma.apo',"w+",newline='')
    f.writelines(soma_con)
    f.close()
    
    ## heatmap
    bouton_data=np.array(bouton_data)
    
    methods=['x-y','x-z','y-z'] # three perspectives
    for method in methods:
        plt.close('all')
        if method=='x-y':
            min_y=math.floor(min(bouton_data[:,1])/step)
            min_x=math.floor(min(bouton_data[:,0])/step)
            rows=math.ceil(max(bouton_data[:,1])/step)-min_y
            cols=math.ceil(max(bouton_data[:,0])/step)-min_x
            heatmap=np.zeros((rows+1,cols+1))
            for x in bouton_data:
                heatmap[math.ceil(x[1]/step)-min_y,math.ceil(x[0]/step)-min_x]+=1 
        elif method=='x-z':
            min_x=math.floor(min(bouton_data[:,0])/step)
            min_z=math.floor(min(bouton_data[:,2])/step)
            rows=math.ceil(max(bouton_data[:,0])/step)-min_x
            cols=math.ceil(max(bouton_data[:,2])/step)-min_z
            heatmap=np.zeros((rows+1,cols+1))
            for x in bouton_data:
                heatmap[math.ceil(x[0]/step)-min_x,math.ceil(x[2]/step)-min_z]+=1
        elif method=='y-z':
            min_y=math.floor(min(bouton_data[:,1])/step)
            min_z=math.floor(min(bouton_data[:,2])/step)
            rows=math.ceil(max(bouton_data[:,1])/step)-min_y
            cols=math.ceil(max(bouton_data[:,2])/step)-min_z
            heatmap=np.zeros((rows+1,cols+1))
            for x in bouton_data:
                heatmap[math.ceil(x[1]/step)-min_y,math.ceil(x[2]/step)-min_z]+=1
        plt.figure(figsize=(cols/50, rows/50))
        pic=sns.heatmap(data=heatmap,cbar=False,xticklabels=False,yticklabels=False,cmap=plt.get_cmap('OrRd'))
        plt.tight_layout()
        if method=='y-z':
            pic.invert_xaxis()
        plt.savefig('./heatmap/'+name+'_'+method+'.png',dpi=300)