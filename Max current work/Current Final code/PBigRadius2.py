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
def Load(select):
    table = pa.read_table('Physical_Pair_Chunk_i_0.parquet') 
    Ppairs1 = table.to_pandas() 
    table = pa.read_table('Physical_Pair_Chunk_i_1.parquet') 
    Ppairs2 = table.to_pandas() 
    table = pa.read_table('Physical_Pair_chunk_0.parquet') 
    Ppairs11 = table.to_pandas() 
    table = pa.read_table('Physical_Pair_chunk_1.parquet') 
    Ppairs22 = table.to_pandas() 

    end = time.time()
    print('pairs',end-start)
    #Ppairs = np.array([4035,4156,2714,2798,2900,3100])                  #Array containing the physical pairs
                                                 
    bins = 100 
    binss = np.arange(0.05,20,0.1)                                                                                                  #set the number of bins in the histogram
    Stack = np.zeros(len(binss)-1)                                                                              #create an array to contain the stacking of non-physical pairs
     
      #max 4608
    rand = [random.randint(0, (len(Ppairs1))-1) for _ in range(select)]  
    rand = np.arange(0,select-1,1)   
    #rand = np.array([6])

    table = pa.read_table('P_Chunks.parquet') 
    df_Chunk = table.to_pandas()
    
    return Ppairs1,Ppairs2,Ppairs11,Ppairs22,bins,binss,select,rand,df_Chunk,Stack

def Dataset():
    D1,D2,R1,R2 = [],[],[],[]
    
    
    #end = time.time()
    #print('chunks1',end-start)
    data = pd.DataFrame()
    chunks = df_Chunk.iloc[i,1]
    chunks = chunks.replace("[", "")
    chunks = chunks.replace("]", "")
    chunks = chunks.replace("'", "")
    chunks = chunks.replace(",", "")
    chunks = chunks.replace("-1", "3")  #might have to adjust this!
    chunks = chunks.replace("4", "1")  #might have to adjust this!
    chunks = chunks.split(" ")  
    #end = time.time()
    #print('chunks2',end-start)
    overlaps = np.arange(0,len(chunks))
    for j in overlaps:
        table = pa.read_table('Chunk_'+str(chunks[j])+'.parquet')
        df = table.to_pandas()
        df = df.drop('# ID', axis=1)
        col_to_move = df.pop(' RVIR')  # Remove & store column
        df[' RVIR'] = col_to_move      # Re-add at the end
        data = pd.concat([data, df], ignore_index=True, sort=False)
    #end = time.time()
    #print('chunks3',end-start)
    
    table = pa.read_table('Chunk_'+str(Ppairs11.iloc[i,0])+'.parquet')
    df1 = table.to_pandas()      
    ran = random.randint(0,1)
    if ran == 0:

        D1 = df1.iloc[int(Ppairs1.iloc[i,0]),3:6].values.reshape(1, -1)                                  #Co-ords of cluster 1
        R1 = df1.iloc[int(Ppairs1.iloc[i,0]),2]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc
         
        if Ppairs11.iloc[i,0]== Ppairs22.iloc[i,0]:
            D2 = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1) 
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000                                  #Co-ords of cluster 2
        else:
            print('different!1')
            table = pa.read_table('Chunk_'+str(Ppairs22.iloc[i,0])+'.parquet')
            df1 = table.to_pandas()
            D2 = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1) 
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 
    else: 

        D2 = df1.iloc[int(Ppairs1.iloc[i,0]),3:6].values.reshape(1, -1)                                  #Co-ords of cluster 1
        R1 = df1.iloc[int(Ppairs1.iloc[i,0]),2]/1000
        if Ppairs11.iloc[i,0]== Ppairs22.iloc[i,0]:
            D1 = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1)                                  #Co-ords of cluster 2
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 
        else:
            print('different!2')
            table = pa.read_table('Chunk_'+str(Ppairs22.iloc[i,0])+'.parquet')
            df1 = table.to_pandas()
            D1 = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1)    
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 
    XYZsep = np.sqrt((D1[0,0]-D2[0,0])**2+ (D1[0,1]-D2[0,1])**2+ (D1[0,2]-D2[0,2])**2)

    return D1,D2,R1,R2,XYZsep,data

def PValues(D1,D2):                                                                          #All of the physical cluster data for calculations 
    xc1,yc1,mc1 = [],[],[]                           #reset all the arrays       
    theta_z,theta_y,Zsep,XYZsep = 0,0,0,0
    
    D1origin = D1
    D2origin = D2

   
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
      
    #print(D1,D2)
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

        

    

    return xc1,yc1,mc1,D1,D2,zslice,vol,ClustersX,ClustersY,theta_z,theta_y,lims,Zsep,XYZsep,D1origin,D2origin,multiplier 


def Penvironment():             #A function to find the indexes of DM haloes around each of the two clusters        
    global ind1
    ind1,indVir1,indVir2 = [],[],[]
    XYZ = data.iloc[:,1:4]
    tree = KDTree(XYZ, leaf_size=1000000)
   
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
    global xp
    global yp
    R,xp,yp=[],[],[]# check!
      
    Rz = np.array([[np.cos(theta_z),-1*np.sin(theta_z),0],[np.sin(theta_z),np.cos(theta_z),0],[0,0,1]])
    Ry = np.array([[np.cos(theta_y),0,np.sin(theta_y)],[0,1,0],[-1*np.sin(theta_y),0,np.cos(theta_y)]])
    for i in ind1:
        rot = np.array([data.iloc[i,1],data.iloc[i,2],data.iloc[i,3]])
        rot = rot @ Rz      
        rot = rot @ Ry 
        if np.abs(D1[0,2]-rot[2])< zslice:              #makes sure all data points are within the zslice. Any DM halo with z value now within the zslice is removed
            #xp.append( (rot[0]*multiplier)-D1[0,0]*multiplier  )  
            #yp.append((rot[1]*multiplier)-D1[0,1]*multiplier )
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
                        mc1.append(data.iloc[i,0]/vol)

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
    #plt.figure()
    #plt.plot(xp,yp,'.')
                                                                                            
def Final():
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
#end of functions


end = time.time()
print('start',end-start)
                                                                         #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
Ppairs1,Ppairs2,Ppairs11,Ppairs22,bins,binss,select,rand,df_Chunk,Stack = Load(100)
i=0
for i in rand:    
    
    D1,D2,R1,R2,XYZsep,data = Dataset()
    if XYZsep < 20:         #for now ignoring plots where cluster 1 and cluster 2 are on the opposite sides of the box due but are pairs due to periodicity.
        
        xc1,yc1,mc1,D1,D2,zslice,vol,ClustersX,ClustersY,theta_z,theta_y,lims,Zsep,XYZsep,D1origin,D2origin, multiplier = PValues(D1,D2)
        Penvironment()                                                        #Rotation function - random number between 0 and 2pi (approximately 6.28).
        Protation(theta_z,theta_y)                                                                                        #Rotation of 0 degrees for testing purposes
        Pplot()   
        #print('end') 
        end = time.time()
        #print(end-start)  
    else: 
        break                                                             
  
Final()  

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots for testing

    

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
