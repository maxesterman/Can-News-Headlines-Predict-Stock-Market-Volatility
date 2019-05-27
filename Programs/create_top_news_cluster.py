#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 19:43:35 2018

@author: maxsterman
"""
import numpy as np
import pandas as pd
import datetime
import time
import math
import pickle


def DBSCAN(df,minPts,epsilon,topicsList,numTopics):
    rowIndexes=list(df.index.values)
    docTermMatrix=np.zeros((len(rowIndexes),numTopics))
    topTopicsList=[topicTuple[0] for topicTuple in topicsList[0:numTopics]]
    docTermToRowIndex=dict()
    k=0
    for rowNum in rowIndexes:
        docTermToRowIndex[k]=rowNum
        NGramLemmas=df.loc[rowNum,'NGram Lemmas List']
        for i in range(len(topTopicsList)):
            if topTopicsList[i] in NGramLemmas:
                docTermMatrix[k,i]=1
        k+=1
    
    
    wordsInCommon=np.zeros((0,docTermMatrix.shape[0]))
    #print(wordsInCommon.shape)
    for docNum in range(docTermMatrix.shape[0]):
        currentDoc=docTermMatrix[docNum,:]
        wordsInCommonForDoc=(currentDoc*docTermMatrix).sum(axis=1).reshape(1,docTermMatrix.shape[0])
        wordsInCommon=np.concatenate([wordsInCommon,wordsInCommonForDoc],axis=0)
        
    #findingCorePoints 
    #1) find the number with topics greater than epsilon
    #2) find if that number is greater than minpts
    epsilonPtsInCommonMat=(wordsInCommon>=epsilon).astype(int)
    epsilonPtsInCommon=epsilonPtsInCommonMat.sum(axis=1)
    epsilonPtsInCommon=epsilonPtsInCommon.reshape(epsilonPtsInCommon.shape[0])
    #print(epsilonPtsInCommon.tolist())
    indexWMinPts=np.argwhere(epsilonPtsInCommon>=minPts)
    CorePts=indexWMinPts.reshape(indexWMinPts.shape[0]).tolist()
    
    #print("Core Points: ")
    #print(CorePts)
    
    #finding all the rows with epsilon points in common
    corePtsArray=epsilonPtsInCommonMat[CorePts,:]  
    
    
    potentialBorderPoints=np.unique(np.argwhere(corePtsArray > 0)[:,1]).tolist()
    #print("Border Points: ")
    #print(potentialBorderPoints)
    corePlusBorderSet=set(CorePts).union(set(potentialBorderPoints))
    corePlusBorder=sorted(list(corePlusBorderSet))
    
    #index for pandas
    corePlusBorderIndexes=[docTermToRowIndex[k] for k in corePlusBorder]       
    
    return epsilonPtsInCommonMat,corePlusBorderIndexes
    


def findAtLeastN(ngramList,n):
    for i in range(len(ngramList)):
        curr_value=ngramList[i][1]
        if curr_value<n:
            return i
                

def main(rootPath):

        
    articleDateWriter=open(rootPath+"/Data/News_Headlines/articles_by_date.pickle",mode='rb')
    articlesByDate=pickle.load(articleDateWriter)
    articleDateWriter.close() 
    
    topicsDateWriter=open(rootPath+"/Data/News_Headlines/topics_by_date.pickle",mode='rb')
    topicsByDate=pickle.load(topicsDateWriter)
    topicsDateWriter.close() 
    
    ngramWithDatesWriter=open(rootPath+"/Data/News_Headlines/All_Metadata_with_n_grams_lemmas_and_better_time.pickle",mode='rb')
    newsMetaDataFrame_ngram=pickle.load(ngramWithDatesWriter)
    ngramWithDatesWriter.close()



    newsMetaDataFrame_ngram_Good_Dates=newsMetaDataFrame_ngram[newsMetaDataFrame_ngram['Published Date'].dt.year <= datetime.date.today().year]
    allDates=newsMetaDataFrame_ngram_Good_Dates["Published Datestr"].unique()
    
    start_time=time.time()
    pointsPerHalfHour=dict()
    
    for curr_date in allDates:
        print(curr_date)
        pdForDate=newsMetaDataFrame_ngram_Good_Dates[newsMetaDataFrame_ngram_Good_Dates["Published Datestr"] == curr_date]
        currentDay=pdForDate["Published Date"][pdForDate.index[0]]
        for hour in [9,10,11,12,13,14,15]:
            for half in [0, 30]:
                if (hour == 9) and (half == 0):
                    continue
                print("%d:%02d" % (hour,half))
                curr_time=time.time()
                print("Time Elapsed: %f" % (curr_time-start_time))
                current_articles=articlesByDate[curr_date+("_%d:%02d" % (hour,half))]
                current_topics=topicsByDate[curr_date+("_%d:%02d" % (hour,half))]
                
                num_terms_to_use=findAtLeastN(current_topics,2)
                #epsPts,corePlusBorderPts=DBSCAN(current_articles,4,3,current_topics,num_terms_to_use)
                epsPts,corePlusBorderPts=DBSCAN(current_articles,4,3,current_topics,30)
                pointsPerHalfHour[curr_date+("_%d:%02d" % (hour,half))]=corePlusBorderPts
                
    pointsPerHalfHourWriter=open(rootPath+"/Data/News_Headlines/per_half_hour_headlines.pickle",mode='wb')   
    pickle.dump(pointsPerHalfHour,pointsPerHalfHourWriter)
    pointsPerHalfHourWriter.close()
    