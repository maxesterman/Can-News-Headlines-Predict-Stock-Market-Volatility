#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 21:42:57 2018

@author: maxsterman
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

def main(rootPath):
    os.chdir(rootPath+"/Data")
    
    All_Data_For_Charts=pd.read_csv("All_Data_Original_DBSCAN.csv")
    All_Data_For_Charts["date"]=pd.to_datetime(All_Data_For_Charts["date"],format="%Y-%m-%d %H:%M:%S")
    All_Data_For_Charts.index=All_Data_For_Charts["date"]
    
    #dep_vars=['VIX Change', 'TB_polarity', 'TB_subjectivity', 'Vader_comp',
    #       'Vader_neg', 'Vader_neu', 'Vader_pos']
    
    dep_vars=['TB_polarity', 'TB_subjectivity', 'Vader_comp',
           'Vader_neg', 'Vader_neu', 'Vader_pos']
    
    fig = plt.figure()
    fig.subplots_adjust(hspace=0)
    axPlots=[fig.add_subplot(int('61%d' % i)) for i in range(1,7)]
    
    i=0
    
    for var in dep_vars:
        
    #    if var =='VIX_Change':
    #        curr_chart_df=All_Data_For_Charts[["date",var]]
    #    else:
    #        curr_chart_df=pd.concat([All_Data_For_Charts["date"],All_Data_For_Charts[var].rolling(13).mean()], axis=1)
        
        curr_chart_df=pd.concat([All_Data_For_Charts["date"],All_Data_For_Charts[[var,"VIX Change"]].rolling(13).mean()], axis=1)
        curr_chart_df["VIX Change"]=(curr_chart_df["VIX Change"]-curr_chart_df["VIX Change"].mean())/(curr_chart_df["VIX Change"].std())
        curr_chart_df[var]=(curr_chart_df[var]-curr_chart_df[var].mean())/(curr_chart_df[var].std())
    
        
        curr_chart_df.plot(x="date",y=[var,"VIX Change"],legend=False,ax=axPlots[i],figsize=(12,12))
        axPlots[i].set_ylabel(var)
        #axPlots[i].update(hspace=0)
        i+=1
    #    test_plot=curr_chart_df.plot(x="date",y=var,title=var,legend=False,figsize=(10,10))
    #    if var =='VIX_Change':
    #        test_plot.set_ylabel('Log Change')
    #    else:
    #        test_plot.set_ylabel('Sentiment Score')
        
        
        #fig = test_plot.get_figure()
            
            
        #fig.savefig("%s_as_time_series.png" %(var))
    #fig.savefig("all_time_series.png")
    os.chdir(rootPath+"/Data/Results")
    fig.savefig("all_time_series_against_VIX.png")
