#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 28/07/2018
#version: 0.1
#generate a txt with all combinations of offDoms+TLDs

#usage: aux-mergeAllOffDoms.py tldsJSONFile domainsDirectory outputFile

import argparse
import os
import json

def genCombs(tldsFile,domainsDir):
	files = []
	doms = []
	result = []
	tlds = json.load(open(tldsFile))

	for f in os.listdir(domainsDir):
		files.append(f)
	for file in files:
		with open(domainsDir+file) as f:
			doms.append(f.read().splitlines())
	i=0
	for c in files:
		res = []
		for url in doms[i]:
			u = url.rsplit('.',1)[0].lower() # name of the domain
			#generate combinations with the name and the tlds:
			for tld in tlds:
				res.append(u+tld)
		res = list(set(res)) # REMOVE DUPlicates in res
		result.extend(res)
		i+=1
	return result

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('tldsJSONFile',help='e.g.: files/tlds-44.json')
	parser.add_argument('domainsDirectory',help='e.g.: files/DAT/')
	parser.add_argument('outputFile',help='e.g.: merge-doms.txt')
	args = parser.parse_args()

	results = genCombs(args.tldsJSONFile,args.domainsDirectory)

	# print results as a txt to outputFile
	with open(args.outputFile,'w') as f:
		for r in results:
			print(r,file=f)
