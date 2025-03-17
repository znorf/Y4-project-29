import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.neighbors import KDTree
from matplotlib.colors import LogNorm


data = pd.read_csv('stack100^3rvir.csv')        #Mvir,x,y,z, rvir from a 100*100*100 h^-3 Mpc^3 sample with masses above 10^11 h^-1 solar masses
n=len(data.iloc[:,0])-1                         #number of data values 
    
pairs = np.array([4035,4156])                   #Array containing the non-physical pairs
                                                #big haloes in the are 2714,2798, 4035,4156,6608,11670

XYZ = data.iloc[:,1:4]


def environment(cluster1,cluster2):             #A function to find the indexes of DM haloes around each of the two clusters        
    global ind1
    global ind2
    indVir1 = []
    indVir2 = []
    tree = KDTree(XYZ, leaf_size=2)
     
    ind = tree.query_radius(D1, r=XYsep*1.5)    #ind gathers the indicies of all haloes within a certain radius of the first cluster in the non-physical pair. 1.5* the R_2D of the origional physical pair.
    indVir = tree.query_radius(D1, r=R1*2)      #indVir gathers the indicies of all haloes within 2*Virial radius of the first cluster in the non-physical pair. 2*Virial radius is chosen to isolate filaments from clusters.
    
    for indices in indVir:                      #indVir is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            indVir1.append(i)                   #indVir1 now contains indVir in a usable format
    
    for indices in ind:                         #ind (index) is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            if np.abs(D1[0,2]-data.iloc[i,3])< zslice and i not in indVir1:     #This filters the haloes so that only those within z values +- a certain value from the first cluster in the non-physical pair are allowed. The second statement filters out all haloes within 2*Virial radius of the first cluster in the non-physical pair
                ind1.append(i)
     
    ind = tree.query_radius(D2, r=XYsep*1.5)    #repeat the steps above for the second cluster in the non-physical pair.
    indVir = tree.query_radius(D2, r=R2*2)

    for indices in indVir:                 
         for i in indices:
             indVir2.append(i)
             
    for indices in ind:
        for i in indices:
            if np.abs(D2[0,2]-data.iloc[i,3])< zslice and i not in indVir2:
                ind2.append(i)

def rotation(rotate):                           #A function to create arrays containing x and y coordinates of DM haloes and their mass densities. This is done for the two clusters separately. Cluster 2 is rotated by a random value between 0 and 2 pi, given by the variable 'rotate'. 
    for i in ind1:                              
        mc1.append(data.iloc[i,0]/vol)          #Add the mass density of a DM halo around Cluster 1  
        xc1.append(data.iloc[i,1])              #Add the x co-ords of a DM halo around Cluster 1
        yc1.append(data.iloc[i,2])              #Add ther y co-ords of a DM halo around Cluster 1
        
    for i in ind2:                              #For cluster 2, x and y co-ords are randomly rotated and then put at a distance of 1 * Xsep to the right of cluster 1.

        Rz = np.array([[np.cos(rotate),-1*np.sin(rotate),0],[np.sin(rotate),np.cos(rotate),0],[0,0,1]])     #Matrix to rotate a set of coordinates around the z-axis.
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])                                      #Collect the x,y,z coordinates of a DM halo around cluster 2.
        rot = rot - np.array([[data.iloc[cluster2,1],data.iloc[cluster2,2],data.iloc[cluster2,3]]])         #Translate the x,y,z coordinates to the origin so that the rotation is about the origin
        rot = rot @ Rz                                                                                      #Matrix multiplicaiton of the x,y,z coordinates and the rotation matrix. This rotates the x,y,z co-ords about the z axis by a random value given by the variable 'rotate'.
        rot = rot + np.array([data.iloc[cluster1,1]+XYsep,data.iloc[cluster1,2],data.iloc[cluster1,3]])     #Translate the new x,y,z coordinates that are centred at the same y level and 1 * Xsep to the right of cluster 1.
        rot=rot.transpose()                                                                                 #Transpose the matrix as we need to to swap columns and rows after the matrix multiplication.
        xc2.extend(rot[0])                                                                                  #Add the x co-ords of a DM halo around Cluster 2
        yc2.extend(rot[1])                                                                                  #Add the y co-ords of a DM halo around Cluster 2
        mc2.append(data.iloc[i,0]/vol)                                                                      #Add the mass density of a DM halo around Cluster 2

                                        
bins = 100                                                                                                  #set the number of bins in the histogram
Stack = np.zeros((bins,bins))                                                                               #create an array to contain the stacking of non-physical pairs
i=0 
while i <len(pairs):                                                                                        #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.
    ind1,ind2,xc1,yc1,mc1,xc2,yc2,mc2,D1,D2 = [],[],[],[],[],[],[],[],[],[]                                 #reset all the arrays after every loop      
    R1,R2 = 0,0   
    
    cluster1,cluster2 = pairs[i], pairs[i+1]                                            #take the first non-physical pair from the pair catalogue
    D1 = data.iloc[cluster1,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 1
    D2 = data.iloc[cluster2,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 2
    R1 = data.iloc[cluster1,4]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc
    R2 = data.iloc[cluster2,4]/1000                                                     #Virial radius of cluster 2
    XYsep = 10                                                                          #This is the R_2D separation between the origional clusters in the physical pair. For testing purposes, this is set to 10 h^-1 Mpc
    zslice = D1[0,2]-D2[0,2]/2                                                          #set the +- slice thickness. For testing purposes this is set so that all data will be in the zslice.
    ClustersX = np.array([D1[0,0],D1[0,0]+XYsep])                                       #x co-ords of cluster 1 and 2 after translation
    ClustersY = np.array([D1[0,1],D1[0,1]])                                             #y co-ords of cluster 1 and 2 after translation
    lims = [[D1[0,0]-0.5*XYsep, D1[0,0]+1.5*XYsep], [D1[0,1]-XYsep, D1[0,1]+XYsep]]     #x and y limits of plot

    length = ((D1[0,0]+1.5*XYsep)-(D1[0,0]-0.5*XYsep))/bins                             #length of each box in the histogram
    height = ((D1[0,1]+XYsep)- (D1[0,1]-XYsep))/bins                                    #height of each box in the histogram
    vol = length * height * zslice                                                      #volume of each box in the histogram
    
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
    environment(cluster1,cluster2)  
    #rotation(random.randint(0, 628)/100)                                                       #rotation function - random number between 0 and 2pi (approximately 6.28).
    rotation(0)                                                                                 #Rotation of 0 degrees for testing purposes
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
      
    
    
    h1, _, _ = np.histogram2d(xc1, yc1, bins=(bins, bins), range = lims, weights=mc1)           #histogram data for mass density of DM haloes around cluster 1
    h2, _, _ = np.histogram2d(xc2, yc2, bins=(bins, bins), range = lims, weights=mc2)           #histogram data for mass density of DM haloes around cluster 2    
    combined = h1+h2                                                                            #histogram data for combined mass density of DM haloes around cluster 1 and cluster 2
    Stack += combined                                                                           #Stack the mass density of all non-physical pairs
    i+=2                                                                                        #+2 because each loop uses two clusters (a pair). 

Stack = np.rot90(Stack)                                                                         #The data has to be rotated by 90 degrees for plt.imshow()        
plt.figure()
plt.imshow(Stack, norm=LogNorm())                                                               #Plot the mass density histogram
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)            #Red stars to show the location of the clusters
plt.axis('scaled')   

