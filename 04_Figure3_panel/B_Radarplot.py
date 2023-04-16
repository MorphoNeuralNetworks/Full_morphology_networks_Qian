'''
Radar plot of network properties: cost, storage capacity, routing efficiency
'''
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
data=np.load('../Data/Network_Data/CostStorageRouting_normal.npy')
results=[]
for i in data:
    x=i.tolist()
    x[0]=1
    x=list(map(float,x))
    temp=dict()
    temp['Cost(1e5)']=x[1]/100000
    temp['Storage capacity(1e2)']=x[2]/100
    temp['Routing efficiency']=x[3]
    # temp['Storage/Cost(1e-3)']=x[2]/x[1]*1000
    # temp['Routing/Cost(1e-5)']=x[3]/x[1]*100000
    results.append(temp)

print(results[2]["Cost(1e5)"]/results[0]["Cost(1e5)"])
print(results[2]["Storage capacity(1e2)"]/results[0]["Storage capacity(1e2)"])
print(results[2]["Routing efficiency"]/results[0]["Routing efficiency"])

data_length = len(results[0])
# equate the polar coordinates according to the length of the data
angles = np.linspace(0, 2*np.pi, data_length, endpoint=False)
labels = [key for key in results[0].keys()]
score = [[v for v in result.values()] for result in results]
# make radar map data closed
score_a = np.concatenate((score[0], [score[0][0]]))
score_b = np.concatenate((score[1], [score[1][0]]))
score_c = np.concatenate((score[2], [score[2][0]]))
angles = np.concatenate((angles, [angles[0]]))
labels = np.concatenate((labels, [labels[0]]))

# set the size of the figure
plt.close('all')
fig = plt.figure(figsize=(8,4))
# create a new subplot
ax = plt.subplot(111, polar=True)
# plot radar maps
ax.plot(angles, score_a,c="#1f77b4", linewidth=3)
ax.plot(angles, score_c,c="#ff7f0e", linewidth=3)
ax.plot(angles, score_b,c="#7f7f7f", linewidth=3)
# set the label display
ax.set_thetagrids(angles*180/np.pi, labels,fontsize=20,fontproperties='Calibri',weight='bold')
# set 0 degree start position
ax.set_theta_zero_location('N')
# set the coordinate scale range
# ax.set_rlim(0, 100)
# set the coordinate value display angle, offset relative to the starting angle
ax.set_rlabel_position(270)
plt.legend(['Predicted','Uniform','Same density'],prop={'family':'Calibri','weight':'bold','size':14},frameon=False,loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
plt.tight_layout()
# plt.savefig('feature_radar.pdf', dpi=300)
