#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 20:00:40 2018

@author: maxsterman
"""

import datetime
import pandas as pd
import os
import statsmodels.api as sm
import math
import numpy as np


#rootPath="/Users/maxsterman/Downloads/"

def main(rootPath):
    all_results=pd.read_csv(rootPath+"/Data/All_Data_Original_DBSCAN.csv")
    print(all_results)
    
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
    
    
    
    os.chdir(rootPath+"/Data/ARIMAX")
    
    test_series=wanted_series[wanted_series['date'] >= datetime.datetime(2018,11,15)]
    train_series=wanted_series[wanted_series['date'] < datetime.datetime(2018,11,15)]
    
    train_series.index=train_series["date"]
    test_series.index=test_series["date"]
    
    indep_vars=['TB_polarity', 'TB_subjectivity', 'Vader_comp',
           'Vader_neg', 'Vader_neu', 'Vader_pos']
    
    
    p_max=8
    
    coeff_lags_string_list=["Coeff Lag %d" % i for i in range(1,p_max)]
    pval_lags_string_list=["Pval Lag %d" % i for i in range(1,p_max)]
    
    #ARIMA_X_df=pd.DataFrame(columns=["X","p","d","q","AIC","BIC","Log-Lik"]+coeff_lags_string_list+pval_lags_string_list)
    
    rmse_df=pd.DataFrame(index=[i for i in range(1,p_max)],columns=dep_vars)
    dir_df=pd.DataFrame(index=[i for i in range(1,p_max)],columns=dep_vars)
    first_diff_dir_df=pd.DataFrame(index=[i for i in range(1,p_max)],columns=dep_vars)
    Level_dir_df=pd.DataFrame(index=[i for i in range(1,p_max)],columns=dep_vars)
    Level_first_diff_dir_df=pd.DataFrame(index=[i for i in range(1,p_max)],columns=dep_vars)
    
    
    
    for p in range(1,p_max):
        print("p: %d" % p)
        VIX_vars_to_use=["VIX Change_lag_%d" % (i) for i in range(1,(p+1))]
        print(VIX_vars_to_use)
        train_series_to_use=train_series[["VIX Change"]]
        train_series_to_use=train_series_to_use.dropna()
        
        test_series_to_use=test_series[VIX_vars_to_use]
        test_series_to_use=sm.add_constant(test_series_to_use)
        #print("Using test series")
        #print(test_series_to_use)
        #print("test series used")
        test_VIX=test_series["VIX Change"]
        
        model_to_use=sm.tsa.ARIMA(endog=train_series_to_use["VIX Change"],
                                                order=[p,0,0])
        results_model=model_to_use.fit()
        
        
        
        ar_params=[results_model.params["ar.L%d.VIX Change" % (lag_num)] for lag_num in range(1,(p+1))]
        const_params=[results_model.params["const"]]
        
        const_array=np.array(const_params+ar_params)
        const_array=np.reshape(const_array,(test_series_to_use.shape[1],1))
        
        
        test_VIX_values=test_VIX.values
        test_VIX_values_diff=np.diff(test_VIX_values)
        pred_values=np.dot(test_series_to_use,const_array)
        pred_values_size=pred_values.shape[0]
        
        pred_values=pred_values.reshape(pred_values_size)
        pred_values_diff=np.diff(pred_values)
        
        forecast_errors=test_VIX_values-pred_values
        forecast_errors_sq=np.square(forecast_errors)
        
        mse=forecast_errors_sq.sum()/pred_values_size
        rmse=np.sqrt(mse)
        
        direction=np.sum(((test_VIX_values*pred_values) > 0).astype(int))/len(pred_values)
        direction_first_diff=np.sum(((test_VIX_values_diff*pred_values_diff) > 0).astype(int))/len(pred_values_diff)
        
        
        
        
        
        
        
        print(ar_params)
        print(const_params)
        print(test_series_to_use.head())
        print(rmse)
        rmse_df.loc[p,"VIX Change"]=rmse
        dir_df.loc[p,"VIX Change"]=np.round(direction,3)
        first_diff_dir_df.loc[p,"VIX Change"]=np.round(direction_first_diff,3)
        
    
    
    
    import time
    time.sleep(5)
    
    for var in indep_vars:
        print("var: %s" % var)
        for p in range(1,p_max):
            print("p: %d" % p)
            vars_to_use=["%s_lag_%d" % (var,i) for i in range(1,(p+1))]
            VIX_vars_to_use=["VIX Change_lag_%d" % (i) for i in range(1,(p+1))]
            print(VIX_vars_to_use)
            train_series_to_use=train_series[["VIX Change"]+vars_to_use]
            train_series_to_use=train_series_to_use.dropna()
            
            test_series_to_use=test_series[vars_to_use+VIX_vars_to_use]
            test_series_to_use=sm.add_constant(test_series_to_use)
            test_VIX=test_series["VIX Change"]
            test_Level_VIX_day_ago=test_series["Level_VIX_Day_Ago"]
            test_Level_VIX_today=test_series["Level_VIX_Current"]
            
            model_to_use=sm.tsa.ARIMA(endog=train_series_to_use["VIX Change"],exog=train_series_to_use[vars_to_use],
                                                    order=[p,0,0])
            results_model=model_to_use.fit()
            
            
            
            exog_params=[results_model.params["%s_lag_%d" % (var, lag_num)] for lag_num in range(1,(p+1))]
            ar_params=[results_model.params["ar.L%d.VIX Change" % (lag_num)] for lag_num in range(1,(p+1))]
            const_params=[results_model.params["const"]]
            
            const_array=np.array(const_params+exog_params+ar_params)
            const_array=np.reshape(const_array,(test_series_to_use.shape[1],1))
            
            
            test_VIX_values=test_VIX.values
            test_VIX_values_diff=np.diff(test_VIX_values)
#            test_Level_VIX_today=np.diff(test_Level_VIX_today.values)
#            test_Level_VIX_day_ago=test_Level_VIX_today.values
    
            pred_values=np.dot(test_series_to_use,const_array)
            pred_values_size=pred_values.shape[0]
            
            pred_values=pred_values.reshape(pred_values_size)
            pred_values_diff=np.diff(pred_values)
    
            forecast_errors=test_VIX_values-pred_values
            forecast_errors_sq=np.square(forecast_errors)
            
            mse=forecast_errors_sq.sum()/pred_values_size
            rmse=np.sqrt(mse)
            
            direction=(np.sum(((test_VIX_values*pred_values) > 0).astype(int))/len(pred_values))*100
            direction_first_diff=(np.sum(((test_VIX_values_diff*pred_values_diff) > 0).astype(int))/len(pred_values_diff))*100
    
            
    
            
            
            print(exog_params)
            print(ar_params)
            print(const_params)
            rmse_df.loc[p,var]=rmse
            dir_df.loc[p,var]=np.round(direction,3)
            first_diff_dir_df.loc[p,var]=np.round(direction_first_diff,3)
    
    
            #ARIMA_X_df=ARIMA_X_df.append(newResults)
        
    os.chdir(rootPath+"/Data")
    rmse_df.to_csv("Results/ARIMAX_rmses.csv")
    dir_df.to_csv("ARIMAX/ARIMAX_direction.csv")
    first_diff_dir_df.to_csv("Results/ARIMAX_first_diff_direction.csv")
    
    #wanted_series=wanted_series.dropna()
    #model3=sm.tsa.ARIMA(endog=wanted_series["VIX Change"],exog=wanted_series[["Vader_neu_lag_1",
    #                                        "Vader_neu_lag_2","Vader_neu_lag_3",
    #                                        "Vader_neu_lag_4","Vader_neu_lag_5",
    #                                        "Vader_neu_lag_6","Vader_neu_lag_7",
    #                                        "Vader_neu_lag_8","Vader_neu_lag_9",
    #                                        "Vader_neu_lag_10","Vader_neu_lag_11",
    #                                        "Vader_neu_lag_12","Vader_neu_lag_13",]],
    #                                        order=[13,0,0])
    #results3=model3.fit()
    #print(results3.summary())
