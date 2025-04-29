# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 21:23:30 2025

@author: Max
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.neighbors import KDTree
from matplotlib.colors import LogNorm
import math as math
import time
import pyarrow.parquet as pa
start = time.time()

#functions
def load(select):
    table = pa.read_table('n_Physical_Pairs_n0.parquet')    #a:b
    n0 = table.to_pandas() 
    table = pa.read_table('n_Physical_Pairs_n1.parquet')    #a:b
    n1 = table.to_pandas() 
    #table = pa.read_table('n_Physical_Pairs_pid.parquet')   #ID
    #pid = table.to_pandas() 
    table = pa.read_table('n_Physical_Pairs_aid (1).parquet')   #ID
    pid = table.to_pandas()
    table = pa.read_table('n_p_chunk_1.parquet')            #ID
    n1Chunks = table.to_pandas() 
    table = pa.read_table('n_p_chunk_0.parquet') 
    n0Chunks = table.to_pandas() 
    
    dataH13 = pd.read_csv('Rockstar_13R.csv')
    
    bins = 100                                                                                                  #set the number of bins in the histogram
    Stack = np.zeros((bins,bins))                                                                               #create an array to contain the stacking of non-physical pairs
    
    rand = [random.randint(0, (len(pid))-1) for _ in range(select)] 
    rand = np.array([3995947])
    #rand = [random.randint(0, 400000) for _ in range(select)] 
    #rand = np.arange(0,select-1,1)   
    #rand = np.array([0,1,2,3,4,5,6,7,8,9,10])
    return n0,n1,pid,n0Chunks,n1Chunks,dataH13,rand,Stack,bins,select

def Dataset(Type):  #XYZsep needed!!!
    global chunks    
    D1,D2,R1,R2 = [],[],[],[]
    data = pd.DataFrame()
    print(i)
    chunks = []
    if Type == 0:
        chunks = n0Chunks.iloc[i,1]      #changes!!    #cleaning data eg: from ['3_1_0','2_2_3'] to 3_1_0 and 2_2_3
        P= str(n0.iloc[i,0])     #get the a:b H13 ID's 
    elif Type == 1:
        chunks = n1Chunks.iloc[i,1]
        P= str(n1.iloc[i,0])     #get the a:b H13 ID's
    else:
        print('error type !=1 or 0')
    cluster1,cluster2 = P.split(':')
    cluster1, cluster2 = int(cluster1),int(cluster2)
    
    chunks = chunks.replace("[", "")
    chunks = chunks.replace("]", "")
    chunks = chunks.replace("'", "")
    chunks = chunks.replace(",", "")

    chunks2 = chunks.replace(" ", "")     #cleaning data but only to check for outliers
    chunks2 = chunks2.replace("-1", "5") 
    chunks2 = chunks2.replace("_", "")

    move = np.zeros(5)
    move1 = np.zeros(5)
    c_numb = 1      #character number in the list

    for item in chunks2:            #this for loops goes through each chunk. If a chunk is an outlier (has a 4 or 5 in it) it notes down the co-ordinate translation needed.
                                    # eg: 4_4_0 needs the x and y co-ords of the 1
        if item == '4':
            move[c_numb] = 1000 

        if item == '5':
            move[c_numb] = -1000 
    
        if c_numb == 3:
            c_numb = 0
            move1 = np.vstack((move1,move))
        c_numb +=1

    chunks = chunks.replace("-1", "3")  #might have to adjust this!  #cleaning data
    chunks = chunks.replace("4", "0")  #might have to adjust this!
    chunks = chunks.split(" ")  

    overlaps = np.arange(0,len(chunks))     #how many chunks in the data eg ['3_1_0','2_2_3'] goes over 2 chunks
    for j in overlaps:
       
        table = pa.read_table('Chunk_'+str(chunks[j])+'.parquet')       #loading the chunks and changing the columns so that it fits with the code I have written.
        df = table.to_pandas()
        df = df.drop('# ID', axis=1)
        col_to_move = df.pop(' RVIR')  # Remove & store column
        df[' RVIR'] = col_to_move      # Re-add at the end
        df0 =df + move1[j+1]

        data = pd.concat([data, df0], ignore_index=True, sort=False)     #If there are multiple chunks, stick them together

    ran = random.randint(0,1)
    if ran == 0:                        

        D1 = dataH13.iloc[cluster1,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 1
        R1 = dataH13.iloc[cluster1,4]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc                             
        D2 = dataH13.iloc[cluster2,1:4].values.reshape(1, -1) 
        R2 = dataH13.iloc[cluster2,4]/1000                                 
        
    else:                                                                           #the same as above but if ran == 1 (50/50 chance)
        
        D1 = dataH13.iloc[cluster2,1:4].values.reshape(1, -1)                                  #Co-ords of cluster 1
        R1 = dataH13.iloc[cluster2,4]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc                             
        D2 = dataH13.iloc[cluster1,1:4].values.reshape(1, -1) 
        R2 = dataH13.iloc[cluster1,4]/1000

    Ppair= str(pid.iloc[i,0])   
    Ppair0,Ppair1 = Ppair.split(':')
    Pxyz0 = dataH13.iloc[int(Ppair0),1:4].values.reshape(1, -1)
    Pxyz1 = dataH13.iloc[int(Ppair1),1:4].values.reshape(1, -1)
    XYZsep = np.sqrt((Pxyz0[0,0]-Pxyz1[0,0])**2+ (Pxyz0[0,1]-Pxyz1[0,1])**2+ (Pxyz0[0,2]-Pxyz1[0,2])**2)  #R_3D distance between clusters
    print(chunks)
    return D1,D2,R1,R2,XYZsep,data,cluster1,cluster2

def NValues(D1,D2):                                                                         
                                                                                                                                #This is the R_2D separation between the origional clusters in the physical pair. For testing purposes, this is set to 10 h^-1 Mpc
    zslice = 2                                                         #set the +- slice thickness. For testing purposes this is set so that all data will be in the zslice.
    length = ((D1[0,0]+1.5*XYZsep)-(D1[0,0]-0.5*XYZsep))/bins                             #length of each box in the histogram
    height = ((D1[0,1]+XYZsep)- (D1[0,1]-XYZsep))/bins                                    #height of each box in the histogram
    vol = length * height * zslice                                                      #volume of each box in the histogram
    multiplier = 20/XYZsep
    lims = [[(D1[0,0]*multiplier-10), D1[0,0]*multiplier+30], [D1[0,1]*multiplier-20, D1[0,1]*multiplier+20]]       #plot x1,x2 and y1,y2 limits

    return zslice,vol,lims,multiplier  

def Nenvironment():             #A function to find the indexes of DM haloes around each of the two clusters        
    global ind1
    global ind2
    global indVir1
    global indVir2
    global mid

    mid = (D1+ np.array([[XYZsep/2,0,0]]))/2
    ind1,ind2,indVir1,indVir2 = [],[],[],[]

    tree = KDTree(data.iloc[:,1:4], leaf_size=10000000)
    indVir = tree.query_radius(D1, r=R1*2)      #indVir gathers the indicies of all haloes within 2*Virial radius of the first cluster in the non-physical pair. 2*Virial radius is chosen to isolate filaments from clusters.   
    for indices in indVir:                      #indVir is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            indVir1.append(i)                   #indVir1 now contains indVir in a usable format
    
    indVir = tree.query_radius(D2, r=R2*2)      #Do the same for the second cluster
    for indices in indVir:                 
         for i in indices:
             indVir2.append(i) 

    ind = tree.query_radius((D1+ np.array([[XYZsep/2,0,0]])), r=(np.sqrt((XYZsep)**2+ XYZsep**2+ (zslice)**2)))    #ind gathers the indicies of all haloes within a certain radius of the first cluster in the non-physical pair. 1.5* the R_2D of the origional physical pair.         

    for indices in ind:                                     #ind (index) is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            
            if np.abs(D1[0,2]-data.iloc[i,3])< zslice and i not in indVir1 and i not in indVir2:     #This filters the haloes so that only those within z values +- a certain value from the first cluster in the non-physical pair are allowed. The second statement filters out all haloes within 2*Virial radius of the first and second clusters in the non-physical pair
                ind1.append(i) 
    
    ind = tree.query_radius(D2, r=(np.sqrt((1.5*XYZsep)**2+ XYZsep**2+ zslice**2)))
    for indices in ind:
        for i in indices:
            if np.abs(D2[0,2]-data.iloc[i,3])< zslice and i not in indVir1 and i not in indVir2:
                ind2.append(i)
                 
def Nrotation(rotate):                           #A function for physical pairs to create arrays containing x and y coordinates of DM haloes and their mass densities. This is done for the two clusters separately. Cluster 2 is rotated by a random value between 0 and 2 pi, given by the variable 'rotate'. 
    xc1,xc2,yc1,yc2,mc1,mc2 = [],[],[],[],[],[]   
    global rot
    for i in ind1:                              
        mc1.append(data.iloc[i,0]/vol)          #Add the mass density of a DM halo around Cluster 1  
        xc1.append(data.iloc[i,1]*multiplier)              #Add the x co-ords of a DM halo around Cluster 1
        yc1.append(data.iloc[i,2]*multiplier)              #Add ther y co-ords of a DM halo around Cluster 1

    for i in ind2:                              #DM halo masses and co-ords for cluster 2. x and y co-ords are randomly rotated and then put at a distance of 1 * Xsep to the right of cluster 1.
                     
        Rz = np.array([[np.cos(rotate),-1*np.sin(rotate),0],[np.sin(rotate),np.cos(rotate),0],[0,0,1]])     #Matrix to rotate a set of coordinates around the z-axis.
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])                                      #Collect the x,y,z coordinates of a DM halo around cluster 2.
        rot = rot - D2         #Translate the x,y,z coordinates to the origin so that the rotation is about the origin
        rot = rot @ Rz                                                                                      #Matrix multiplicaiton of the x,y,z coordinates and the rotation matrix. This rotates the x,y,z co-ords about the z axis by a random value given by the variable 'rotate'.
        rot = rot + D1     #Translate the new x,y,z coordinates that are centred at the same y level and 1 * Xsep to the right of cluster 1.
        #rot=rot.transpose()                                                                                 #Transpose the matrix as we need to to swap columns and rows after the matrix multiplication.
        xc2.append(rot[0,0]*multiplier+20)                                                                                  #Add the x co-ords of a DM halo around Cluster 2
        yc2.append(rot[0,1]*multiplier)                                                                                  #Add the y co-ords of a DM halo around Cluster 2
        mc2.append(data.iloc[i,0]/vol) 
                                                              #Add the mass density of a DM halo around Cluster 2
        
    return xc1,xc2,yc1,yc2,mc1,mc2
        
def Nplot():                                                                                    #plotting sum of physical and non-physical pairs      
    global Stack  
    hist1, _, _ = np.histogram2d(xc1, yc1, bins=(bins, bins), range = lims,  weights=mc1)           #non-physical pairhistogram data for mass density of DM haloes around cluster 1
    hist2, _, _ = np.histogram2d(xc2, yc2, bins=(bins, bins), range = lims, weights=mc2)           #non-physical pairhistogram data for mass density of DM haloes around cluster 2    
    combined = hist1+hist2                                                                            #non-physical pairhistogram data for combined mass density of DM haloes around cluster 1 and cluster 2
    Stack += combined                                                                           #Stack the mass density of the non-physical pairs   
    '''
    plt.figure()
    plt.plot(xc1,yc1,'r.')
    plt.plot(xc2,yc2,'b.') 
    plt.xlim(D1[0,0]*multiplier-10, D1[0,0]*multiplier +30)  
    plt.ylim(D1[0,1]*multiplier-10, D1[0,1]*multiplier+10)                                                                           
    plt.plot(D1[0,0]*multiplier,D1[0,1]*multiplier,color = 'orange',marker='*',markersize=15)
    plt.plot(D1[0,0]*multiplier +20, D1[0,1]*multiplier,color = 'green',marker='*',markersize=15)
    '''
    
def Final():
    NFilament = np.rot90(Stack/select*2)                                                               #The data has to be rotated by 90 degrees for plt.imshow()        
    plt.figure()
    plt.imshow(NFilament,norm=LogNorm())                                                         #Plot the mass density histogram
    plt.colorbar()
    plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
    plt.axis('scaled')
    end = time.time()
    print(end-start) 
    return NFilament
#end of functions
                                                                                #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
end = time.time()
print(end-start) 
n0,n1,pid,n0Chunks,n1Chunks,dataH13,rand,Stack,bins,select = load(200)
end = time.time()
print(end-start)

Nran = []
i=0
for i in rand:  
    if n0.iloc[i,0] == 'no_pair':
        print('no pair')        
    else:
        D1,D2,R1,R2,XYZsep,data,cluster1,cluster2 = Dataset(0)
        if len(chunks) < 17 and XYZsep < 20:                                     #ignoring wierd chunk boundary plots and (currently) ignoring pairs that go over due to periodicity
            zslice,vol,lims,multiplier = NValues(D1,D2)        
            Nenvironment()                                                       
            xc1,xc2,yc1,yc2,mc1,mc2 = Nrotation(random.randint(0, 628)/100)  #get the x,y and mass density data                                                                                      
            Nplot()                     #create histograms 
            if n1.iloc[i,0] == 'no_pair':
                print('no pair')
            else:
                D1,D2,R1,R2,XYZsep,data,cluster1,cluster2 = Dataset(1)
                if len(chunks) < 17 and XYZsep < 20:
                    zslice,vol,lims,multiplier = NValues(D1,D2)        
                    Nenvironment()                                                       
                    xc1,xc2,yc1,yc2,mc1,mc2 = Nrotation(random.randint(0, 628)/100)  #get the x,y and mass density data                                                                                      
                    Nplot()
                    Nran.append(i)
        else:
            print('too big! or XYZ > 20')
            print(len(chunks),XYZsep)
NFilament = Final()                             #plot final histogram
#np.savetxt("Nran.csv", Nran, delimiter=",")
#np.savetxt("NFilament.csv", NFilament, delimiter=",")
end = time.time()
print(end-start) 

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots for testing




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

