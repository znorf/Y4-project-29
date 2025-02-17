import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random


data = pd.read_csv('stack100^3rvir.csv') #Mvir,x,y,z, rvir
n=len(data.iloc[:,0])-1 #number of data values 

halo1 = 640
halo2 = 719
x1,y1,z1,r1 = data.iloc[halo1,1],data.iloc[halo1,2],data.iloc[halo1,3],data.iloc[halo1,4]/1000    #x,y,z, virial radius data for the first cluster. rvir/1000 to convert to h^-1Mpc from h^-1Kpc.
x2,y2,z2,r2 = data.iloc[halo2,1],data.iloc[halo2,2],data.iloc[halo2,3], data.iloc[halo2,4]/1000
Rsep = np.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2 + abs(z1-z2)**2)  
Xsep = x1-x2                     #3D separation between the two clusters
particles1 = []
particles2 = []
xc1 = []
yc1 = []
xc2 = []
yc2 = []

def environment(halo1,halo2):
    for i in range(1,n): 

        dx1=data.iloc[halo1,1]-data.iloc[i,1] 
        dx2=data.iloc[halo2,1]-data.iloc[i,1] 
        dy1=data.iloc[halo1,2]-data.iloc[i,2] 
        dy2=data.iloc[halo2,2]-data.iloc[i,2]
        dz1=data.iloc[halo1,3]-data.iloc[i,3]
        dz2=data.iloc[halo2,3]-data.iloc[i,3]

        ds1=np.sqrt(dx1**2+dy1**2+dz1**2) 
        ds2=np.sqrt(dx2**2+dy2**2+dz2**2) 

        if ds1<=1.5*Rsep and ds1>=2*r1: #criteria for physical pairs  
            particles1.append(i)
        if ds2<=1.5*Rsep and ds2>=2*r1: #criteria for physical pairs  
            particles2.append(i)

def rotation(rotate):
    #starting by rotating around the x-axis.

   
    for i in particles2:
        #Rx = np.array([[1,0,0],[0,np.cos(rotate),-1*np.sin(rotate)],[0,np.sin(rotate),np.cos(rotate)]])
        Rz = np.array([[np.cos(rotate),-1*np.sin(rotate),0],[np.sin(rotate),np.cos(rotate),0],[0,0,1]])
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])
        rot1 = rot - np.array([[data.iloc[halo2,1],data.iloc[halo2,2],data.iloc[halo2,3]]])
        rot1 = rot1 @ Rz
        
        rot1 = rot1 + np.array([data.iloc[halo1,1]+Xsep,data.iloc[halo1,2],data.iloc[halo1,3]])
        rot1=rot1.transpose()
        xc2.append(rot1[0])
        yc2.append(rot1[1])
    
    for i in particles1:
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])
        xc1.append(rot[0])
        yc1.append(rot[1])



environment(halo1,halo2)
rotation(random.randint(0, 628)/100)


#fig, ax = plt.subplots()

plt.scatter(xc2,yc2)
plt.scatter(xc1,yc1)
plt.ylim(-20,50)
plt.xlim(10,110)


















