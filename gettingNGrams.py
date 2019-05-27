#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 15:01:35 2018

@author: maxsterman
"""

from nltk import ngrams
import pandas as pd
import time
import math
import pickle

newsMetaDataFrame=pd.read_csv\
("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_no_stop_words_updated.csv")
newsMetaDataFrame=newsMetaDataFrame.drop(['Unnamed: 0'],axis=1)

metaDataFileReader=open("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_with_n_grams.pickle",mode='rb')
newsMetaDataFrame_ngram=pickle.load(metaDataFileReader)
metaDataFileReader.close()

newsMetaDataFrame['NGram List']=newsMetaDataFrame_ngram['NGram List']

#starter=[]
#for i in range(newsMetaDataFrame.shape[0]):
##    newsMetaDataFrame['NGram List'][i]=['hello']
#    starter.append(["hello"])
#newsMetaDataFrame['NGram List']=starter



start_time=time.time()

for i in range(newsMetaDataFrame.shape[0]):
    if i == 19338:
        print("success")
        
    if i < newsMetaDataFrame_ngram.shape[0]:
        continue
    
    if (i%100) == 0:
        print(i)
        curr_time=time.time()
        print("Time passed: %f" % (curr_time-start_time))
    
    nGramForTitle=[]
        
    
    title=newsMetaDataFrame.loc[i,'Title']

    if type(title) is not str:
        newsMetaDataFrame.loc[i,'NGram List']=[]
        continue

    for nGramSize in range(1,5):
        nGramsGen=ngrams(title.split(), nGramSize)
        
        
        for currNgram in nGramsGen:
            nGramForTitle.append(' '.join(currNgram))
    
    newsMetaDataFrame.loc[i,'NGram List']=nGramForTitle
    

allMetadatafileWriter=open("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_with_n_grams.pickle",mode='wb')
pickle.dump(newsMetaDataFrame,allMetadatafileWriter)
allMetadatafileWriter.close()  
#newsMetaDataFrame.to_csv("/Users/maxsterman/Downloads/PA Term Project/Data/News_Headlines/All_Metadata_with_n_grams.csv")
