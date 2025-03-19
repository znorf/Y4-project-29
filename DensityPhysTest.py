import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.neighbors import KDTree
from matplotlib.colors import LogNorm
import math as math

data = pd.read_csv('stack100^3rvir.csv') #Mvir,x,y,z, rvir
n=len(data.iloc[:,0])-1 #number of data values 
#pairs = np.array([8399,8803])       #random set of points until we have a non-physical pair catalogue.
pairs = np.array([6608,4156])
#big haloes are 2714,2798, 4035,4156,6608,11670

XYZ = data.iloc[:,1:4]
   


def environment(halo1,halo2):           #function to find the indexes of DM haloes around each of the two clusters
    global ind1
    global ind2
    tree = KDTree(XYZ, leaf_size=2)     
    ind = tree.query_radius(D1, r=XYsep*1.5)       
    for indices in ind:                 #ind (index) is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            ind1.append(i)
    ind = tree.query_radius(D2, r=XYsep*1.5)
    for indices in ind:
        for i in indices:
            ind2.append(i)


def rotation(rotate):           #A function to create arrays for the scatter plot containing x and y coordinates. For cluster 1 this uses the origional coordinates. For cluster 2, they are randomly rotated and then put at a distance of 1 * Xsep to the right of cluster 1.
    Rz = np.array([[np.cos(rotate),-1*np.sin(rotate),0],[np.sin(rotate),np.cos(rotate),0],[0,0,1]])
    for i in ind1:
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])
        rot = rot @ Rz
        
        mc1.append(data.iloc[i,0])
        xc1.append(rot[0])  
        yc1.append(rot[1])                     
    for i in ind2:    #A for loop that collects transformed x and y coordinates of the haloes surrounding cluster 2. 
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])
        rot = rot @ Rz  
        
        mc2.append(data.iloc[i,0])
        xc2.append(rot[0])  
        yc2.append(rot[1]) 


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section
i=0
while i <len(pairs):        #Go through the code for every pair in the non-physical pair catalogue 'pairs'.
    ind1,ind2,xc1,yc1,mc1,xc2,yc2,mc2,D1,D2 = [],[],[],[],[],[],[],[],[],[]           #reset all the arrays       
    R1,R2,Xsep = 0,0,0   
    
    halo1,halo2 = pairs[i], pairs[i+1]
    D1 = data.iloc[halo1,1:4].values.reshape(1, -1)   
    D2 = data.iloc[halo2,1:4].values.reshape(1, -1) 
    theta = math.atan2((D2[0,1]-D1[0,1]),(D2[0,0]-D1[0,0]))
    #theta = (2)
    
    R1 = data.iloc[halo1,4]/1000
    R2 = data.iloc[halo2,4]/1000
    
    XYsep = np.sqrt((D1[0,0]-D2[0,0])**2+(D1[0,1]-D2[0,1])**2)
    zslice = D1[0,2]-D2[0,2]/2         #set the +- slice thickness. This will probably be changed.


    environment(halo1,halo2)  
    rotation(theta)
    #rotation(0)
    Rz = np.array([[np.cos(theta),-1*np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
    D2 = D2 @ Rz 
    D1 = D1 @ Rz
    ClustersX = np.array([D1[0,0],D2[0,0]])
    ClustersY = np.array([D1[0,1],D2[0,1]])
    if D1[0,0]<D2[0,0]:                 #way to make sure that the axis stay the same even if the two clusters are in opposite order.
        if D1[0,1]<D2[0,2]:
            lims = [[D1[0,0]-0.5*XYsep, D2[0,0]+0.5*XYsep], [D1[0,1]-XYsep, D2[0,1]+XYsep]]
        else:
            lims = [[D1[0,0]-0.5*XYsep, D2[0,0]+0.5*XYsep], [D2[0,1]-XYsep,D1[0,1]+XYsep]]
    if D1[0,0]>D2[0,0]:                    
        if D1[0,1]<D2[0,2]:
            lims = [[D2[0,0]-0.5*XYsep,D1[0,0]+0.5*XYsep], [D1[0,1]-XYsep, D2[0,1]+XYsep]]
        else: 
            lims = [[D2[0,0]-0.5*XYsep,D1[0,0]+0.5*XYsep], [D2[0,1]-XYsep,D1[0,1]+XYsep]]
    
    h1,_,_,_ = plt.hist2d(xc1, yc1, bins=(100, 100),weights = mc1,norm=LogNorm(),range=lims)
    plt.colorbar()
    plt.plot(ClustersX,ClustersY,color = 'red',marker='*',markersize=12)
    plt.axis('scaled')
    plt.figure()
    h2,_,_,_ = plt.hist2d(xc2, yc2, bins=(100, 100),weights = mc2,norm=LogNorm(),range=lims)
    plt.colorbar()
    plt.plot(ClustersX,ClustersY,color = 'red',marker='*',markersize=12)
    plt.axis('scaled')

    combined = h1+h2
    plt.figure()
    plt.imshow(combined,norm=LogNorm())
    plt.colorbar()
    #plt.plot(ClustersX,ClustersY,color = 'red',marker='*',markersize=12)
    plt.axis('scaled')
    i+=2  
  
