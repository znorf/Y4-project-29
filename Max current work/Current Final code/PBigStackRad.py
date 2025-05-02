# -*- coding: utf-8 -*-
"""
Created on Fri May  2 11:25:16 2025

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
   
    
    end = time.time()
    print('start',end-start)
    table = pa.read_table('Physical_Pair_Chunk_i_0.parquet') 
    Ppairs1 = table.to_pandas() 
    table = pa.read_table('Physical_Pair_Chunk_i_1.parquet') 
    Ppairs2 = table.to_pandas() 
    table = pa.read_table('Physical_Pair_chunk_0.parquet') 
    Ppairs11 = table.to_pandas() 
    table = pa.read_table('Physical_Pair_chunk_1.parquet') 
    Ppairs22 = table.to_pandas() 
    table = pa.read_table('P_Chunks.parquet') 
    df_Chunk = table.to_pandas()

    end = time.time()
    print('pairs',end-start)
    bins = 100                                                                                                  #set the number of bins in the histogram
    Stack = np.zeros((bins,bins))                                                                               #create an array to contain the stacking of non-physical pairs
    binss = np.arange(0.05,20,0.1)                                                                                                  #set the number of bins in the histogram
    StackRad = np.zeros(len(binss)-1) 
    
    #rand = [random.randint(0, (len(Ppairs1))-1) for _ in range(select)]  
    #rand = np.arange(0,select-1,1)   
    rand = np.loadtxt("Nran.csv", delimiter=",",dtype=int)     
    #rand = np.array([59])
    select = len(rand)
    return Ppairs1,Ppairs2,Ppairs11,Ppairs22,df_Chunk,rand,Stack,bins,select,StackRad,binss

def Dataset():
    D1origin,D2origin,R1,R2 = [],[],[],[]
    data = pd.DataFrame()
    
    chunks = df_Chunk.iloc[i,1]         #cleaning data eg: from ['3_1_0','2_2_3'] to 3_1_0 and 2_2_3
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

        #print(char,c_numb)
        if item == '4':
            move[c_numb] = 1000 
            #print('4!',chunks,c_numb)

            
            #print(c_numb,char)
        if item == '5':
            #print('-1!',chunks,c_numb)
            move[c_numb] = -1000 

      
        if c_numb == 3:
            c_numb = 0
            move1 = np.vstack((move1,move))
            #print('hi',move1,'heyy',move)
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

    
    table = pa.read_table('Chunk_'+str(Ppairs11.iloc[i,0])+'.parquet')  #get the chunk that the first cluster is in
    df1 = table.to_pandas()      
    ran = random.randint(0,1)       #randomly choose cluster 1    
    #ran = 0
    
    if ran == 0:                        
    
        D1origin = df1.iloc[int(Ppairs1.iloc[i,0]),3:6].values.reshape(1, -1)                                  #Co-ords of cluster 1
        R1 = df1.iloc[int(Ppairs1.iloc[i,0]),2]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc
         
        if Ppairs11.iloc[i,0]== Ppairs22.iloc[i,0]:                                 #if the two clusters are in the same chunk, use that chunk to find the co-ords and virial radius of cluster 2
            D2origin = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1) 
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000                                  
        else:
            table = pa.read_table('Chunk_'+str(Ppairs22.iloc[i,0])+'.parquet')      #if not in the same chunk, load the new chunk and use that chunk to find the co-ords and virial radius of cluster 2
            df1 = table.to_pandas()
            D2origin = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1) 
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 
    else:                                                                           #the same as above but if ran == 1 (50/50 chance)
        
        D2origin = df1.iloc[int(Ppairs1.iloc[i,0]),3:6].values.reshape(1, -1)                                  
        R1 = df1.iloc[int(Ppairs1.iloc[i,0]),2]/1000
        if Ppairs11.iloc[i,0]== Ppairs22.iloc[i,0]:
            D1origin = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1)                                  
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 
        else:
            print('different!')
            table = pa.read_table('Chunk_'+str(Ppairs22.iloc[i,0])+'.parquet')
            df1 = table.to_pandas()
            D1origin = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1)    
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 

    XYZsep = np.sqrt((D1origin[0,0]-D2origin[0,0])**2+ (D1origin[0,1]-D2origin[0,1])**2+ (D1origin[0,2]-D2origin[0,2])**2)  #R_3D distance between clusters
    return D1origin,D2origin,R1,R2,XYZsep,data

def PValues(D1origin,D2origin):                                                                          #All of the physical cluster data for calculations 
           
    theta_z,theta_y,= 0,0
                                               #Virial radius of cluster 2                                                                        #This is the R_2D separation between the origional clusters in the physical pair. For testing purposes, this is set to 10 h^-1 Mpc
    zslice = 2                                                         #set the +- slice thickness. For testing purposes this is set so that all data will be in the zslice.
    length = ((D1origin[0,0]+1.5*XYZsep)-(D1origin[0,0]-0.5*XYZsep))/bins                             #length of each box in the histogram
    height = ((D1origin[0,1]+XYZsep)- (D1origin[0,1]-XYZsep))/bins                                    #height of each box in the histogram
    volStack = length * height * zslice                                                      #volume of each box in the histogram
    multiplier = 20/XYZsep
    #multiplier = 1
    
    theta_z = math.atan2((D2origin[0,1]-D1origin[0,1]),(D2origin[0,0]-D1origin[0,0]))

 
    Rz = np.array([[np.cos(theta_z),-1*np.sin(theta_z),0],[np.sin(theta_z),np.cos(theta_z),0],[0,0,1]])     #matrix to rotate about the z-axis
      
 
    D1 = D1origin @ Rz 
    D2 = D2origin @ Rz

    theta_y = math.atan2((D2[0,2]-D1[0,2]),(D2[0,0]-D1[0,0])) 
    theta_y = theta_y *-1
    Ry = np.array([[np.cos(theta_y),0,np.sin(theta_y)],[0,1,0],[-1*np.sin(theta_y),0,np.cos(theta_y)]])     #matrix to rotate about the y-axis  

    D1 = D1 @ Ry                            #The new rotated cluster co-ordinates
    D2 = D2 @ Ry   


    lims = [[(D1[0,0]*multiplier-10), D1[0,0]*multiplier+30], [D1[0,1]*multiplier-20, D1[0,1]*multiplier+20]]       #plot x1,x2 and y1,y2 limits

    return zslice,volStack,theta_z,theta_y,lims,XYZsep,multiplier,D1,D2  


def Penvironment():             #A function to find the indexes of DM haloes around each of the two clusters        
    global ind1
    ind1,indVir1,indVir2,indVir = [],[],[],[]

    tree = KDTree(data.iloc[:,1:4], leaf_size=10000000)     #make a KD tree
   
    indVir = tree.query_radius(D1origin, r=R1*2)      #indVir gathers the indicies of all haloes within 2*Virial radius of the first cluster in the non-physical pair. 2*Virial radius is chosen to isolate filaments from clusters.   
    for indices in indVir:                      #indVir is in a wierd format, this for loop turns a long list of numbers into a list where each new number is a new column.
        for i in indices:
            indVir1.append(i)                   #indVir1 now contains indVir in a usable format
    
    indVir = tree.query_radius(D2origin, r=R2*2)      #Do the same for the second cluster
    for indices in indVir:                 
         for i in indices:
             indVir2.append(i) 
    indVir = np.concatenate((indVir1,indVir2))
    ind = tree.query_radius((D1origin+D2origin)/2, r=(np.sqrt((XYZsep)**2+ XYZsep**2+ (zslice)**2)))    #repeat the steps above for the midpoint between the two clusters               
    for indices in ind:
        for i in indices:
            if i not in indVir:   #This statement removes DM haloes within two virial radius of each cluster.  
                ind1.append(i)          
        
               
def Protation(theta_z,theta_y):                           #A function for physical pairs to create arrays containing x and y coordinates of DM haloes and their mass densities. This is done for the two clusters separately. Cluster 2 is rotated by a random value between 0 and 2 pi, given by the variable 'rotate'. 
    global rot
    xc1,yc1,mc1 = [],[],[]                           #reset all the arrays
    mcT,R = [],[]
    Rz = np.array([[np.cos(theta_z),-1*np.sin(theta_z),0],[np.sin(theta_z),np.cos(theta_z),0],[0,0,1]])
    Ry = np.array([[np.cos(theta_y),0,np.sin(theta_y)],[0,1,0],[-1*np.sin(theta_y),0,np.cos(theta_y)]])
    for i in ind1:
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])

        rot = rot @ Rz      

        rot = rot @ Ry 

        if np.abs(D1[0,2]-rot[2])< zslice:              #makes sure all data points are within the zslice. Any DM halo with z value now within the zslice is removed
            mc1.append(data.iloc[i,0]/volStack)
            xc1.append(rot[0]*multiplier)  
            yc1.append(rot[1]*multiplier)
            
            x = (rot[0]*multiplier)-D1[0,0]*multiplier
            y = (rot[1]*multiplier)-D1[0,1]*multiplier    
            z = (rot[2]*multiplier)-D1[0,2] *multiplier   
            r = np.sqrt(y**2+z**2)
            if r > binss[0] and x < (20-(2*R2)*multiplier) and x > (0+(2*R1)*multiplier):
                #xp.append( (rot[0]*multiplier)-D1[0,0]*multiplier  )  
                #yp.append((rot[1]*multiplier)-D1[0,1]*multiplier )    
                for k in range(len(binss)):   
                    if r < binss[k]:
                        R.append(r)
                        vol = (np.pi*XYZsep*(binss[k]**2)-(np.pi*XYZsep*(binss[k-1]**2)))
                        mcT.append(data.iloc[i,0]/vol)
        
                        break
    
    
    
    
    return  xc1,yc1,mc1,R,mcT 

def Pplot():                                                                                    #plotting sum of physical and non-physical pairs    
    global Filament     #making filament and pcombined global for testing purposes
    global Stack
    global p
    global StackRad
    p, _, _ = np.histogram2d(xc1, yc1, bins=(bins, bins), range = lims, weights=mc1)           #physical pair histogram data for mass density of DM haloes around cluster 1
    Stack += p
    
    
    Ph,v = np.zeros(199),[]
    if len(mcT) > 1:
        Ph,v = np.histogram(R, bins = binss,weights=mcT)
    elif len(mcT) == 1:
        Ph,v = np.histogram(R, bins = binss,weights=mcT) 
    
    StackRad += Ph
    
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

def Final():
    #stacking
    PFilament = np.rot90(Stack/select)                                                               #The data has to be rotated by 90 degrees for plt.imshow()        
    plt.figure()
    plt.imshow(PFilament,interpolation='nearest',norm=LogNorm())                                                         #Plot the mass density histogram
    plt.colorbar()
    plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
    plt.axis('scaled') 
    plt.title('Physical Pair Stacked Mass density ')
    np.savetxt("PFilament.csv", PFilament, delimiter=",")
    
    #radius
    midss = []
    for i in range(len(binss) - 1):
        m =(((binss[i] + binss[i + 1])/2 ))
        midss.append(m)
        
    plt.figure()                                                               
    plt.plot(midss,StackRad/((select)))
    plt.xscale('log')
    plt.xlim(0.1,20)
    plt.title('Physical Pair Radius Mass Density')
    plt.savefig('Pradius.png')
    np.savetxt("Prad.csv", StackRad, delimiter=",")
    
    end = time.time()
    print(end-start)
    return PFilament
#end of functions
                                                                                #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
Ppairs1,Ppairs2,Ppairs11,Ppairs22,df_Chunk,rand,Stack,bins,select,StackRad,binss = load(10)
Nran = []
i=0
count = 0
for i in rand:  
    D1origin,D2origin,R1,R2,XYZsep,data = Dataset()

    if XYZsep < 20:         #for now ignoring plots where cluster 1 and cluster 2 are on the opposite sides of the box due but are pairs due to periodicity. 
        zslice,volStack,theta_z,theta_y,lims,XYZsep,multiplier,D1,D2 = PValues(D1origin,D2origin)    
        Penvironment()                                                       
        xc1,yc1,mc1,R,mcT = Protation(theta_z,theta_y)  #get the x,y and mass density data                                                                                     
        Pplot()                     #create histograms
        Nran.append(i)
    else:
        print('something is wrong',XYZsep)
        break      
    end = time.time()
    print(end-start)
    count +=1
    print('                                            ',(count*100)/len(rand))        #percentage of the way through the code is
PFilament = Final()                             #plot final histogram

#np.savetxt("Nran.csv", Nran, delimiter=",")
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots for testing




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

