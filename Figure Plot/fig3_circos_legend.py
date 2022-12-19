import numpy as np
import matplotlib.pyplot as plt

upper_name={'549':'TH','477':'STR','1089':'HPF','703':'CTXsp','315':'Isocortex'}
color_map=np.load("../Data/Other_Infomation/color_network.npy",allow_pickle=True).item()

plt.close()
fig,ax=plt.subplots(figsize=(6,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
x=range(0,10)
y=[1]*10
for area in list(upper_name.values()):
    plt.plot(x,y,c=color_map[area],linewidth=4,label=area)
plt.legend(prop={'family':'Calibri','weight':'bold','size':16},frameon=False)
plt.tight_layout()
# plt.savefig('regions legend.png', dpi=300)

name=["Community 1","Community 2","Community 3"]
color_map={"Community 1":"#FF0000","Community 2":"#00FF00","Community 3":"#0000FF"}

plt.close()
fig,ax=plt.subplots(figsize=(6,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
x=range(0,10)
y=[1]*10
for area in name:
    plt.plot(x,y,c=color_map[area],linewidth=4,label=area)
plt.legend(prop={'family':'Calibri','weight':'bold','size':16},frameon=False)
# plt.xlabel('Path length(um)',fontsize=22,fontproperties='Calibri',weight='bold')
# plt.ylabel('Frequency(log)',fontsize=22,fontproperties='Calibri',weight='bold')
# plt.title('Distribution of path length betwen axon boutons',fontsize=14)
plt.tight_layout()
# plt.savefig('cluster legend.png', dpi=300)



plt.close()
fig,ax=plt.subplots(figsize=(6,4))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
x=range(0,10)
y=[1]*10
for i in range(2):
    plt.plot(x,y,linewidth=4)
plt.legend(['Predicted','Uniform'],prop={'family':'Calibri','weight':'bold','size':16},frameon=False)
# plt.xlabel('Path length(um)',fontsize=22,fontproperties='Calibri',weight='bold')
# plt.ylabel('Frequency(log)',fontsize=22,fontproperties='Calibri',weight='bold')
# plt.title('Distribution of path length betwen axon boutons',fontsize=14)
plt.tight_layout()
plt.savefig('radar legend.png', dpi=300)