#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 19:05:08 2018

@author: maxsterman
"""
import pickle
import pandas as pd
import datetime
import numpy as np


def main(rootPath):

#if "yes" == "yes":
    
    
    #rootPath="/Users/maxsterman/Downloads/PA Term Project_submit"
    pointsPerHalfHourWriter=open(rootPath+"/Data/News_Headlines/per_half_hour_headlines.pickle",mode='rb')   
    pointsPerHalfHour=pickle.load(pointsPerHalfHourWriter)
    pointsPerHalfHourWriter.close()
    
    vaderMetaDataFrame=pd.read_csv(rootPath+"/Data/News_Headlines/All_Metadata_With_Vader_Sentiment.csv")
    
    textBlobMetaDataFrame=pd.read_csv(rootPath+"/Data/News_Headlines/All_Metadata_with_text_blob.csv")

    curr_metadata=pd.DataFrame(columns=["date","Vader_neg","Vader_neu","Vader_pos","Vader_comp","TB_subjectivity","TB_polarity"])
    for key in pointsPerHalfHour.keys():
        topics_index_list=pointsPerHalfHour[key]
        key_to_use=""
        if key.split('_')[1]=='9:30':
            print(key)
            print(key.split('_'))
            current_day=datetime.datetime.strptime(key.split('_')[0],"%Y-%m-%d")
            day_of_week=current_day.weekday()
            if day_of_week == 0:
                yesterdayString=(current_day-datetime.timedelta(days=3)).strftime("%Y-%m-%d")
            else:
                yesterdayString=(current_day-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            key_to_use=yesterdayString+' 16:00:00'
        else:
            print(key)
            print(key.split('_'))
            key_to_use=key.split('_')[0]+" "+key.split('_')[1]+":00"
        print(key_to_use)

        if len(topics_index_list)==0:
            curr_time_df=pd.DataFrame(data={"date":[key_to_use],"Vader_neg":[0.0],"Vader_neu":[1.0], "Vader_pos":[0.0],
                                       "Vader_comp":[0.0],"TB_subjectivity":[0.0],"TB_polarity":[0.0]})
            curr_metadata=curr_metadata.append(curr_time_df)
            continue
        
        curr_vader=vaderMetaDataFrame.loc[topics_index_list,["Vader_neg","Vader_neu","Vader_pos","Vader_comp"]]
        curr_vader_avg=curr_vader.mean().to_frame().transpose()
        curr_TB=textBlobMetaDataFrame.loc[topics_index_list,["TB_subjectivity","TB_polarity"]]
        curr_TB_avg=curr_TB.mean().to_frame().transpose()
        curr_time_df=pd.DataFrame(data={"date":[key_to_use]})
        curr_time_df=pd.concat([curr_time_df,curr_vader_avg,curr_TB_avg],axis=1)
        curr_metadata=curr_metadata.append(curr_time_df)
 
    curr_metadata=curr_metadata.reset_index(drop=True)       
#    curr_metadata=curr_metadata.set_index('date')
    curr_metadata.to_csv(rootPath+"/Data/News_Headlines/sentiment_scores_DBSCAN_training_and_test.csv")
    
    Total_VIX=pd.read_csv(rootPath+"/Data/VIX/all_VIX_data.csv")
    Total_VIX["VIX Change"]=np.log(Total_VIX["4. close"]/Total_VIX["1. open"].shift(12))
    
    curr_metadata["date"]=pd.to_datetime(curr_metadata["date"], format="%Y-%m-%d %H:%M:%S")
    Total_VIX["date"]=pd.to_datetime(Total_VIX["date"], format="%Y-%m-%d %H:%M:%S")
    VIX_And_Sent_Data=pd.merge(Total_VIX,curr_metadata,on="date")
    VIX_And_Sent_Data.to_csv(rootPath+"/Data/All_Data_Original_DBSCAN.csv")
    
    
