#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.8)
#date: 03/10/2018
#version: 0.8 (fix: each domain as a ES document)
#INSERT data from a file into ELASTICSEARCH
#
#usage: insertES.py dataFile.json elasticSearchIndex

import json
from elasticsearch import Elasticsearch, helpers
import argparse
import requests

ip = 'localhost'
port = '9200'
es = Elasticsearch('http://{}:{}/'.format(ip,port))

def insertES(data,index):
	mapping = {
	  "mappings":{
	    "domain":{
	      "properties":{
	        "timestamp":{
	          "type":"date",
	          "format":"yyyy-MM-dd hh:mm:ss"
	        },
	        "reg_date":{
	          "type":"date",
	          "format":"yyyy-MM-dd hh:mm:ss"
	        },
	        "owner_change":{
	          "type":"date",
	          "format":"yyyy-MM-dd hh:mm:ss"
	        },
	        "creation_date":{
	          "type":"date",
	          "format":"yyyy-MM-dd hh:mm:ss"
	        }
	      }
	    }
	  }
	}
	es.indices.create(index=index,ignore=400, body=mapping)
	body = str(data).replace( "'",'"')
	es.index(index=index, doc_type='domain', body=body)

def updateES(domain,data,index):
	#first search the domain to get the id:
	body = {"query": {"match": {"domain": {"query": domain}}},"size": 500}
	res = es_search_scroll(index, body)
	#then update the matching doc:
	es.update(index=index, doc_type='domain', 
		id=res['hits']['hits'][0]['_id'], body={"doc": data})

def insertESBulk(documents,index):
	# (from a @julgoor's chunk of code)
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
			op_dict = {"index": {"_index": index,"_type": 'domain'}}
			bulk_data.append(op_dict)
			bulk_data.append(data_dict)

		try:
			es.bulk (index=index, body=bulk_data, refresh=True)
		except Exception as e:
			print("ElasticSearch ERROR:",e)

def getESDocs(index, customer='*', technic='*'):
	# (from a @julgoor's chunk of code)
	### Prepare the query
	#body = {"query": { "match": { "customer":  customer }}, "size": 500}
	body = {"query": {"bool": {"must": [ \
		{ "match": { "customer":  customer }}, \
		{ "match": { "generation": technic }} ] }}, "size": 500}
	# Launch the initial query
	results = es_search_scroll(index, body)
	# Clean the results
	documents = []
	if 'hits' in results and 'hits' in results['hits']:
		while results['hits']['hits']:
			documents.extend(results['hits']['hits'])
			results=es_search_scroll(index,scroll_id=results['_scroll_id'])
	return [ p["_source"] for p in documents ]

def es_search_scroll(index,body=None,scroll_id=None,scroll_duration="1m"):
	# (from a @julgoor's chunk of code)
	'''Launch a query directly to ES'''
	# Prepare the URL and the body depending on the first call or other
	url = ""
	if body and scroll_duration:
		url = 'http://{}:{}/'.format(ip,port) + index + \
			"/_search?scroll=%s" % scroll_duration
	else:
		if scroll_id and scroll_duration:
			url = 'http://{}:{}/'.format(ip,port) + "_search/scroll"
			body = {
				"scroll" : scroll_duration,
				"scroll_id": scroll_id
			}
	# Launch the query and returns the results
	r = requests.post( url, json=body )
	return json.loads( r.text )

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('dataFile')
	parser.add_argument('elasticSearchIndex')
	args = parser.parse_args()

	data = json.load(open(args.dataFile))
	index = args.elasticSearchIndex
	insertESBulk(data,index)
