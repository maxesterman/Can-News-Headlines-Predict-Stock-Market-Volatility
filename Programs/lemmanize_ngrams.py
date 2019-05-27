#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 22:30:25 2018

@author: maxsterman
"""



import time
import pandas as pd
import pickle
import numpy as np
from nltk.stem import WordNetLemmatizer
from copy import deepcopy

countryListReader=open('pickle_country_list.pickle',mode='rb')
countryList=pickle.load(countryListReader)
countryListReader.close()

metaDataFileReader=open("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_with_n_grams.pickle",mode='rb')
newsMetaDataFrame=pickle.load(metaDataFileReader)
metaDataFileReader.close()

nGramSeries=newsMetaDataFrame['NGram List']
allNGramVectors=nGramSeries.tolist()
allNGramLemmas=deepcopy(allNGramVectors)



i=0
start_time=time.time()

wordnet_lemmatizer=WordNetLemmatizer()
wordnet_lemmatizer.lemmatize('dogs')




for NgramVector in allNGramLemmas:
    for num in range(len(NgramVector)):
        Ngram=NgramVector[num]
        splitWord=Ngram.split()
        for wordNum in range(len(splitWord)):
            curr_word=splitWord[wordNum]
            #lemma_word=wordnet_lemmatizer.lemmatize(curr_word)
            if curr_word in countryList:
                splitWord[wordNum]=curr_word
            else:
                lower_word=curr_word.lower()
                splitWord[wordNum]=wordnet_lemmatizer.lemmatize(lower_word)
        NgramVector[num]=' '.join(splitWord)
    if (i % 1000) == 0:
        print(i)
        curr_time=time.time()
        print("elapsed time: %f" % (curr_time-start_time))
    i=i+1

newsMetaDataFrame['NGram Lemmas List']=pd.Series(np.array(allNGramLemmas))
metaDataFileReader=open("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata_with_n_grams_and_lemmas.pickle",mode='wb')
pickle.dump(newsMetaDataFrame,metaDataFileReader)
metaDataFileReader.close()
