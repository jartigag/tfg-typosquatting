#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 12/08/2018
#version: 0.2 (adapted to dnstwist.DomainFuzz format)
#INSERT data from a file into ELASTICSEARCH
#
#usage: insertES.py dataFile.json elasticSearchIndex

import json
from elasticsearch import Elasticsearch
import argparse

es = Elasticsearch(['http://localhost:9200'])

def insertES(data,index):
	es.indices.create(index=index,ignore=400)
	for d in data: #TODO: revisar estos dos bucles
		body = '{"doc": {'
		l = list(d)
		for i in l:
			if not l.index(i)==len(l)-1:
				body+='"'+i+'":"'+str(d[i])+'",'
			else:
				body+='"'+i+'":"'+str(d[i])+'"}}'
		es.index(index=index, doc_type='string', body=body, id=d['domain-name'])

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('dataFile')
	parser.add_argument('elasticSearchIndex')
	args = parser.parse_args()

	data = json.load(open(args.dataFile))
	index = args.elasticSearchIndex
	insertES(data,index)
