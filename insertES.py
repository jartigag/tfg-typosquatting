#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.5)
#date: 16/08/2018
#version: 0.5 (insertESBulk really working)
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
	es.index(index=index, doc_type='domain', body=body)

def insertESBulk(documents,index):
	# (copied from a @julgoor chunk of code)
	# Split the data into smaller parts
	parts = []
	length = 100
	if len(documents) > length:
		begin = 0
		while begin < len(documents):
			parts.append( documents[begin:begin+length] )
			begin += length
	else:
		parts = [ documents ]

	# Work with each part per separate
	failed_documents = []
	for part in parts:

		# Prepare the data
		bulk_data = []
		for doc in part:

			data_dict = doc

			op_dict = {
				"index": {
					"_index": index,
					"_type": 'domain'
				}
			}

			bulk_data.append(op_dict)
			bulk_data.append(data_dict)
	try:
		es.indices.create(index=index,ignore=400)
		es.bulk (index=index, body=bulk_data, refresh=True)
	except Exception as e:
		print("ElasticSearch ERROR:",e)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('dataFile')
	parser.add_argument('elasticSearchIndex')
	args = parser.parse_args()

	data = json.load(open(args.dataFile))
	index = args.elasticSearchIndex
	insertES(data,index)
