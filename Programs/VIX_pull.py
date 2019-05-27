#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 19:47:56 2018

@author: maxsterman
"""
import pandas as pd

import pandas_datareader.data as web
import datetime

import quandl
import os

from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='G71KPESH40O01ZY9', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='VIX',interval='30min', outputsize='full')
os.chdir("/Users/maxsterman/Downloads/PA Term Project_submit/")
os.chdir("Data/VIX/")
Total_VIX=pd.read_csv('all_VIX_data.csv')

os.chdir("/Users/maxsterman/Downloads/PA Term Project_submit/")

data["date"]=data.index
data["date"]=pd.to_datetime(data["date"], format='%Y-%m-%d %H:%M:%S')
data_to_use=data[data["date"] > datetime.datetime(2018,11,22)]
try:
    Total_VIX=Total_VIX.drop(['index','Unnamed: 0'],axis=1)
except:
    print("Congrats. Those columns were already removed")
Total_VIX["date"]=pd.to_datetime(Total_VIX["date"], format='%Y-%m-%d %H:%M:%S')
Residual_VIX=data_to_use[data_to_use["date"] > Total_VIX["date"][Total_VIX.shape[0]-1]]
Total_VIX=pd.concat([Total_VIX,Residual_VIX])
Total_VIX=Total_VIX.reset_index(drop=True)
os.chdir("Data/VIX/")
Total_VIX.to_csv('all_VIX_data.csv')

#os.chdir("/Users/maxsterman/Downloads/PA Term Project/")
#
#os.chdir("Data/VIX/")
#
#VIX_1030=pd.read_csv('VIX_Data_pulled_10_30_2018.csv')
#VIX_1105=pd.read_csv('VIX_Data_pulled_11_05_2018.csv')
#
#
#
#VIX_1030["date"]=pd.to_datetime(VIX_1030["date"],format="%Y-%m-%d %H:%M:%S")
#VIX_1105["date"]=pd.to_datetime(VIX_1105["date"],format="%Y-%m-%d %H:%M:%S")
#VIX_after_1030=VIX_1105[VIX_1105["date"] > VIX_1030["date"][VIX_1030.shape[0]-1]]
#Total_VIX=pd.concat([VIX_1030,VIX_after_1030])
#Total_VIX=Total_VIX.reset_index()
#Total_VIX.to_csv('all_VIX_data.csv')