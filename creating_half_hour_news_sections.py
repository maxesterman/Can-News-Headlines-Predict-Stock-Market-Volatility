#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 11:12:22 2018

@author: maxsterman
"""

import math
import datetime
import pandas as pd
import pickle
import numpy as np
import time
import operator


#metaDataFileReader=open(rootPath+"/Data/News_Headlines/All_Metadata_with_n_grams.pickle",mode='rb')
#newsMetaDataFrame_ngram=pickle.load(metaDataFileReader)
#metaDataFileReader.close()

#newsMetaDataFrame_ngram["Current Day"]=math.nan
#newsMetaDataFrame_ngram["Current Hour"]=math.nan
#newsMetaDataFrame_ngram["Current Minute"]=datet

def get_DateTime(newsMetaDataFrame_ngram):
    badRows=pd.DataFrame(columns=newsMetaDataFrame_ngram.columns.values)
    
#    start_time= time.time()
    
    for i in range(newsMetaDataFrame_ngram.shape[0]):
        try:
            d1=datetime.datetime.strptime(newsMetaDataFrame_ngram.loc[i,"Published Time"],"%Y-%m-%dT%H:%M:%SZ")
    #        newsMetaDataFrame_ngram["Current Day"][i]=d1.strftime("%Y-%m-%d")
    #        newsMetaDataFrame_ngram["Current Hour"][i]=d1.hour
    #        newsMetaDataFrame_ngram["Current Minute"][i]=d1.minute
            
        except:
            print(newsMetaDataFrame_ngram.loc[i,:])
            print("Problem at %d"  % i)
            badRow=newsMetaDataFrame_ngram.loc[i,:].copy()
            newsMetaDataFrame_ngram=newsMetaDataFrame_ngram.drop(i)
            badRows=badRows.append(badRow)
            
            
    #    if (i%100) == 0:
    #        print(i)
    #        curr_time=time.time()
    #        print("Time elapsed: %.2f" % (curr_time-start_time))
    # 
    newsMetaDataFrame_ngram["Published Date"]=pd.to_datetime(newsMetaDataFrame_ngram["Published Time"], format="%Y-%m-%dT%H:%M:%SZ")       
    newsMetaDataFrame_ngram["Published Hour"]=newsMetaDataFrame_ngram["Published Date"].dt.hour
    newsMetaDataFrame_ngram["Published Minute"]=newsMetaDataFrame_ngram["Published Date"].dt.minute
    newsMetaDataFrame_ngram["Published Datestr"]=newsMetaDataFrame_ngram["Published Date"].dt.strftime("%Y-%m-%d")
    
    badRows["Published Date"]=datetime.datetime(year=2100,day=12,month=3, hour=18, minute=30, second=1)
    badRows["Published Hour"]=badRows["Published Date"].dt.hour
    badRows["Published Minute"]=badRows["Published Date"].dt.minute
    badRows["Published Datestr"]=badRows["Published Date"].dt.strftime("%Y-%m-%d")

    
    newsMetaDataFrame_ngram=newsMetaDataFrame_ngram.append(badRows)
    newsMetaDataFrame_ngram=newsMetaDataFrame_ngram.sort_index()
    return newsMetaDataFrame_ngram


def getTopicsMatrix(newsMetaDataFrame_ngram,start_time):
    termCount=dict()
    for i in newsMetaDataFrame_ngram.index.values:
        articleNGramList=newsMetaDataFrame_ngram.loc[i,'NGram Lemmas List']
        for NGram in articleNGramList:
            try:
                termCount[NGram]+=1
            except:
                termCount[NGram]=1
    
        
#        if (i % 20)==0:
#            print(i)
#            curr_time=time.time()
#            print("Time Elapsed: %f" % (curr_time-start_time))
#            if (curr_time-start_time) > 100:
#                break
    sorted_terms=sorted(termCount.items(),key=operator.itemgetter(1),reverse=True)
    return sorted_terms

def main(rootPath):
    articlesByDate=dict()
    topicsByDate=dict()
    metaDataFileReader=open(rootPath+"/Data/News_Headlines/All_Metadata_with_n_grams_and_lemmas.pickle",mode='rb')
    newsMetaDataFrame_ngram=pickle.load(metaDataFileReader)
    metaDataFileReader.close()
    newsMetaDataFrame_ngram=get_DateTime(newsMetaDataFrame_ngram)
    allDates=newsMetaDataFrame_ngram["Published Datestr"].unique()
    start_time=time.time()
    
    for curr_date in allDates:
        print(curr_date)
        pdForDate=newsMetaDataFrame_ngram[newsMetaDataFrame_ngram["Published Datestr"] == curr_date]
        currentDay=pdForDate["Published Date"][pdForDate.index[0]]
        for hour in [9,10,11,12,13,14,15]:
            for half in [0, 30]:
                if (hour == 9) and (half == 0):
                    continue
                
                
                
                print("%d:%02d" % (hour,half))
                curr_time=time.time()
                print("Time Elapsed: %f" % (curr_time-start_time))
                endDateTime=datetime.datetime(year=currentDay.year,\
                                              month=currentDay.month,\
                                              day=currentDay.day,\
                                              hour=hour,\
                                              minute=half)
                startDateTime=endDateTime-datetime.timedelta(minutes=30)
                if (hour == 9) and (half == 30):
                    startDateTime=endDateTime-datetime.timedelta(minutes=((60*9)+3))
                pdForHalfHour=newsMetaDataFrame_ngram[newsMetaDataFrame_ngram["Published Date"] < endDateTime]
                pdForHalfHour=pdForHalfHour[pdForHalfHour["Published Date"] >= startDateTime]
                articlesByDate[curr_date+("_%d:%02d" % (hour,half))]=pdForHalfHour
                topicsByDate[curr_date+("_%d:%02d" % (hour,half))]=getTopicsMatrix(pdForHalfHour,start_time)
        
    articleDateWriter=open(rootPath+"/Data/News_Headlines/articles_by_date.pickle",mode='wb')
    pickle.dump(articlesByDate,articleDateWriter)
    articleDateWriter.close() 
    
    topicsDateWriter=open(rootPath+"/Data/News_Headlines/topics_by_date.pickle",mode='wb')
    pickle.dump(topicsByDate,topicsDateWriter)
    topicsDateWriter.close() 
    
    ngramWithDatesWriter=open(rootPath+"/Data/News_Headlines/All_Metadata_with_n_grams_lemmas_and_better_time.pickle",mode='wb')
    pickle.dump(newsMetaDataFrame_ngram,ngramWithDatesWriter)
    ngramWithDatesWriter.close()
