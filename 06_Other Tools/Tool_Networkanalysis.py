import subprocess,os
import numpy as np
import math

def sc(s,d):
    n=s+d-1
    k=s
    a=0
    b=0
    k=n-k if k>n-k else k
    for j in range(1,int(k)+1):
        a+=math.log2(j)
    for j in range(int(n-k)+1,int(n)+1):
        b+=math.log2(j)
    return 2*(b-a);

def CostStorage(path,filename):
    with open(path+filename) as file_object:
        contents = file_object.readlines()
        file_object.close()
    N=int(contents[0])
    d=[0]*(N+1)
    s=[0]*(N+1)
    for x in contents[1:]:
        t=x.split(' ')
        t=list(map(float,t))
        s[int(t[1])]+=t[2]
        d[int(t[1])]+=1
    b=0
    l=0
    for i in range(0,N):
        b+=sc(s[i],d[i])
        l+=s[i]
    print("Cost is "+str(l))
    print("Storage capacity is "+str(b/N))
    return l,b/N

path="./NetworkDatFiles/"
result=[]
for root, dirs, files in os.walk(path):
    for f in files:
        temp=[f[0:-4]]
        cost,storage=CostStorage(path,f)
        temp.append(cost)
        temp.append(storage)
        
        cmd='fw.exe '+path+f+' temp.dat'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()
        command_output = process.stdout.read().decode()
        temp.append(float(command_output))
        result.append(temp)
np.save('CostStorageRouting.npy',result)