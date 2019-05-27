#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 11:57:51 2018

@author: maxsterman
"""

import os
rootPath="/Users/maxsterman/Downloads/PA Term Project_submit"

programPath=rootPath+"/Programs"

os.chdir(programPath)

import creating_half_hour_news_sections
import create_top_news_cluster
import makingSentimentScores
import saving_lags_to_csv
import calculating_ar_test_Set
import plotting_time_series_of_vars



os.chdir(programPath)
creating_half_hour_news_sections.main(rootPath)
os.chdir(programPath)
create_top_news_cluster.main(rootPath)
os.chdir(programPath)
makingSentimentScores.main(rootPath)
os.chdir(programPath)
saving_lags_to_csv.main(rootPath)
os.chdir(programPath)
calculating_ar_test_Set.main(rootPath)
os.chdir(programPath)
plotting_time_series_of_vars.main(rootPath)
