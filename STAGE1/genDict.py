#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.4)
#author: Aruna Prem Bianzino (v0.1, typosquattinggeneration.py)
#date: 03/07/2018
#version: 0.4 (it accepts arguments)
#GENerate a DICTionary of DOMAINS
# from a list of Official Domains and a list of ccTLDs

#usage: genDict.py [-v] tldsJSONFile domainsDirectory outputDictFile

import argparse
import os
import json

def genDict(tldsFile,domainsDir,verbose):
	files = []
	doms = []
	result = [] # array with all domains for all clients,
				# as ["customer":cust_code,"domains":res]
	tlds = json.load(open(tldsFile))

	for f in os.listdir(domainsDir):
		files.append(f)
	for file in files:
		with open(domainsDir+file) as f:
			doms.append(f.read().splitlines())

	i=0
	ndoms=0
	ncombs=0
	for c in files:
		res = [] # array with domains combinations for a client
		e = {} # element (type: dictionary) to append in result array
		cust_code = c.split('_-_')[0] # customer code
		i+=1
		d=doms[i-1]
		if verbose:
			print("%i - %s 	%i doms (%i combs)" %
				(i,cust_code,len(d),len(d)*len(tlds)))
		ndoms+=len(d)
		ncombs+=len(d)*len(tlds)
		for url in d:
			u = url.rsplit('.',1)[0].lower() # name of the domain
			#generate combinations with the name and the tlds:
			for tld in tlds:
				res.append(u+tld)
		res = list(set(res)) # REMOVE DUPlicates in res
		e['customer'] = cust_code
		e['domains'] = res
		result.append(e)

	if verbose:
		print("TOTAL domains:",ndoms)
		print("TOTAL combinations (with duplicates):",ncombs)
		print("removing duplicated domains...")
		c=0
		for r in result:
			c+=len(r['domains'])
		print("TOTAL COMBINATIONS:",c,
			"(%i duplicates removed)"%(ncombs-c))

	return result

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('tldsJSONFile',help='e.g.: ccTLDS.json')
	parser.add_argument('domainsDirectory',help='e.g.: files/DAT/')
	parser.add_argument('outputDictFile',help='e.g.: dict-37tlds.json')
	parser.add_argument('-v','--verbose',action='store_true')
	args = parser.parse_args()

	results = genDict(args.tldsJSONFile,args.domainsDirectory,args.verbose)

	# print results as a json to outputDictFile
	with open(args.outputDictFile,'w') as f:
		print("[",end="",file=f)
		for r in results:
			if not results.index(r)==len(results)-1:
				print(json.dumps(r, indent=2, sort_keys=True),
					end=",\n",file=f)
			else:
				print(json.dumps(r, indent=2, sort_keys=True),
					end="",file=f)
		print("]",file=f)
