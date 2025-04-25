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
def PValues(D1,D2):                                                                          #All of the physical cluster data for calculations 
    xc1,yc1,mc1 = [],[],[]                           #reset all the arrays       
    theta_z,theta_y,Zsep,XYZsep = 0,0,0,0
    
    D1origin = D1
    D2origin = D2 
    #print('heyyyy',D1,D2)
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

        

    

    return xc1,yc1,mc1,zslice,vol,ClustersX,ClustersY,theta_z,theta_y,lims,Zsep,XYZsep,D1origin,D2origin,multiplier,D1,D2  


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

end = time.time()
print('pairs',end-start)
#Ppairs = np.array([4035,4156,2714,2798,2900,3100])                  #Array containing the physical pairs
                                             
                                                #big haloes in the are 2714,2798, 4035,4156,6608,11670


bins = 100                                                                                                  #set the number of bins in the histogram
Stack = np.zeros((bins,bins))                                                                               #create an array to contain the stacking of non-physical pairs
i=0 
select = 100  #max 4608
rand = [random.randint(0, (len(Ppairs1))-1) for _ in range(select)]  
rand = np.arange(0,select-1,1)   
#rand = np.array([6])

table = pa.read_table('P_Chunks.parquet') 
df_Chunk = table.to_pandas()
end = time.time()
#print('chunks',end-start)






D1,D2,R1,R2 = [],[],[],[]
data = pd.DataFrame()
flick = 0                                                                                    #A while loop to create density arrays for all non-physical paris in the non-physical pair catalogue 'pairs'.         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Funciton calling section    
select = 2
for i in rand:  
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
        flick +=1
        D1 = df1.iloc[int(Ppairs1.iloc[i,0]),3:6].values.reshape(1, -1)                                  #Co-ords of cluster 1
        R1 = df1.iloc[int(Ppairs1.iloc[i,0]),2]/1000                                                     #Virial radius of cluster 1. /1000 to convert from h^-1 Kpc to h^-1 Mpc
         
        if Ppairs11.iloc[i,0]== Ppairs22.iloc[i,0]:
            D2 = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1) 
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000                                  #Co-ords of cluster 2
        else:
            table = pa.read_table('Chunk_'+str(Ppairs22.iloc[i,0])+'.parquet')
            df1 = table.to_pandas()
            D2 = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1) 
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 
    else: 
        flick +=1
        D2 = df1.iloc[int(Ppairs1.iloc[i,0]),3:6].values.reshape(1, -1)                                  #Co-ords of cluster 1
        R1 = df1.iloc[int(Ppairs1.iloc[i,0]),2]/1000
        if Ppairs11.iloc[i,0]== Ppairs22.iloc[i,0]:
            D1 = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1)                                  #Co-ords of cluster 2
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 
        else:
            print('different!')
            table = pa.read_table('Chunk_'+str(Ppairs22.iloc[i,0])+'.parquet')
            df1 = table.to_pandas()
            D1 = df1.iloc[int(Ppairs2.iloc[i,0]),3:6].values.reshape(1, -1)    
            R2 = df1.iloc[int(Ppairs2.iloc[i,0]),2]/1000 
    #end = time.time()
    #print('chunks4',end-start)
    XYZsep = np.sqrt((D1[0,0]-D2[0,0])**2+ (D1[0,1]-D2[0,1])**2+ (D1[0,2]-D2[0,2])**2)
    
    if XYZsep < 20:         #for now ignoring plots where cluster 1 and cluster 2 are on the opposite sides of the box due but are pairs due to periodicity.
        xc1,yc1,mc1,zslice,vol,ClustersX,ClustersY,theta_z,theta_y,lims,Zsep,XYZsep,D1origin,D2origin, multiplier,D1,D2 = PValues(D1,D2)    
        #end = time.time()
        #print('chunks5',end-start)
        
        Penvironment() 
        #end = time.time()
        #print('chunks6',end-start)                                                       #Rotation function - random number between 0 and 2pi (approximately 6.28).
        Protation(theta_z,theta_y)  
        end = time.time()
        #print('chunks7',end-start)                                                                                      
        Pplot() 
        #end = time.time()
        #print('chunks8',end-start)
    
        #print(XYZsep,chunks)
    else:
        break
       
    

Filament = np.rot90(Stack/select)                                                               #The data has to be rotated by 90 degrees for plt.imshow()        
plt.figure()
plt.imshow(Filament,interpolation='nearest',norm=LogNorm())                                                         #Plot the mass density histogram
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
plt.axis('scaled') 
end = time.time()
print(end-start)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#Plots for testing




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#