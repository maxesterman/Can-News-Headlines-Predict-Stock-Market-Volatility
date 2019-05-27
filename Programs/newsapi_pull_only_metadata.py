#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 20:59:35 2018

@author: maxsterman
"""

from newsapi import NewsApiClient
import time



# /v2/top-headlines
#top_headlines2 = newsapi2.get_top_headlines(q='trump',
#                                          sources='cnn,cbs-news,fox-news')


import os

news_sources=['abc-news',
 'al-jazeera-english',
 'associated-press',
 'axios',
 'bloomberg',
 'breitbart-news',
 'business-insider',
 'cbs-news',
 'cnn',
 'cnbc',
 'fortune',
 'fox-news',
 'google-news',
 'msnbc',
 'national-review',
 'nbc-news',
 'newsweek',
 'new-york-magazine',
 'politico',
 'reddit-r-all',
 'reuters',
 'the-american-conservative',
 'the-hill',
 'the-huffington-post',
 'the-new-york-times',
 'the-washington-post',
 'the-washington-times',
 'the-wall-street-journal',
 'time',
 'usa-today',
 'vice-news']
'''
startdate_list=['2018-11-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05',\
                '2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12',\
                '2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19',\
                '2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26']
'''

startdate_list=['2018-12-17','2018-12-18','2018-12-19','2018-12-20','2018-12-21']


for startdate in startdate_list:
    print(startdate)
    newsSourceDict=dict()
    newsapiDict=dict()

    starttime=startdate+"T00:00:01"
    endTime=startdate+"T16:30:00"
    os.chdir("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines")
    try:
        os.mkdir(startdate)
    except:
        print("Directory {} already made".format(startdate))
        
    os.chdir(startdate)
    for newsSource in news_sources:
    
        # Init
        
        print(newsSource)
        newsapiDict[newsSource] = NewsApiClient(api_key='232a4fc08ea04a1d84419b7f677611ae')
        newsSourceDict[newsSource]= newsapiDict[newsSource].get_everything(sources=newsSource, from_param=starttime,\
                      to=endTime, sort_by='popularity', page_size=100, language='en')
        time.sleep(3)
        
    
    
    
    '''
    news_sources=['abc-news','nbc-news','fox-news','the-new-york-times','the-washington-post','the-fox-news',\
                  'the-wall-street-journal','google-news','cnn','usa-today','the-huffington-post','the-hill',\
                  'breitbart-news','politico','reuters']
    '''
    
    
    
    
    print(" ")
    print("making metadata")
    print(" ")
    for source in news_sources:
        try:
            os.mkdir(source)
        except:
            print("Directory {} already made".format(source))
        os.chdir(source)
        print(source)
        
    
        
        for i in range(len((newsSourceDict[source])['articles'])):
            metadataFile=open("metadata_article_{}.txt".format(i),'w')
            metadataFile.write("Title: {} \n".format((newsSourceDict[source])['articles'][i]['title']))
            metadataFile.write("Url: {} \n".format((newsSourceDict[source])['articles'][i]['url']))
            metadataFile.write("Published Time: {} \n".format((newsSourceDict[source])['articles'][i]['publishedAt']))
            metadataFile.write("Description: {} \n".format((newsSourceDict[source])['articles'][i]['description']))
            metadataFile.close()
            
            ##f.write(str(yuppyText.prettify))
            #print(i)
            time.sleep(0.01)
        os.chdir('..')
    ## /v2/everything
    #all_articles = newsapi.get_everything(q='bitcoin',
    #                                      sources='bbc-news,the-verge',
    #                                      domains='bbc.co.uk,techcrunch.com',
    #                                      from_param='2017-12-01',
    #                                      to='2017-12-12',
    #                                      language='en',
    #                                      sort_by='relevancy',
    #                                      page=2)
    
    # /v2/sources
    #sources2 = newsapi3.get_sources()