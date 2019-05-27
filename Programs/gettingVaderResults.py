#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 15:32:08 2018

@author: maxsterman
"""
import pandas as pd
import numpy as np
import math
import time

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


newsMetaDataFrame=pd.read_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata.csv")

newsMetaDataFrame_vader=pd.read_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_With_Vader_Sentiment.csv")


newsMetaDataFrame['Vader_neg']=newsMetaDataFrame_vader['Vader_neg']
newsMetaDataFrame['Vader_neu']=newsMetaDataFrame_vader['Vader_neu']
newsMetaDataFrame['Vader_pos']=newsMetaDataFrame_vader['Vader_pos']
newsMetaDataFrame['Vader_comp']=newsMetaDataFrame_vader['Vader_comp']

#newsMetaDataFrame['Vader_neg']=math.nan
#newsMetaDataFrame['Vader_neu']=math.nan
#newsMetaDataFrame['Vader_pos']=math.nan
#newsMetaDataFrame['Vader_comp']=math.nan

text_Analyzer = SentimentIntensityAnalyzer()

start_time=time.time()

for i in range(newsMetaDataFrame.shape[0]):
    
    if i < newsMetaDataFrame_vader.shape[0]:
        continue
    
    if i % 20 == 0:
        curr_time=time.time()
        print(i)
        print("Time passed: %f" % (start_time-curr_time))
    
    vaderResults = text_Analyzer.polarity_scores(newsMetaDataFrame['Title'][i])
    newsMetaDataFrame['Vader_neg'][i]=vaderResults['neg']
    newsMetaDataFrame['Vader_neu'][i]=vaderResults['neu']
    newsMetaDataFrame['Vader_pos'][i]=vaderResults['pos']
    newsMetaDataFrame['Vader_comp'][i]=vaderResults['compound']



newsMetaDataFrame.to_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_With_Vader_Sentiment.csv")    
