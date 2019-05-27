#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 17:07:19 2018

@author: maxsterman
"""


#test_results=All_Data_Needed.copy()
#test_results.index=test_results.date

import datetime
import pandas as pd
import os
import statsmodels.api as sm
import math

def main(rootPath):
    all_results=pd.read_csv(rootPath+"/Data/All_Data_Original_DBSCAN.csv")
    #all_results
    
    os.chdir(rootPath+"/Data/")
    all_results=all_results.rename_axis({'1. open':'Level_VIX_Day_Ago','4. close':'Level_VIX_Current'},axis=1)
    all_results['Level_VIX_Day_Ago']=all_results['Level_VIX_Day_Ago'].shift(12)
    
    dep_vars=['VIX Change', 'TB_polarity', 'TB_subjectivity', 'Vader_comp',
           'Vader_neg', 'Vader_neu', 'Vader_pos']
    wanted_series=all_results[dep_vars+['date','Level_VIX_Day_Ago','Level_VIX_Current']]
    
    for var in dep_vars:
        for i in range(1,14):
            wanted_series["%s_lag_%d" % (var,i)]=wanted_series[var].shift(i)
            
    wanted_series["date"]=pd.to_datetime(wanted_series["date"],format="%Y-%m-%d %H:%M:%S")
    
    
    wanted_series.to_csv("All_Data_Original_DBSCAN_plus_lags.csv")

