#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 07/08/2018 (working on PoC, according the Workflow)
#version: 0.1 (based on genDict v0.4. including DomainFuzz and --pipelining)
#GENerate a DICTionary of DOMAINS and its TYPOsquatting variations
#from a list of Official Domains and a list of TLDs

#usage: genTypoDict.py [-o outputDictFile] [-p | -v] tldsJSONFile domainsDirectory

#TODO: review FORs

import argparse
import os
import json
from dnstwist import DomainFuzz

def genDict(tldsFile,domainsDir,verbose, pipelining):
	files = []
	doms = []
	result = [] # array with all domains for all clients, as ["customer":cust_code,"domain":fuzzed_domains]
	tlds = json.load(open(tldsFile))

	for f in os.listdir(domainsDir):
		files.append(f)
	for file in files:
		with open(domainsDir+file) as f:
			doms.append(f.read().splitlines())

	i=0
	ndoms=0
	ncombs=0
	totalnvars=0
	for c in files[0:1]: ## PARA PRUEBA CORTA
	#for c in files:
		combs = [] # # array with domains combinations for a client
		e = {} # element (type: dictionary) to append in result array
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

			e['customer'] = cust_code
			e['domains'] = fuzzed_doms
			result.append(e)

			if pipelining:
				for d in fuzzed_doms:
					print(cust_code,d)

		if verbose:
			print("%i - %s 	%i doms (%i combs, %i vars)" % (i,cust_code,len(ds),len(ds)*len(tlds),nvars))

		ndoms+=len(ds)
		ncombs+=len(ds)*len(tlds)
		totalnvars+=nvars

	if verbose:
		print("TOTAL domains:",ndoms)
		print("TOTAL combinations (with duplicates):",ncombs)
		print("TOTAL variations (possible duplicates:",totalnvars)

	return result

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	onlyOneGroup = parser.add_mutually_exclusive_group()
	parser.add_argument('tldsJSONFile',help='e.g.: ccTLDS.json')
	parser.add_argument('domainsDirectory',help='e.g.: files/DAT/')
	parser.add_argument('-o','--outputDictFile',help='e.g.: dict-37tlds.json')
	onlyOneGroup.add_argument('-p','--pipelining',action='store_true',help='print each result in stdout')
	onlyOneGroup.add_argument('-v','--verbose',action='store_true',help='print how many combinations there are')
	args = parser.parse_args()

	results = genDict(args.tldsJSONFile,args.domainsDirectory,args.verbose,args.pipelining)

	if args.outputDictFile:
		# print results as a json to outputDictFile
		with open(args.outputDictFile,'w') as f:
			print("[",end="",file=f)
			for r in results[:-1]:
				print(json.dumps(r, indent=2, sort_keys=True),end=",\n",file=f)
			print(json.dumps(results[-1], indent=2, sort_keys=True),end="",file=f)
			print("]",file=f)
