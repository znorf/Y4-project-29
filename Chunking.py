import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.neighbors import KDTree
from matplotlib.colors import LogNorm
import math as math
import time as time

start = time.time()
data = pd.read_csv("snapdata_125.txt", delimiter=(" "),
                   #usecols=["ID","PID","MVIR","RVIR","XYZ"],
                   chunksize= 100000)

for idx,chunk in enumerate(data):
    if idx ==0:
        df = pd.DataFrame(chunk)
        df = df.drop(['TreeRoot,',
               'mvir_all,', 'M200C', 'M200b'],axis = 1)
        print(df.head())
    else:
        break

print(df.iloc[5,5])
'''
for idx,chunk in enumerate(data):
    print(idx)
    df = pd.DataFrame(chunk)
    df = df.drop(['TreeRoot,',
           'mvir_all,', 'M200C', 'M200b'],axis = 1)

'''
#356 * 100,000
