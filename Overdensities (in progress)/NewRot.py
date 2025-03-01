import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.neighbors import KDTree
 

data = pd.read_csv('stack100^3rvir.csv') #Mvir,x,y,z, rvir
n=len(data.iloc[:,0])-1 #number of data values 
pairs = np.array([7000,22204,4210,14353,10284,10248])
XYZ = data.iloc[:,1:4]


def environment(halo1,halo2):           #function to find the indexes of DM haloes around each of the two clusters
    global ind1
    global ind2
    tree = KDTree(XYZ, leaf_size=2)     
    ind = tree.query_radius(D1, r=30)       
    for indices in ind:                 #ind (index) is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            ind1.append(i)
    ind = tree.query_radius(D2, r=30)
    for indices in ind:
        for i in indices:
            ind2.append(i)


def rotation(rotate):           #A function to create arrays for the scatter plot containing x and y coordinates. For cluster 1 this uses the origional coordinates. For cluster 2, they are randomly rotated and then put at a distance of 1 * Xsep to the right of cluster 1.
    for i in ind1:
        xc1.append(data.iloc[i,1])  
        yc1.append(data.iloc[i,2])                      
    for i in ind2:    #A for loop that collects transformed x and y coordinates of the haloes surrounding cluster 2. 
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
i=0
while i <len(pairs):        #Go through the code for every pair in the non-physical pair catalogue 'pairs'.
    ind1,ind2,xc1,yc1,xc2,yc2,D1,D2 = [],[],[],[],[],[],[],[]               
    R1,R2,Xsep = 0,0,0   
    
    halo1,halo2 = pairs[i], pairs[i+1]
    print(halo1,halo2)
    D1 = data.iloc[halo1,1:4].values.reshape(1, -1)
    D2 = data.iloc[halo2,1:4].values.reshape(1, -1)
    R1 = data.iloc[halo1,4]/1000
    R2 = data.iloc[halo2,4]/1000
    Xsep = D1[0,0]-D2[0,0]
    
    environment(halo1,halo2)  
    #rotation(random.randint(0, 628)/100) #rotation function - random number between 0 and 2pi (approximately 6.28).
    rotation(0)
    plt.figure()
    plt.scatter(xc2,yc2)    #cluster 2 data
    plt.scatter(xc1,yc1)    #cluster 1 data (on the same plot)
    #plt.ylim(-20,130)
    #plt.xlim(-20,130)
    i+=2                    #plus 2 because we use two clusters (a pair) in every loop of the while loop.
    
        
    



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots section





























