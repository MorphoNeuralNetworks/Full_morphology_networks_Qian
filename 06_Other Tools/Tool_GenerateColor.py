import numpy as np
import json

## convert R, G, B to hexadecimal splice conversion and capitalize them respectively
def RGB_to_Hex(tmp):
    rgb = tmp.split(',')
    strs = '#'
    for i in rgb:
        num = int(i)
        #
        strs += str(hex(num))[-2:].replace('x','0').upper()
    return strs

## get the color set for leiden detection
contents=[]
count=0
for i in range(1,8):
    t_c=round(255/i)
    contents.append(str(t_c)+',0,0')
    count+=1
    contents.append('0,'+str(t_c)+',0')
    count+=1
    contents.append('0,0,'+str(t_c))
    count+=1
    contents.append(str(t_c)+','+str(t_c)+',0')
    count+=1
    contents.append('0,'+str(t_c)+','+str(t_c))
    count+=1
    contents.append(str(t_c)+',0,'+str(t_c))
    count+=1
    # contents.append(str(t_c)+','+str(t_c)+','+str(t_c))
    # count+=1
color_dict={i:RGB_to_Hex(contents[i]) for i in range(len(contents))}
np.save("../Data/Other_InfomationOther_Infomation/leiden_color.npy",color_dict)


## color of all brain regions in CCFv3
with open(r'..\Data\Other_Infomation\tree.json','r',encoding='utf_8_sig')as fp:
    json_data = json.load(fp)
    fp.close()
area_color=dict()
for x in json_data:
    temp=str(x['rgb_triplet'][0])+','+str(x['rgb_triplet'][1])+','+str(x['rgb_triplet'][2])
    area_color[x['acronym']]=RGB_to_Hex(temp)
np.save("../Data/Other_InfomationOther_Infomation/color_network.npy",area_color)