#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 20/07/2018
#version: 0.2

# PREVIOUSLY: check duplicates in customers' files (.csv files in 'csv/' path)
# with offDoms/check_dups.py script and remove them manually

# to change extension from .csv to .dat (results in 'files/DAT/'):
#rename 's/\.csv$/\.dat/' *.csv

# extract used tlds
python3 offDoms/extract-tlds.py >> offDoms/extracted-TLDs.txt

# 1. Generate dictFile:
python3 genDict.py offDoms/extracted-TLDs.txt files/DAT/ files/dictFile.json

# 2. Retrieve Data (whois, priority and test_freq, ip, mx, http(s) requests)
#    continuously:
bash continuum-retrieveData.sh files/dictFile.json

# 3. When log-files/$dictFile/output$i.json is ready, run this to insert into ElasticSearch:
#python3 insertES.py log-files/$dictFile/output$i.json elasticSearchIndex
