import numpy as np
import csv,os
import matplotlib.pyplot as plt 
# 获取神经元所在脑区的信息
with open(r'..\Data\Other_Infomation\Allen_CellType_Detail.csv', 'r', newline='') as csvfile:
    t = csv.reader(csvfile)
    area_data=np.array(list(t))
    csvfile.close()
cell_type=dict()
for root, dirs, files in os.walk(r'..\Data\Noregisted\bouton_swc'):
    for file in files:
        t=file.split('.')[0]
        if '15257_' in t:
            t=t.replace('15257_', '210254_')
        tt=np.where(area_data[:,0]==t)
        if len(tt[0])==0:
            print(t+' out of file')
        else:
            cell_type[file.split('.')[0]]=str(area_data[tt[0],1][0])

bouton_stat=np.load('bouton_stat.npy',allow_pickle=True)
# bouton_stat=bouton_stat[:,2].astype(np.float64)
# t=np.where(bouton_stat<100)[0]
# bouton_stat=bouton_stat[t]
# plt.close()
# plt.hist(bouton_stat,bins=round(max(bouton_stat)/10))
# print(1/np.mean(bouton_stat))

## 筛选出某个特定
## somatosensory cortex
# special=['SS','SSp','SSp-n','SSp-bfd','VISrll','SSp-ll','SSp-m','SSp-ul','SSp-tr','SSp-un']
## Thalamus
# special=["TH","DORsm","VENT","VAL","VM","VP","VPL","VPLpc","VPM","VPMpc","PoT","SPF","SPFm","SPFp","SPA","PP","GENd","MG","MGd","MGv","MGm","LGd","LGd-sh","LGd-co","LGd-ip","DORpm","LAT","LP","PO","POL","SGN","Eth","REth","ATN","AV","AM","AMd","AMv","AD","IAM","IAD","LD","MED","IMD","MD","MDc","MDl","MDm","SMT","PR","MTN","PVT","PT","RE","Xi","ILM","RH","CM","PCN","CL","PF","PIL","RT","GENv","IGL","IntG","LGv","LGvl","LGvm","SubG","EPI","MH","LH","PIN",]
## cortical layers
# special=["FRP","FRP1","FRP2/3","FRP5","FRP6a","FRP6b","MO","MO1","MO2/3","MO5","MO6a","MO6b","MOp","MOp1","MOp2/3","MOp5","MOp6a","MOp6b","MOs","MOs1","MOs2/3","MOs5","MOs6a","MOs6b","SS","SS1","SS2/3","SS4","SS5","SS6a","SS6b","SSp","SSp1","SSp2/3","SSp4","SSp5","SSp6a","SSp6b","SSp-n","SSp-n1","SSp-n2/3","SSp-n4","SSp-n5","SSp-n6a","SSp-n6b","SSp-bfd","SSp-bfd1","SSp-bfd2/3","SSp-bfd4","SSp-bfd5","SSp-bfd6a","SSp-bfd6b","VISrll","VISrll1","VISrll2/3","VISrll4","VISrll5","VISrll6a","VISrll6b","SSp-ll","SSp-ll1","SSp-ll2/3","SSp-ll4","SSp-ll5","SSp-ll6a","SSp-ll6b","SSp-m","SSp-m1","SSp-m2/3","SSp-m4","SSp-m5","SSp-m6a","SSp-m6b","SSp-ul","SSp-ul1","SSp-ul2/3","SSp-ul4","SSp-ul5","SSp-ul6a","SSp-ul6b","SSp-tr","SSp-tr1","SSp-tr2/3","SSp-tr4","SSp-tr5","SSp-tr6a","SSp-tr6b","SSp-un","SSp-un1","SSp-un2/3","SSp-un4","SSp-un5","SSp-un6a","SSp-un6b","SSs","SSs1","SSs2/3","SSs4","SSs5","SSs6a","SSs6b","GU","GU1","GU2/3","GU4","GU5","GU6a","GU6b","VISC","VISC1","VISC2/3","VISC4","VISC5","VISC6a","VISC6b","AUD","AUDd","AUDd1","AUDd2/3","AUDd4","AUDd5","AUDd6a","AUDd6b","VISlla","VISlla1","VISlla2/3","VISlla4","VISlla5","VISlla6a","VISlla6b","AUDp","AUDp1","AUDp2/3","AUDp4","AUDp5","AUDp6a","AUDp6b","AUDpo","AUDpo1","AUDpo2/3","AUDpo4","AUDpo5","AUDpo6a","AUDpo6b","AUDv","AUDv1","AUDv2/3","AUDv4","AUDv5","AUDv6a","AUDv6b","VIS","VIS1","VIS2/3","VIS4","VIS5","VIS6a","VIS6b","VISal","VISal1","VISal2/3","VISal4","VISal5","VISal6a","VISal6b","VISam","VISam1","VISam2/3","VISam4","VISam5","VISam6a","VISam6b","VISl","VISl1","VISl2/3","VISl4","VISl5","VISl6a","VISl6b","VISp","VISp1","VISp2/3","VISp4","VISp5","VISp6a","VISp6b","VISpl","VISpl1","VISpl2/3","VISpl4","VISpl5","VISpl6a","VISpl6b","VISpm","VISpm1","VISpm2/3","VISpm4","VISpm5","VISpm6a","VISpm6b","VISli","VISli1","VISli2/3","VISli4","VISli5","VISli6a","VISli6b","VISpor","VISpor1","VISpor2/3","VISpor4","VISpor5","VISpor6a","VISpor6b","ACA","ACA1","ACA2/3","ACA5","ACA6a","ACA6b","ACAd","ACAd1","ACAd2/3","ACAd5","ACAd6a","ACAd6b","ACAv","ACAv1","ACAv2/3","ACAv5","ACAv6a","ACAv6b","PL","PL1","PL2","PL2/3","PL5","PL6a","PL6b","ILA","ILA1","ILA2","ILA2/3","ILA5","ILA6a","ILA6b","ORB","ORB1","ORB2/3","ORB5","ORB6a","ORB6b","ORBl","ORBl1","ORBl2/3","ORBl5","ORBl6a","ORBl6b","ORBm","ORBm1","ORBm2","ORBm2/3","ORBm5","ORBm6a","ORBm6b","ORBv","ORBvl","ORBvl1","ORBvl2/3","ORBvl5","ORBvl6a","ORBvl6b","AI","AId","AId1","AId2/3","AId5","AId6a","AId6b","AIp","AIp1","AIp2/3","AIp5","AIp6a","AIp6b","AIv","AIv1","AIv2/3","AIv5","AIv6a","AIv6b","RSP","RSPagl","RSPagl1","RSPagl2/3","RSPagl5","RSPagl6a","RSPagl6b","VISmma","VISmma1","VISmma2/3","VISmma4","VISmma5","VISmma6a","VISmma6b","VISmmp","VISmmp1","VISmmp2/3","VISmmp4","VISmmp5","VISmmp6a","VISmmp6b","VISm","VISm1","VISm2/3","VISm4","VISm5","VISm6a","VISm6b","RSPd","RSPd1","RSPd2/3","RSPd4","RSPd5","RSPd6a","RSPd6b","RSPv","RSPv1","RSPv2","RSPv2/3","RSPv5","RSPv6a","RSPv6b","PTLp","PTLp1","PTLp2/3","PTLp4","PTLp5","PTLp6a","PTLp6b","VISa","VISa1","VISa2/3","VISa4","VISa5","VISa6a","VISa6b","VISrl","VISrl1","VISrl2/3","VISrl4","VISrl5","VISrl6a","VISrl6b","TEa","TEa1","TEa2/3","TEa4","TEa5","TEa6a","TEa6b","PERI","PERI6a","PERI6b","PERI1","PERI5","PERI2/3","ECT","ECT1","ECT2/3","ECT5","ECT6a","ECT6b",]
## layer 1 of mouse primary motor cortex
special=['MOp']
cell_list=[]
for key in cell_type.keys():
    if cell_type[key] in special:
        cell_list.append(key)
new_stat=[]
for x in bouton_stat:
    if x[0] in cell_list:
        new_stat.append(x)
new_stat=np.array(new_stat)
new_stat=new_stat[:,2].astype(np.float64)
t=np.where(new_stat<100)[0]
new_stat=new_stat[t]
plt.close()
plt.hist(new_stat,bins=round(max(new_stat)/10))
print(1/np.mean(new_stat))
'''
sholl_result=np.load('sholl_result.npy', allow_pickle=True).item()
sholl_result_density=np.load('sholl_result_density_all.npy', allow_pickle=True).item()
## 全局的均值
best_par=dict()
maxlen=0
count=0

for key in cell_type:
    if len(sholl_result[key][0])>maxlen:
        maxlen=len(sholl_result[key][0])
    if len(sholl_result_density[key])>maxlen:
        maxlen=len(sholl_result_density[key])
    count+=1
sholl_data=np.zeros((4,count,maxlen))

count=0
for key in cell_type:
    t=len(sholl_result[key][0])
    sholl_data[0:3,count,0:t]=sholl_result[key]
    t=len(sholl_result_density[key])
    sholl_data[3,count,0:t]=sholl_result_density[key]
    count+=1
# # 找到每个cell type的bouton和boutondensity的最优参数
bouton_result=np.mean(sholl_data[0,:,:],0)
boutondensity=np.mean(sholl_data[3,:,:],0)
st=round(np.mean(boutondensity)/np.mean(bouton_result),3)*1000-5000
end=round(np.mean(boutondensity)/np.mean(bouton_result),3)*1000+1000
record=[]
for k in range(int(st),int(end)):
    boutondensity_new=boutondensity*k/1000
    res=bouton_result-boutondensity_new
    loss=np.sum(np.square(res))
    record.append(loss)
# plt.plot(record)
best_par['all']=(st+record.index(min(record)))/1000
# best_pair_t=np.load('best_density.npy', allow_pickle=True).item()
# np.save('best_density.npy',best_par)

x_as=[i*100 for i in range(1,maxlen+1)]

plt.close('all')
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('Length(um)')
ax1.set_ylabel('Cable length', color=color)
ax1.plot(x_as, np.mean(sholl_data[1,:,:],0), color=color,label='cable_length',linewidth=3)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
# ax2.set_ylabel('Bouton', color=color)  # we already handled the x-label with ax1
ax2.plot(x_as, np.mean(sholl_data[0,:,:],0), color=color,label='bouton',linewidth=3)
ax2.tick_params(axis='y')
color = 'tab:green'
ax2.plot(x_as, np.mean(sholl_data[2,:,:],0), color=color,label='branch_points',linewidth=3)
color = 'tab:orange'
ax2.plot(x_as, np.mean(sholl_data[3,:,:],0), color=color,label='boutondensity',linewidth=3)

ax2.legend(['Bouton','Branch points','Bouton density'])
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
# plt.savefig(name+'_all.png', dpi=300)
'''