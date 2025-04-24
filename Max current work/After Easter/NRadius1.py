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
def NValues():                                                                          #All of the non-physical cluster data for calculations 
    xc1,yc1,mc1,xc2,yc2,mc2,D1,D2 = [],[],[],[],[],[],[],[]                             #reset all the arrays after every while loop      
    R1,R2,theta = 0,0,0
    XYZsep = 20 
     
    
    D1 = data.iloc[cluster1,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 1
    D2 = data.iloc[cluster2,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 2
    R1 = data.iloc[cluster1,4]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc
    R2 = data.iloc[cluster2,4]/1000                                                     #Virial radius of cluster 2                                                                                 #This is the R_2D separation between the origional clusters in the physical pair. For testing purposes, this is set to 10 h^-1 Mpc
    zslice = 2                                                         #set the +- slice thickness. For testing purposes this is set so that all data will be in the zslice.       
 
                                             #y co-ords of cluster 1 and 2 after translation
    lims = [[D1[0,0]-0.5*XYZsep, D1[0,0]+1.5*XYZsep], [D1[0,1]-XYZsep, D1[0,1]+XYZsep]]     #x and y limits of plot
    return xc1,yc1,mc1,xc2,yc2,mc2,D1,D2,R1,R2,XYZsep,zslice,cluster1,cluster2,theta,lims 


def Nenvironment(cluster1,cluster2):             #A function to find the indexes of DM haloes around each of the two clusters        
    global ind1
    global ind2
    global mid
    
    mid = (D1+ np.array([[XYZsep/2,0,0]]))/2
    ind1,ind2,indVir1,indVir2 = [],[],[],[]

    tree = KDTree(XYZ, leaf_size=2)
   
    indVir = tree.query_radius(D1, r=R1*2)      #indVir gathers the indicies of all haloes within 2*Virial radius of the first cluster in the non-physical pair. 2*Virial radius is chosen to isolate filaments from clusters.   
    for indices in indVir:                      #indVir is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            indVir1.append(i)                   #indVir1 now contains indVir in a usable format
    
    indVir = tree.query_radius(D2, r=R2*2)      #Do the same for the second cluster
    for indices in indVir:                 
         for i in indices:
             indVir2.append(i) 

    ind = tree.query_radius((D1+ np.array([[XYZsep/2,0,0]])), r=(np.sqrt((XYZsep/2)**2+ (XYZsep/2)**2+ zslice**2)))    #ind gathers the indicies of all haloes within a certain radius of the first cluster in the non-physical pair. 1.5* the R_2D of the origional physical pair.         

    for indices in ind:                                     #ind (index) is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            
            if np.abs(D1[0,2]-data.iloc[i,3])< zslice and i not in indVir1 and i not in indVir2:     #This filters the haloes so that only those within z values +- a certain value from the first cluster in the non-physical pair are allowed. The second statement filters out all haloes within 2*Virial radius of the first and second clusters in the non-physical pair
                ind1.append(i) 
    ind = tree.query_radius((D2- np.array([[XYZsep/2,0,0]])), r=(np.sqrt((XYZsep/2)**2+ (XYZsep/2)**2+ zslice**2)))    #repeat the steps above for the second cluster in the non-physical pair.
    for indices in ind:
        for i in indices:
            if np.abs(D2[0,2]-data.iloc[i,3])< zslice and i not in indVir1 and i not in indVir2:
                ind2.append(i)
        
def Nrotation(rotate):                           #A function for non-physical pairs to create arrays containing x and y coordinates of DM haloes and their mass densities. This is done for the two clusters separately. Cluster 2 is rotated by a random value between 0 and 2 pi, given by the variable 'rotate'. 
    global R
    global mc1
    R,mc1 = [],[]
    
    for i in ind1:                              
        y = data.iloc[i,2]-D1[0,1]
        z = data.iloc[i,3]-D1[0,2]
        r = np.sqrt(y**2+z**2)
        if r > binss[0]:
            
            for k in range(len(binss)):
                if r < binss[k]:
                    vol = (np.pi*XYZsep*(binss[k]**2)-(np.pi*XYZsep*(binss[k-1]**2)))
                    mc1.append(data.iloc[i,0]/vol)
                    R.append(r)
                    break
    
    
    global rot
    for i in ind2:                              #DM halo masses and co-ords for cluster 2. x and y co-ords are randomly rotated and then put at a distance of 1 * Xsep to the right of cluster 1.
                     
        Rz = np.array([[np.cos(rotate),-1*np.sin(rotate),0],[np.sin(rotate),np.cos(rotate),0],[0,0,1]])     #Matrix to rotate a set of coordinates around the z-axis.
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])                                      #Collect the x,y,z coordinates of a DM halo around cluster 2.
        rot = rot - np.array([[data.iloc[cluster2,1],data.iloc[cluster2,2],data.iloc[cluster2,3]]])         #Translate the x,y,z coordinates to the origin so that the rotation is about the origin
        rot = rot @ Rz                                                                                      #Matrix multiplicaiton of the x,y,z coordinates and the rotation matrix. This rotates the x,y,z co-ords about the z axis by a random value given by the variable 'rotate'.
        rot = rot + np.array([data.iloc[cluster1,1]+XYZsep,data.iloc[cluster1,2],data.iloc[cluster1,3]])     #Translate the new x,y,z coordinates that are centred at the same y level and 1 * Xsep to the right of cluster 1.
        rot=rot.transpose()                                                                                 #Transpose the matrix as we need to to swap columns and rows after the matrix multiplication.

        y = (rot[1])-D1[0,1]    
        z = (rot[2])-D1[0,2]    
        r = np.sqrt(y**2+z**2)
        if r > binss[0]:
            
            for k in range(len(binss)):
                if r < binss[k]:
                    vol = (np.pi*XYZsep*(binss[k]**2)-(np.pi*XYZsep*(binss[k-1]**2)))
                    mc1.append(data.iloc[i,0]/vol)
                    R.append(r)
                    break
        
def Nplot():                                                                                    #get non-physical pairs data for plot          
      
    global Filament     #making filament and pcombined global for testing purposes
    global Stack
    global p
    global v
    p,v = [],[]
 
    #plt.figure()   
    #j,_,_ = plt.hist(R, bins = binss,weights=mc1)
    #print(len(R),len(mc1))
    p,v = np.histogram(R, bins = binss,weights=mc1)
    #plt.hist(R, bins = 50,range = [0,20],weights=mc1)           #physical pair histogram data for mass density of DM haloes around cluster 1
    #plt.hist(R, bins = binss ,weights=mc1)   
    Stack += p
                                
#end of functions


data = pd.read_csv('100box.csv')

n=len(data.iloc[:,0])-1                         #number of data values 

Npairs = np.array(pd.read_csv('Npairs1.csv',header=None))                                               
#Npairs = np.array([2714,2798])                                               #big haloes in the are 2714,2798, 4035,4156,6608,11670

XYZ = data.iloc[:,1:4]
bins = 100                     

#binss = np.arange(0.05,20,0.1) 
binss = np.logspace(-1.3,1.5,100)  #-0.33 works well but 10^-1.3 and 10^1.5 is between 0.05 amd 30
Stack = np.zeros(len(binss)-1)                                                                                 

#create an array to contain the stacking of non-physical pairs
i=0 
select = 200  #max 4608
rand =random.sample(range(0, int(len(Npairs)/2)), int(select/2)) 
                                                               #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
for i in rand:  
    i = i*2
    ran = random.randint(0,1)
    if ran == 0:
        cluster1,cluster2 = int(Npairs[i]), int(Npairs[i+1])  
    else: 
        cluster2,cluster1 = int(Npairs[i]), int(Npairs[i+1]) 
                                        #take the first non-physical pair from the pair catalogue
    xc1,yc1,mc1,xc2,yc2,mc2,D1,D2,R1,R2,XYZsep,zslice,cluster1,cluster2,theta,lims = NValues()
    Nenvironment(cluster1,cluster2)                                                      
    Nrotation(random.randint(0, 628)/100)                                                                     #Rotation function - random number between 0 and 2pi (approximately 6.28)
    Nplot()                                                                 
    #print(len(R),len(mc1),R,mc1)
midss = []
for i in range(len(binss) - 1):
    m =(((binss[i] + binss[i + 1])/2 ))
    midss.append(m)  

plt.figure()                                                               
plt.plot(midss,Stack/((select)))
plt.xscale('log')
plt.xlim(0.1,20)
end = time.time()
print(end-start) 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots for testing


#thoughts: divide density by 2 cus two sets of co-ords?
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
