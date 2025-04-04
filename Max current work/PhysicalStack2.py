import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.neighbors import KDTree
from matplotlib.colors import LogNorm
import math as math
import time

start = time.time()

#functions
def PValues():                                                                          #All of the physical cluster data for calculations 
    xc1,yc1,mc1,D1,D2 = [],[],[],[],[]                            #reset all the arrays       
    R1,R2,theta_z,theta_y,Zsep,XYZsep = 0,0,0,0,0,0
    D1 = data.iloc[cluster1,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 1
    D2 = data.iloc[cluster2,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 2
    D1origin = D1
    D2origin = D2
    R1 = data.iloc[cluster1,4]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc
    R2 = data.iloc[cluster2,4]/1000 
   
    Zsep = np.abs(D1[0,2]-D2[0,2])                                               #Virial radius of cluster 2                                                                        #This is the R_2D separation between the origional clusters in the physical pair. For testing purposes, this is set to 10 h^-1 Mpc
    XYZsep = np.sqrt((D1[0,0]-D2[0,0])**2+ (D1[0,1]-D2[0,1])**2+ (D1[0,2]-D2[0,2])**2)
    zslice = 2                                                         #set the +- slice thickness. For testing purposes this is set so that all data will be in the zslice.
    length = ((D1[0,0]+1.5*XYZsep)-(D1[0,0]-0.5*XYZsep))/bins                             #length of each box in the histogram
    height = ((D1[0,1]+XYZsep)- (D1[0,1]-XYZsep))/bins                                    #height of each box in the histogram
    vol = length * height * zslice                                                      #volume of each box in the histogram
    multiplier = 20/XYZsep
    #multiplier = 1
    
    theta_z = math.atan2((D2[0,1]-D1[0,1]),(D2[0,0]-D1[0,0]))
    #theta_y = math.atan2((D2[0,2]-D1[0,2]),(D2[0,0]-D1[0,0])) 
    #theta_z = theta_z *-1 
                                                  #angle between the two physical pairs
    Rz = np.array([[np.cos(theta_z),-1*np.sin(theta_z),0],[np.sin(theta_z),np.cos(theta_z),0],[0,0,1]])     #matrix to rotate about the z-axis
      
 
    D1 = D1 @ Rz 
    D2 = D2 @ Rz

    theta_y = math.atan2((D2[0,2]-D1[0,2]),(D2[0,0]-D1[0,0])) 
    theta_y = theta_y *-1
    Ry = np.array([[np.cos(theta_y),0,np.sin(theta_y)],[0,1,0],[-1*np.sin(theta_y),0,np.cos(theta_y)]])     #matrix to rotate about the y-axis  

    D1 = D1 @ Ry
    D2 = D2 @ Ry   
       
                                                                                    #calculate new co-ords for the second cluster after rotation
    ClustersX = np.array([D1[0,0],D2[0,0]])                                                                 #Cluster 1 and 2 x co-ords
    ClustersY = np.array([D1[0,1],D2[0,1]])                                                                 #Cluster 1 and 2 y co-ords
    #[D1[0,0]*multiplier,(D1[0,0]+XYZsep)*multiplier],[D1[0,1]*multiplier,D1[0,1]*multiplier]
                            #These if statements make sure that the x and y lims of the plot stay consistant even if the two clusters are in opposite order.

    lims = [[(D1[0,0]*multiplier-10), D1[0,0]*multiplier+30], [D1[0,1]*multiplier-20, D1[0,1]*multiplier+20]]

        

    

    return xc1,yc1,mc1,D1,D2,R1,R2,zslice,vol,ClustersX,ClustersY,theta_z,theta_y,lims,Zsep,XYZsep,D1origin,D2origin,multiplier  


def Penvironment(cluster1,cluster2):             #A function to find the indexes of DM haloes around each of the two clusters        
    global ind1
    ind1,indVir1,indVir2 = [],[],[]

    tree = KDTree(XYZ, leaf_size=2)
   
    indVir = tree.query_radius(D1origin, r=R1*2)      #indVir gathers the indicies of all haloes within 2*Virial radius of the first cluster in the non-physical pair. 2*Virial radius is chosen to isolate filaments from clusters.   
    for indices in indVir:                      #indVir is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            indVir1.append(i)                   #indVir1 now contains indVir in a usable format
    
    indVir = tree.query_radius(D2origin, r=R2*2)      #Do the same for the second cluster
    for indices in indVir:                 
         for i in indices:
             indVir2.append(i) 
  
    ind = tree.query_radius((D1origin+D2origin)/2, r=(np.sqrt((XYZsep)**2+ XYZsep**2+ (zslice)**2)))    #repeat the steps above for the midpoint between the two clusters               
    for indices in ind:
        for i in indices:
            if i not in indVir1 and i not in indVir2:   #This statement removes DM haloes within two virial radius of each cluster.  
                ind1.append(i)          
  
                
def Protation(theta_z,theta_y):                           #A function for physical pairs to create arrays containing x and y coordinates of DM haloes and their mass densities. This is done for the two clusters separately. Cluster 2 is rotated by a random value between 0 and 2 pi, given by the variable 'rotate'. 
    global rot
    
    Rz = np.array([[np.cos(theta_z),-1*np.sin(theta_z),0],[np.sin(theta_z),np.cos(theta_z),0],[0,0,1]])
    Ry = np.array([[np.cos(theta_y),0,np.sin(theta_y)],[0,1,0],[-1*np.sin(theta_y),0,np.cos(theta_y)]])
    for i in ind1:
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])

        rot = rot @ Rz      

        rot = rot @ Ry 

        if np.abs(D1[0,2]-rot[2])< zslice:              #makes sure all data points are within the zslice. Any DM halo with z value now within the zslice is removed
            mc1.append(data.iloc[i,0]/vol)
            xc1.append(rot[0]*multiplier)  
            yc1.append(rot[1]*multiplier)

def Pplot():                                                                                    #plotting sum of physical and non-physical pairs    
    global Filament     #making filament and pcombined global for testing purposes
    global Stack
    global p
    p, _, _ = np.histogram2d(xc1, yc1, bins=(bins, bins), range = lims, weights=mc1)           #physical pair histogram data for mass density of DM haloes around cluster 1
    Stack += p
    '''
    plt.figure()
    plt.plot(xc1,yc1,'.')
    plt.plot([D1[0,0]*multiplier,(D1[0,0]+XYZsep)*multiplier],[D1[0,1]*multiplier,D1[0,1]*multiplier],color = 'red',marker='*',markersize=12)
    
    
    
    
    Filament = np.rot90(p)                                                               #The data has to be rotated by 90 degrees for plt.imshow()        
    plt.figure()
    plt.imshow(Filament,norm=LogNorm())                                                         #Plot the mass density histogram
    plt.colorbar()
    plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
    plt.axis('scaled')                                                                                               
    '''
    
#end of functions


data = pd.read_csv('100box.csv')

n=len(data.iloc[:,0])-1                         #number of data values 

Ppairs = np.array(pd.read_csv('Pparirs1.csv',header=None))    
#Ppairs = np.array([4035,4156,2714,2798,2900,3100])                  #Array containing the physical pairs
                                             
                                                #big haloes in the are 2714,2798, 4035,4156,6608,11670

XYZ = data.iloc[:,1:4]
bins = 100                                                                                                  #set the number of bins in the histogram
Stack = np.zeros((bins,bins))                                                                               #create an array to contain the stacking of non-physical pairs
i=0
 

                                                                                     #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
select = 2930
while i <len(Ppairs)-select:   
    cluster1,cluster2 = Ppairs[i], Ppairs[i+1]                                        #take the first non-physical pair from the pair catalogue
    xc1,yc1,mc1,D1,D2,R1,R2,zslice,vol,ClustersX,ClustersY,theta_z,theta_y,lims,Zsep,XYZsep,D1origin,D2origin, multiplier = PValues()    
    
    
    Penvironment(cluster1,cluster2)                                                        #Rotation function - random number between 0 and 2pi (approximately 6.28).
    Protation(theta_z,theta_y)                                                                                        
    Pplot() 
    
    i+=2    
    

Filament = np.rot90(Stack/(len(Ppairs)-select))                                                               #The data has to be rotated by 90 degrees for plt.imshow()        
plt.figure()
plt.imshow(Filament,interpolation='nearest',norm=LogNorm())                                                         #Plot the mass density histogram
plt.colorbar()
plt.show()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
plt.axis('scaled') 
end = time.time()
print(end-start)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots for testing




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#