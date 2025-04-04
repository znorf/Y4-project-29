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
    ind = tree.query_radius((D1origin+D2origin)/2, r=(np.sqrt((XYZsep/2)**2+ (XYZsep/2)**2+ (zslice)**2)))
    #ind = tree.query_radius(D1origin, r=(np.sqrt((XYZsep*1.5)**2+ XYZsep**2+ (zslice)**2)))    #repeat the steps above for the second cluster in the non-physical pair.            
    for indices in ind:
        for i in indices:
            if i not in indVir1 and i not in indVir2:   #This statement removes DM haloes within two virial radius of each cluster.  
                ind1.append(i)          
  
                
def Protation(theta_z,theta_y):                           #A function for physical pairs to create arrays containing x and y coordinates of DM haloes and their mass densities. This is done for the two clusters separately. Cluster 2 is rotated by a random value between 0 and 2 pi, given by the variable 'rotate'. 
    global rot
    global R
    R=[] # check!
      
    Rz = np.array([[np.cos(theta_z),-1*np.sin(theta_z),0],[np.sin(theta_z),np.cos(theta_z),0],[0,0,1]])
    Ry = np.array([[np.cos(theta_y),0,np.sin(theta_y)],[0,1,0],[-1*np.sin(theta_y),0,np.cos(theta_y)]])
    for i in ind1:
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])
        rot = rot @ Rz      
        rot = rot @ Ry 
        if np.abs(D1[0,2]-rot[2])< zslice:              #makes sure all data points are within the zslice. Any DM halo with z value now within the zslice is removed
            y = (rot[1]*multiplier)-D1[0,1]*multiplier    
            z = (rot[2]*multiplier)-D1[0,2] *multiplier   
            r = np.sqrt(y**2+z**2)
            if r > binss[0]:
                R.append(r)
                for k in range(len(binss)):
                    
                    if r < binss[k]:
                       
                        
                        vol = (np.pi*XYZsep*(binss[k]**2)-(np.pi*XYZsep*(binss[k-1]**2)))
                        #print(binss[k])
                        #print(vol)
                        #print('1',vol,np.pi*XYZsep*(binss[i]**2),np.pi*XYZsep*(binss[i-1]**2),r,'2')
                        mc1.append(data.iloc[i,0]/vol)
                        #print('1',r,binss[k],binss[k-1],data.iloc[i,0]/vol,'2')
                        break


def Pplot():                                                                                    #plotting sum of physical and non-physical pairs    
    global Filament     #making filament and pcombined global for testing purposes
    global Stack
    global p
    global v
    p,v = [],[]
 
    #plt.figure()   
    #j,_,_ = plt.hist(R, bins = binss,weights=mc1)
    p,v = np.histogram(R, bins = binss,weights=mc1)
    #plt.hist(R, bins = 50,range = [0,20],weights=mc1)           #physical pair histogram data for mass density of DM haloes around cluster 1
    #plt.hist(R, bins = binss ,weights=mc1)   
    Stack += p
                                                                                            
    
#end of functions


data = pd.read_csv('100box.csv')

n=len(data.iloc[:,0])-1                         #number of data values 
    
Ppairs = np.array(pd.read_csv('Pparirs1.csv',header=None)) 
#Ppairs = np.array([4035,4156,2714,2798,2900,3100])                  #Array containing the physical pairs
#Npairs = np.array([2714,2798,2900,3100])                  #Array containing the non-physical pairs                                                
                                                #big haloes in the are 2714,2798, 4035,4156,6608,11670

XYZ = data.iloc[:,1:4]
bins = 100 
select = 2938                                                                                              #set the number of bins in the histogram                                                                           #create an array to contain the stacking of non-physical pairs
i=0

binss = np.arange(0.05,20,0.1) 
  
Stack = np.zeros(len(binss)-1)                                                                                  #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
rand =random.sample(range(0, int(len(Ppairs)/2)), int(select/2))

                                                                              #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
for i in rand:    
    i=i*2
    cluster1,cluster2 = Ppairs[i], Ppairs[i+1]                                        #take the first non-physical pair from the pair catalogue
    xc1,yc1,mc1,D1,D2,R1,R2,zslice,vol,ClustersX,ClustersY,theta_z,theta_y,lims,Zsep,XYZsep,D1origin,D2origin, multiplier = PValues()
    Penvironment(cluster1,cluster2)                                                        #Rotation function - random number between 0 and 2pi (approximately 6.28).
    Protation(theta_z,theta_y)                                                                                        #Rotation of 0 degrees for testing purposes
    Pplot()                                                                  
   
    
v=(np.delete(v,-1))+0.05
plt.figure()                                                               
plt.plot(v,Stack/((select)))
plt.xscale('log')
plt.xlim(0.1,20)
end = time.time()
print(end-start)
#=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots for testing



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
