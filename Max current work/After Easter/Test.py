import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.neighbors import KDTree
from matplotlib.colors import LogNorm
import math as math
import time 
import pyarrow.parquet as pa

#data = pd.read_csv('100box.csv')

                       #number of data values 

Npairs = np.array(pd.read_csv('Npairs1.csv',header=None))  





table = pa.read_table('Physical_Pair_Chunk_i_0.parquet') 
Ppairs1 = table.to_pandas() 
table = pa.read_table('Physical_Pair_Chunk_i_1.parquet') 
Ppairs2 = table.to_pandas() 

table = pa.read_table('P_Chunks.parquet') 
df_Chunk = table.to_pandas() 
print(df_Chunk.head())
i = 0
#while i < len(df5):
while i < 20:
    global chunks
    data = pd.DataFrame()
    chunks = df_Chunk.iloc[i,1]
    chunks = chunks.replace("[", "")
    chunks = chunks.replace("]", "")
    chunks = chunks.replace("'", "")
    chunks = chunks.replace(",", "")
    chunks = chunks.replace("-1", "3")  #might have to adjust this!
    chunks = chunks.replace("4", "1")  #might have to adjust this!
    chunks = chunks.split(" ")  

    overlaps = np.arange(0,len(chunks))
    for j in overlaps:
        table = pa.read_table('Chunk_'+str(chunks[j])+'.parquet')
        df = table.to_pandas()
        df = df.drop('# ID', axis=1)
        col_to_move = df.pop(' RVIR')  # Remove & store column
        df[' RVIR'] = col_to_move      # Re-add at the end
        data = pd.concat([data, df], ignore_index=True, sort=False)
    ran = random.randint(0,1)
    if ran == 0:
        cluster1,cluster2 = int(Ppairs1.iloc[i,0]), int(Ppairs2.iloc[i,0])  
    else: 
        cluster2,cluster1 = int(Ppairs2.iloc[i,0]), int(Ppairs1.iloc[i,0])
        
    #cluster1,cluster2 = int(Ppairs1.iloc[i,0]), int(Ppairs2.iloc[i,0]) 
    
    
    
    
    i+=1

print(chunks)
