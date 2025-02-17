import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random


data = pd.read_csv('stack100^3rvir.csv') #Mvir,x,y,z, rvir
n=len(data.iloc[:,0])-1 #number of data values 

halo1 = 640     #choosing two random haloes to test the code on
halo2 = 719
x1,y1,z1,r1 = data.iloc[halo1,1],data.iloc[halo1,2],data.iloc[halo1,3],data.iloc[halo1,4]/1000    #x,y,z, virial radius data for the first cluster. rvir/1000 to convert to h^-1Mpc from h^-1Kpc.
x2,y2,z2,r2 = data.iloc[halo2,1],data.iloc[halo2,2],data.iloc[halo2,3], data.iloc[halo2,4]/1000
Rsep = np.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2 + abs(z1-z2)**2)       #3D separation between the two clusters
Xsep = x1-x2                                        #1-D separation in x dimension
particles1 = []
particles2 = []
xc1 = []
yc1 = []
xc2 = []
yc2 = []

def environment(halo1,halo2):           #A function (partially copied from freddie) to check the DM haloes that are within a certain radius of each cluster. 1.5 Rsep is chosen as this radius.
    for i in range(1,n):                #This for loop does through every halo and calculates the 3-D distance from each cluster.

        dx1=data.iloc[halo1,1]-data.iloc[i,1] 
        dx2=data.iloc[halo2,1]-data.iloc[i,1] 
        dy1=data.iloc[halo1,2]-data.iloc[i,2] 
        dy2=data.iloc[halo2,2]-data.iloc[i,2]
        dz1=data.iloc[halo1,3]-data.iloc[i,3]
        dz2=data.iloc[halo2,3]-data.iloc[i,3]

        ds1=np.sqrt(dx1**2+dy1**2+dz1**2) 
        ds2=np.sqrt(dx2**2+dy2**2+dz2**2) 
                                        
        if ds1<=1.5*Rsep and ds1>=2*r1: #criteria for physical pairs. Haloes within 2 virial masses of the cluster are also removed.  
            particles1.append(i)        #This if statement filters haloes and chooses only haloes nearby to a cluster and records its ID (i = position in the list).
        if ds2<=1.5*Rsep and ds2>=2*r1:  
            particles2.append(i)

def rotation(rotate):           #A function to create arrays for the scatter plot containing x and y coordinates. For cluster 1 this uses the origional coordinates. For cluster 2, they are randomly rotated and then put at a distance of 1 * Xsep to the right of cluster 1.
    for i in particles1:        #A for loop that collects the x and y coordinates of the haloes surrounding cluster 1.
        xc1.append(data.iloc[i,1])  
        yc1.append(data.iloc[i,2])                      

   
    for i in particles2:    #A for loop that collects transformed x and y coordinates of the haloes surrounding cluster 2. 
        #Rx = np.array([[1,0,0],[0,np.cos(rotate),-1*np.sin(rotate)],[0,np.sin(rotate),np.cos(rotate)]])
        Rz = np.array([[np.cos(rotate),-1*np.sin(rotate),0],[np.sin(rotate),np.cos(rotate),0],[0,0,1]])   #Matrix to rotate a set of coordinates around the z-axis.
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])      #Collect the x,y,z coordinates of a halo next to cluster 2.
        rot = rot - np.array([[data.iloc[halo2,1],data.iloc[halo2,2],data.iloc[halo2,3]]])      #Translate the x,y,z coordinates so that the rotation is about the origin
        rot = rot @ Rz                                                              #Matrix multiplicaiton of the x,y,z coordinates. This rotates about the z axis.
        rot = rot + np.array([data.iloc[halo1,1]+Xsep,data.iloc[halo1,2],data.iloc[halo1,3]])  #Translate the new x,y,z coordinates that that they are next to cluster 1.
        rot=rot.transpose()                     #Transpose the matrix as we need to to swap columns and rows.
        xc2.append(rot[0])              #collect x coordinate
        yc2.append(rot[1])              #collect y coordinate
    
    

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section

environment(halo1,halo2)            
rotation(random.randint(0, 628)/100) #rotation function - random number between 0 and 2pi.

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots section
plt.scatter(xc2,yc2)    #cluster 2 data
plt.scatter(xc1,yc1)    #cluster 1 data
plt.ylim(-20,50)
plt.xlim(10,110)


















