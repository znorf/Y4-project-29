import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.neighbors import KDTree
from matplotlib.colors import LogNorm
import math as math

#functions
def Nenvironment(cluster1,cluster2):             #A function to find the indexes of DM haloes around each of the two clusters        
    global ind1
    global ind2
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
    
    ind = tree.query_radius(D1, r=(np.sqrt((XYsep*1.5)**2+ XYsep**2+ zslice**2)))    #ind gathers the indicies of all haloes within a certain radius of the first cluster in the non-physical pair. 1.5* the R_2D of the origional physical pair.         
    for indices in ind:                                     #ind (index) is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            if np.abs(D1[0,2]-data.iloc[i,3])< zslice and i not in indVir1 and i not in indVir2:     #This filters the haloes so that only those within z values +- a certain value from the first cluster in the non-physical pair are allowed. The second statement filters out all haloes within 2*Virial radius of the first and second clusters in the non-physical pair
                ind1.append(i)
     
    ind = tree.query_radius(D2, r=(np.sqrt((XYsep*1.5)**2+ XYsep**2+ zslice**2)))    #repeat the steps above for the second cluster in the non-physical pair.            
    for indices in ind:
        for i in indices:
            if np.abs(D2[0,2]-data.iloc[i,3])< zslice and i not in indVir1 and i not in indVir2:
                ind2.append(i)
def Penvironment(cluster1,cluster2):             #A function to find the indexes of DM haloes around each of the two clusters        
    global ind1
    ind1,indVir1,indVir2 = [],[],[]

    tree = KDTree(XYZ, leaf_size=2)
   
    indVir = tree.query_radius(D1, r=R1*2)      #indVir gathers the indicies of all haloes within 2*Virial radius of the first cluster in the non-physical pair. 2*Virial radius is chosen to isolate filaments from clusters.   
    for indices in indVir:                      #indVir is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            indVir1.append(i)                   #indVir1 now contains indVir in a usable format
    
    indVir = tree.query_radius(D2, r=R2*2)      #Do the same for the second cluster
    for indices in indVir:                 
         for i in indices:
             indVir2.append(i) 
  
    ind = tree.query_radius(D1, r=(np.sqrt((XYsep*1.5)**2+ XYsep**2+ (zslice+Zsep)**2)))    #ind gathers the indicies of all haloes within a certain radius of the first cluster in the non-physical pair. 1.5* the R_2D of the origional physical pair.         
    
    ind = tree.query_radius(D2, r=(np.sqrt((XYsep*1.5)**2+ XYsep**2+ (zslice+Zsep)**2)))    #repeat the steps above for the second cluster in the non-physical pair.            
    for indices in ind:
        for i in indices:
            if (np.abs(D1[0,2]-data.iloc[i,3])< zslice or np.abs(D2[0,2]-data.iloc[i,3])< zslice)  or (np.abs(D2[0,2]-data.iloc[i,3])< Zsep and np.abs(D1[0,2]-data.iloc[i,3]< Zsep)) and i not in indVir1 and i not in indVir2:    
                ind1.append(i)          
            #This if statement asks if the DM Halo is within a distance, zslice, of the first or second cluster. There is a change for the halo to be between the two clusters if zslice is less than the Zsep of the two clusters. In this case, the second statement asks if the DM halo is in between the two clusters. We also want to remove DM haloes within two virial radius of each cluster. The final statement does this.
    
                
def Nrotation(rotate):                           #A function for non-physical pairs to create arrays containing x and y coordinates of DM haloes and their mass densities. This is done for the two clusters separately. Cluster 2 is rotated by a random value between 0 and 2 pi, given by the variable 'rotate'. 
    for i in ind1:                              
        mc1.append(data.iloc[i,0]/vol)          #Add the mass density of a DM halo around Cluster 1  
        xc1.append(data.iloc[i,1])              #Add the x co-ords of a DM halo around Cluster 1
        yc1.append(data.iloc[i,2])              #Add ther y co-ords of a DM halo around Cluster 1
        
    for i in ind2:                              #DM halo masses and co-ords for cluster 2. x and y co-ords are randomly rotated and then put at a distance of 1 * Xsep to the right of cluster 1.
                     
        Rz = np.array([[np.cos(rotate),-1*np.sin(rotate),0],[np.sin(rotate),np.cos(rotate),0],[0,0,1]])     #Matrix to rotate a set of coordinates around the z-axis.
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])                                      #Collect the x,y,z coordinates of a DM halo around cluster 2.
        rot = rot - np.array([[data.iloc[cluster2,1],data.iloc[cluster2,2],data.iloc[cluster2,3]]])         #Translate the x,y,z coordinates to the origin so that the rotation is about the origin
        rot = rot @ Rz                                                                                      #Matrix multiplicaiton of the x,y,z coordinates and the rotation matrix. This rotates the x,y,z co-ords about the z axis by a random value given by the variable 'rotate'.
        rot = rot + np.array([data.iloc[cluster1,1]+XYsep,data.iloc[cluster1,2],data.iloc[cluster1,3]])     #Translate the new x,y,z coordinates that are centred at the same y level and 1 * Xsep to the right of cluster 1.
        rot=rot.transpose()                                                                                 #Transpose the matrix as we need to to swap columns and rows after the matrix multiplication.
        xc2.extend(rot[0])                                                                                  #Add the x co-ords of a DM halo around Cluster 2
        yc2.extend(rot[1])                                                                                  #Add the y co-ords of a DM halo around Cluster 2
        mc2.append(data.iloc[i,0]/vol)                                                                      #Add the mass density of a DM halo around Cluster 2

def Protation(rotate):                           #A function for physical pairs to create arrays containing x and y coordinates of DM haloes and their mass densities. This is done for the two clusters separately. Cluster 2 is rotated by a random value between 0 and 2 pi, given by the variable 'rotate'. 
    Rz = np.array([[np.cos(rotate),-1*np.sin(rotate),0],[np.sin(rotate),np.cos(rotate),0],[0,0,1]])
    for i in ind1:
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])
        rot = rot @ Rz      
        mc1.append(data.iloc[i,0])
        xc1.append(rot[0])  
        yc1.append(rot[1])    
                 
def NValues():                                                                          #All of the non-physical cluster data for calculations 
    xc1,yc1,mc1,xc2,yc2,mc2,D1,D2 = [],[],[],[],[],[],[],[]                             #reset all the arrays after every while loop      
    R1,R2,theta = 0,0,0
    XYsep = 10 
     
    cluster1,cluster2 = Npairs[i], Npairs[i+1]                                          #take the first non-physical pair from the pair catalogue
    D1 = data.iloc[cluster1,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 1
    D2 = data.iloc[cluster2,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 2
    R1 = data.iloc[cluster1,4]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc
    R2 = data.iloc[cluster2,4]/1000                                                     #Virial radius of cluster 2                                                                                 #This is the R_2D separation between the origional clusters in the physical pair. For testing purposes, this is set to 10 h^-1 Mpc
    zslice = np.abs(D1[0,2]-D2[0,2])/2                                                          #set the +- slice thickness. For testing purposes this is set so that all data will be in the zslice.       
    length = ((D1[0,0]+1.5*XYsep)-(D1[0,0]-0.5*XYsep))/bins                             #length of each box in the histogram
    height = ((D1[0,1]+XYsep)- (D1[0,1]-XYsep))/bins                                    #height of each box in the histogram
    vol = length * height * zslice 
    ClustersX = np.array([D1[0,0],D1[0,0]+XYsep])                                       #x co-ords of cluster 1 and 2 after translation
    ClustersY = np.array([D1[0,1],D1[0,1]])                                             #y co-ords of cluster 1 and 2 after translation
    lims = [[D1[0,0]-0.5*XYsep, D1[0,0]+1.5*XYsep], [D1[0,1]-XYsep, D1[0,1]+XYsep]]     #x and y limits of plot
    
    return xc1,yc1,mc1,xc2,yc2,mc2,D1,D2,R1,R2,XYsep,zslice,vol,ClustersX,ClustersY,cluster1,cluster2,theta,lims 

def PValues():                                                                          #All of the physical cluster data for calculations 
    xc1,yc1,mc1,D1,D2 = [],[],[],[],[]                            #reset all the arrays       
    R1,R2,theta,Zsep = 0,0,0,0
     
    cluster1,cluster2 = Ppairs[0], Ppairs[1]                                            #take the first non-physical pair from the pair catalogue
    D1 = data.iloc[cluster1,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 1
    D2 = data.iloc[cluster2,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 2
    R1 = data.iloc[cluster1,4]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc
    R2 = data.iloc[cluster2,4]/1000 
    XYsep = np.abs(D1[0,0]-D2[0,0])   
    Zsep = np.abs(D1[0,2]-D2[0,2])                                               #Virial radius of cluster 2                                                                        #This is the R_2D separation between the origional clusters in the physical pair. For testing purposes, this is set to 10 h^-1 Mpc
    zslice = 10                                                         #set the +- slice thickness. For testing purposes this is set so that all data will be in the zslice.
    length = ((D1[0,0]+1.5*XYsep)-(D1[0,0]-0.5*XYsep))/bins                             #length of each box in the histogram
    height = ((D1[0,1]+XYsep)- (D1[0,1]-XYsep))/bins                                    #height of each box in the histogram
    vol = length * height * zslice                                                      #volume of each box in the histogram

    theta = math.atan2((D2[0,1]-D1[0,1]),(D2[0,0]-D1[0,0]))                                         #angle between the two physical pairs
    Rz = np.array([[np.cos(theta),-1*np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])     #matrix to rotate about the z-axis
    D1 = D1 @ Rz                                                                                    #calculate new co-ords for the first cluster after rotation
    D2 = D2 @ Rz                                                                                    #calculate new co-ords for the second cluster after rotation
    ClustersX = np.array([D1[0,0],D2[0,0]])                                                         #Cluster 1 and 2 x co-ords
    ClustersY = np.array([D1[0,1],D2[0,1]])                                                         #Cluster 1 and 2 y co-ords
    
    if D1[0,0]<D2[0,0]:                             #These if statements make sure that the x and y lims of the plot stay consistant even if the two clusters are in opposite order.
        if D1[0,1]<D2[0,2]:
            lims = [[D1[0,0]-0.5*XYsep, D2[0,0]+0.5*XYsep], [D1[0,1]-XYsep, D2[0,1]+XYsep]]
        else:
            lims = [[D1[0,0]-0.5*XYsep, D2[0,0]+0.5*XYsep], [D2[0,1]-XYsep,D1[0,1]+XYsep]]

    if D1[0,0]>D2[0,0]:                    
        if D1[0,1]<D2[0,2]:
            lims = [[D2[0,0]-0.5*XYsep,D1[0,0]+0.5*XYsep], [D1[0,1]-XYsep, D2[0,1]+XYsep]]
        else: 
            lims = [[D2[0,0]-0.5*XYsep,D1[0,0]+0.5*XYsep], [D2[0,1]-XYsep,D1[0,1]+XYsep]]  

    return xc1,yc1,mc1,xc2,yc2,mc2,D1,D2,R1,R2,XYsep,zslice,vol,ClustersX,ClustersY,cluster1,cluster2,theta,lims,Zsep  

def Nplot():                                                                                    #get non-physical pairs data for plot          
    global Stack  
    n1, _, _ = np.histogram2d(xc1, yc1, bins=(bins, bins), range = lims, weights=mc1)           #non-physical pairhistogram data for mass density of DM haloes around cluster 1
    n2, _, _ = np.histogram2d(xc2, yc2, bins=(bins, bins), range = lims, weights=mc2)           #non-physical pairhistogram data for mass density of DM haloes around cluster 2    
    combined = n1+n2                                                                            #non-physical pairhistogram data for combined mass density of DM haloes around cluster 1 and cluster 2
    Stack += combined                                                                           #Stack the mass density of the non-physical pairs   
                                                                                     
def Pplot():                                                                                    #plotting sum of physical and non-physical pairs    
    global Filament     #making filament and pcombined global for testing purposes
    global p
    p, _, _ = np.histogram2d(xc1, yc1, bins=(bins, bins), range = lims, weights=mc1)           #physical pair histogram data for mass density of DM haloes around cluster 1
    
        
    Filament = p - Stack*0.25  #check 0.25                                              #histogram data for combined mass density of DM haloes around cluster 1 and cluster 2
    Filament = np.rot90(Filament)                                                               #The data has to be rotated by 90 degrees for plt.imshow()        
    plt.figure()
    plt.imshow(Filament)                                                         #Plot the mass density histogram
    plt.colorbar()
    plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
    plt.axis('scaled')                                                                                               
       
#end of functions


data = pd.read_csv('stack100^3rvir.csv')        #Mvir,x,y,z, rvir from a 100*100*100 h^-3 Mpc^3 sample with masses above 10^11 h^-1 solar masses

'''
Pair_id="1234:5678"
x=Pair_id.find(':')
H0=int(Pair_id[:x])
H1=int(Pair_id[x+1:])

print(Pair_id,H0,H1)
'''

n=len(data.iloc[:,0])-1                         #number of data values 
    
Ppairs = np.array([4035,4156])                  #Array containing the physical pairs
Npairs = np.array([2714,2798,2900,3100])                  #Array containing the non-physical pairs                                                
                                                #big haloes in the are 2714,2798, 4035,4156,6608,11670

XYZ = data.iloc[:,1:4]
bins = 100                                                                                                  #set the number of bins in the histogram
Stack = np.zeros((bins,bins))                                                                               #create an array to contain the stacking of non-physical pairs
i=0 
                                                                                     #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
while i <len(Npairs):  
    xc1,yc1,mc1,xc2,yc2,mc2,D1,D2,R1,R2,XYsep,zslice,vol,ClustersX,ClustersY,cluster1,cluster2,theta,lims = NValues()
    Nenvironment(cluster1,cluster2)  
    #NonPhysrotation(random.randint(0, 628)/100)                                                       #Rotation function - random number between 0 and 2pi (approximately 6.28).
    Nrotation(0)                                                                                       #Rotation of 0 degrees for testing purposes
    Nplot()                                                                  
    i+=2    
  
xc1,yc1,mc1,xc2,yc2,mc2,D1,D2,R1,R2,XYsep,zslice,vol,ClustersX,ClustersY,cluster1,cluster2,theta,lims,Zsep = PValues()
Penvironment(cluster1,cluster2)                                                     
Protation(theta) 
Pplot()
print('thickness = Zsep:', Zsep,'+ zslice:', zslice, '=', Zsep+zslice)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots for testing



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
