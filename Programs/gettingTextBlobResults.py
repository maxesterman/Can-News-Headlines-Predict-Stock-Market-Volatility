#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 15:32:08 2018

@author: maxsterman
"""
import pandas as pd
import numpy as np

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import math
import time

newsMetaDataFrame=pd.read_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata.csv")
newsMetaDataFrame_text_blob=pd.read_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_with_text_blob.csv")

newsMetaDataFrame['TB_subjectivity']=newsMetaDataFrame_text_blob['TB_subjectivity']
newsMetaDataFrame['TB_polarity']=newsMetaDataFrame_text_blob['TB_polarity']



start_time=time.time()

#currWord=""
#
#for i in range(newsMetaDataFrame.shape[0]):
#    
#    if i == 100:
#        break
#    
#    if i % 20 == 0:
#        curr_time=time.time()
#        print(i)
#        print("Time passed: %f" % (start_time-curr_time))
#
#
#
#    currWord+=(newsMetaDataFrame["Title"][i]+" \n")
#    
#allWords=currWord.split(" \n")[:-1]


for i in range(newsMetaDataFrame.shape[0]):
    
    if i < newsMetaDataFrame_text_blob.shape[0]:
        continue
    
    if i % 1000 == 0:
        newsMetaDataFrame.to_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_with_text_blob.csv")
    
    ##if i == 100:
    ##    break
    
    if i % 20 == 0:
        curr_time=time.time()
        print(i)
        print("Time passed: %f" % (curr_time-start_time))
    
    currentBlob = TextBlob(newsMetaDataFrame["Title"][i])
    newsMetaDataFrame['TB_subjectivity'][i]=currentBlob.sentiment.subjectivity
    newsMetaDataFrame['TB_polarity'][i]=currentBlob.sentiment.polarity



newsMetaDataFrame.to_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_with_text_blob.csv")
