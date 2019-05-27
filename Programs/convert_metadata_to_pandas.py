#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 13:26:36 2018

@author: maxsterman
"""

import pandas as pd
import os


os.chdir("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines")
News_Headlines_Dates_Dir=os.listdir()

#creating the metadata for the news
#newsMetaDataFrame=pd.DataFrame(columns=["Title","Url","Published Time", "Description","Source"])
dateDirs=['2018-11-15','2018-11-16','2018-11-19','2018-11-20','2018-11-21']


newsMetaDataFrame=pd.read_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata.csv").drop(['Unnamed: 0'], axis=1)

#for currentDate in News_Headlines_Dates_Dir:
for currentDate in dateDirs:
    os.chdir(currentDate)
    print(currentDate)
    News_Headlines_Sources_Dir=os.listdir()
    for source in News_Headlines_Sources_Dir:
        print(source)
        if '.DS_Store' in source:
            continue
        os.chdir(source)
        News_Headlines_Dir=os.listdir()
        for headline in News_Headlines_Dir:
            if "metadata" in headline:
                print(headline)
                
                #opening, reading and splitting the file by line
                f=open(headline,"r")
                fileText=f.read()
                fileMetaDataCategories=fileText.split(" \n")
                
                
                #creating the metadata variables (Title, URL, Time, Description). Note that
                #this was what the split was for and also, note that the file is index [n:] as the first n charachters
                #of this file was part of a string
                fileTitle=fileMetaDataCategories[0][7:]
                fileURL=fileMetaDataCategories[1][5:]
                fileTime=fileMetaDataCategories[2][16:]
                fileDescription=fileMetaDataCategories[3][13:]
                
                #adding the row of metadata variables
                newRow=pd.DataFrame(data=[[fileTitle,fileURL,fileTime,fileDescription,source]],\
                                    columns=["Title","Url","Published Time", "Description","Source"])
                newsMetaDataFrame=newsMetaDataFrame.append(newRow)
                
                
                #closing the file
                f.close()
        
        #once all files by the source has been read, we are finished
        os.chdir("..")
    os.chdir("..")
        
                
newsMetaDataFrame=newsMetaDataFrame.reset_index().drop(['index'],axis=1)
newsMetaDataFrame.to_csv("/Users/maxsterman/Downloads/PA Term Project_submit/Data/News_Headlines/All_Metadata.csv")                    
                
