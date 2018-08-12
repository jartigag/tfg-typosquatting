#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#date: 12/08/2018
#version: 0.3 (includes --elastic storage)
#GENerate a DICTionary of DOMAINS and its TYPOsquatting variations
#from a list of Official Domains and a list of TLDs
#
#usage: genTypoDict.py [-o outputDictFile] [-p | -v] tldsJSONFile domainsDirectory

import argparse
import os
import json
from dnstwist import DomainFuzz
from elasticsearch import Elasticsearch
from insertES import insertES

def genDict(tldsFile,domainsDir,outputDictFile,verbose,pipelining,elasticIndex):
	if outputDictFile:
		outputDictF=open(outputDictFile,'w')
		print("[",end="",file=outputDictF)
	doms = []
	tlds = json.load(open(tldsFile))

	for file in os.listdir(domainsDir):
		with open(domainsDir+file) as f:
			doms.append(f.read().splitlines())

	i=0
	ndoms=0
	ncombs=0
	totalnvars=0
	#for c in os.listdir(domainsDir)[0:1]: ## PARA PRUEBA CORTA
	for c in os.listdir(domainsDir):
		combs = [] # # array with domains combinations for a client
		cust_code = c.split('_-_')[0] # customer code
		i+=1

		ds=doms[i-1]
		for url in ds:
			u = url.rsplit('.',1)[0].lower() # name of the domain
			#generate combinations with the name and the tlds:
			for tld in tlds:
				combs.append(u+tld)

		combs = list(set(combs)) # REMOVE DUPlicates in combs

		nvars=0
		for c in combs:
			fuzzed_doms = [] # array with all variations for a domain
			dfuzz = DomainFuzz(c)
			dfuzz.generate()
			fuzzed_doms = dfuzz.domains
			nvars+=len(fuzzed_doms)

			e = {} # element (type: dictionary) to append in result array
			e['customer'] = cust_code
			e['domains'] = fuzzed_doms

			if pipelining:
				for d in fuzzed_doms:
					print(cust_code,d)
			elif elasticIndex:
				insertES(fuzzed_doms,elasticIndex)
				print(cust_code,fuzzed_doms[0]['domain-name'])
			elif outputDictFile:
				# print results as a json to outputDictF:
				print(json.dumps(e,sort_keys=True),end=",\n",file=outputDictF)
				#TODO: avoid to remove last "," manually

		if verbose:
			print("%i - %s 	%i doms (%i combs, %i vars)" % (i,cust_code,len(ds),len(ds)*len(tlds),nvars))

		ndoms+=len(ds)
		ncombs+=len(ds)*len(tlds)
		totalnvars+=nvars

	if verbose:
		print("TOTAL domains:",ndoms)
		print("TOTAL combinations: %i (%i with duplicates)"%(len(combs),ncombs))
		print("TOTAL variations (possible duplicates):",totalnvars)

	if outputDictFile:
		print("]",file=outputDictF)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	onlyOneGroup = parser.add_mutually_exclusive_group()
	parser.add_argument('tldsJSONFile',help='e.g.: ccTLDS.json')
	parser.add_argument('domainsDirectory',help='e.g.: files/DAT/')
	parser.add_argument('-o','--outputDictFile',help='e.g.: dict-37tlds.json')
	onlyOneGroup.add_argument('-e','--elastic',metavar='INDEX',help='store results in ElasticSearch database')
	onlyOneGroup.add_argument('-p','--pipelining',action='store_true',help='print each result in stdout')
	onlyOneGroup.add_argument('-v','--verbose',action='store_true',help='print how many combinations there are')
	args = parser.parse_args()

	if args.elastic:
		es = Elasticsearch(['http://localhost:9200'])

	genDict(args.tldsJSONFile,args.domainsDirectory,args.outputDictFile,args.verbose,args.pipelining,args.elastic)
