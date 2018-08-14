#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#date: 14/08/2018
#version: 0.3 (keeps cust_code. doc.id=cust_code)
#INSERT data from a file into ELASTICSEARCH
#
#usage: insertES.py dataFile.json elasticSearchIndex

import json
from elasticsearch import Elasticsearch
import argparse

es = Elasticsearch(['http://localhost:9200'])

def insertES(data,index):
	es.indices.create(index=index,ignore=400)
	body = str({'doc':data}).replace( "'",'"')
	es.index(index=index, doc_type='string', body=body, id=data['customer'])

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('dataFile')
	parser.add_argument('elasticSearchIndex')
	args = parser.parse_args()

	data = json.load(open(args.dataFile))
	index = args.elasticSearchIndex
	insertES(data,index)
