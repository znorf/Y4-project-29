# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 14:22:25 2025

@author: Student
"""


import polars as pl
import pandas as pd


def convert(data):
        df=pl.read_csv(data+'.csv')
        df.write_parquet(data+'.parquet')

data_names=['Physical_Pairs_ds'
            ]

for i in range(0,len(data_names)):
    convert(data_names[i])