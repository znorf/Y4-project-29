# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 22:43:19 2025

@author: Freddie
"""

import numpy as np
import threading

def create_p(start, end, split):
    start=int(start)
    end=int(end)
    split=int(split)
    
    globals()['p_pairs_id_S'+str(split)]=''
    globals()['p_pairs_m0_S'+str(split)]=''
    globals()['p_pairs_m1_S'+str(split)]=''
    
    globals()['p_pairs_x0_S'+str(split)]=''
    globals()['p_pairs_y0_S'+str(split)]=''
    globals()['p_pairs_z0_S'+str(split)]=''
    
    globals()['p_pairs_x1_S'+str(split)]=''
    globals()['p_pairs_y1_S'+str(split)]=''
    globals()['p_pairs_z1_S'+str(split)]=''
    
    globals()['p_pairs_ds_S'+str(split)]=''
    
    
    for i in range(start,end):
        locals()['p_pairs_id'+str(i)]=''
        locals()['p_pairs_m0'+str(i)]=''
        locals()['p_pairs_m1'+str(i)]=''
        
        locals()['p_pairs_x0'+str(i)]=''
        locals()['p_pairs_y0'+str(i)]=''
        locals()['p_pairs_z0'+str(i)]=''
        
        locals()['p_pairs_x1'+str(i)]=''
        locals()['p_pairs_y1'+str(i)]=''
        locals()['p_pairs_z1'+str(i)]=''
        
        locals()['p_pairs_ds'+str(i)]=''
        for j in range(i+1,n+1):
            #calcaulates seperation, ds
            dx=float(data[i,1])-float(data[j,1])
            dy=float(data[i,2])-float(data[j,2])
            dz=float(data[i,3])-float(data[j,3])
            ds=round(np.sqrt(dx**2+dy**2+dz**2),3)
            if ds<=20 and ds>=3: #criteria for physical pairs
                
                pair_id=str(i)+';'+str(j) #pair id is combination of positions in list
                #adds physical pair to list
                
                locals()['p_pairs_id'+str(i)]=locals()['p_pairs_id'+str(i)]+','+pair_id
                
                locals()['p_pairs_m0'+str(i)]=locals()['p_pairs_m0'+str(i)]+','+str(data[i,0])
                
                locals()['p_pairs_m1'+str(i)]=locals()['p_pairs_m1'+str(i)]+','+data[j,0]
                
                locals()['p_pairs_x0'+str(i)]=locals()['p_pairs_x0'+str(i)]+','+data[i,1]
                
                locals()['p_pairs_y0'+str(i)]=locals()['p_pairs_y0'+str(i)]+','+data[i,2]
                
                locals()['p_pairs_z0'+str(i)]=locals()['p_pairs_z0'+str(i)]+','+data[i,3]
                
                locals()['p_pairs_x1'+str(i)]=locals()['p_pairs_x1'+str(i)]+','+data[j,1]
                locals()['p_pairs_y1'+str(i)]=locals()['p_pairs_y1'+str(i)]+','+data[j,2]
                locals()['p_pairs_z1'+str(i)]=locals()['p_pairs_z1'+str(i)]+','+data[j,3]
                locals()['p_pairs_ds'+str(i)]=locals()['p_pairs_ds'+str(i)]+','+str(ds)
        print(i)
    for i in range(start,end):
        globals()['p_pairs_id_S'+str(split)]=globals()['p_pairs_id_S'+str(split)]+locals()['p_pairs_id'+str(i)]

        globals()['p_pairs_m0_S'+str(split)]=globals()['p_pairs_m0_S'+str(split)]+locals()['p_pairs_m0'+str(i)]
        
        globals()['p_pairs_m1_S'+str(split)]=globals()['p_pairs_m1_S'+str(split)]+locals()['p_pairs_m1'+str(i)]
        
        globals()['p_pairs_x0_S'+str(split)]=globals()['p_pairs_x0_S'+str(split)]+locals()['p_pairs_x0'+str(i)]
        
        globals()['p_pairs_y0_S'+str(split)]=globals()['p_pairs_y0_S'+str(split)]+locals()['p_pairs_y0'+str(i)]
        
        globals()['p_pairs_z0_S'+str(split)]=globals()['p_pairs_z0_S'+str(split)]+locals()['p_pairs_z0'+str(i)]
        
        globals()['p_pairs_x1_S'+str(split)]=globals()['p_pairs_x1_S'+str(split)]+locals()['p_pairs_x1'+str(i)]
        
        globals()['p_pairs_y1_S'+str(split)]=globals()['p_pairs_y1_S'+str(split)]+locals()['p_pairs_y1'+str(i)]
        
        globals()['p_pairs_z1_S'+str(split)]=globals()['p_pairs_z1_S'+str(split)]+locals()['p_pairs_y1'+str(i)]
        
        globals()['p_pairs_ds_S'+str(split)]=globals()['p_pairs_ds_S'+str(split)]+locals()['p_pairs_ds'+str(i)]
        
        del locals()['p_pairs_id'+str(i)], locals()['p_pairs_m0'+str(i)], locals()['p_pairs_m1'+str(i)], locals()['p_pairs_x0'+str(i)], locals()['p_pairs_y0'+str(i)], locals()['p_pairs_z0'+str(i)], locals()['p_pairs_x1'+str(i)], locals()['p_pairs_y1'+str(i)], locals()['p_pairs_z1'+str(i)], locals()['p_pairs_ds'+str(i)]
    
   
    with open('p_pairs_id_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_id_S'+str(split)][1:])
        
    with open('p_pairs_m0_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_m0_S'+str(split)][1:])
    
    with open('p_pairs_m1_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_m1_S'+str(split)][1:])
    
    with open('p_pairs_x0_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_x0_S'+str(split)][1:])
        
    with open('p_pairs_y0_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_y0_S'+str(split)][1:])
    
    with open('p_pairs_z0_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_z0_S'+str(split)][1:])

    with open('p_pairs_x1_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_x1_S'+str(split)][1:]) 
    
    with open('p_pairs_y1_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_y1_S'+str(split)][1:])
        
    with open('p_pairs_z1_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_z1_S'+str(split)][1:])
        
    with open('p_pairs_ds_S'+str(split)+'.csv', 'w') as out:
        out.write(globals()['p_pairs_ds_S'+str(split)][1:])
    

file = open('Rockstar_A.csv') #opens file containing top 10 highest mass haloes
data = np.genfromtxt('Rockstar_A.csv', delimiter=',', dtype=str) #extracts data from file

n=len(data[:,0])-1 #number of data values



if __name__ =="__main__":
    t0 = threading.Thread(target=create_p, args=(1,200,0))
    t1 = threading.Thread(target=create_p, args=(201,400,1))
    t2 = threading.Thread(target=create_p, args=(401,600,2))
    t3 = threading.Thread(target=create_p, args=(601,800,3))

    t0.start()
    t1.start()
    t2.start()
    t3.start()
    

    t0.join()
    t1.join()
    t2.join()
    t3.join()

    print("Done!")