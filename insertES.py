#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.4)
#date: 14/08/2018
#version: 0.4 (insertESBulk added)
#INSERT data from a file into ELASTICSEARCH
#
#usage: insertES.py dataFile.json elasticSearchIndex

import json
from elasticsearch import Elasticsearch, helpers
import argparse

es = Elasticsearch(['http://localhost:9200'])

def insertES(data,index):
	es.indices.create(index=index,ignore=400)
	body = str(data).replace( "'",'"')
	es.index(index=index, doc_type='string', body=body)

def insertESBulk(data,index):
	es.indices.create(index=index,ignore=400)
	actions = [
		{
			"_index": index,
			"_type": "domains",
			"_id": i,
			"_source": str(data).replace( "'",'"')
		}
		for i in range(len(data))
	]
	helpers.bulk(es, actions)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('dataFile')
	parser.add_argument('elasticSearchIndex')
	args = parser.parse_args()

	data = json.load(open(args.dataFile))
	index = args.elasticSearchIndex
	insertES(data,index)
