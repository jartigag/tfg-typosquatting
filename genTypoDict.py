#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 27/07/2018
#version: 0.2 (allows technics choice)
# GENerate a DICTionary of DOMAINS from a list of Official Domains and a list of ccTLDs,
# including TYPOsquatting variations

#usage: genTypoDict.py [-v] tldsJSONFile domainsDirectory outputDictFile

#TODO: add stats
#TODO: REMOVE DUPlicates in res

import argparse
import os
import json
from dnstwist import DomainFuzz, generate_json

def genDict(tldsFile,domainsDir,verbose,technics):
	files = []
	doms = []
	result = [] # array with all domains for all clients, as ["customer":cust_code,"domains":res]
	tlds = json.load(open(tldsFile))

	for f in os.listdir(domainsDir):
		files.append(f)
	for file in files:
		with open(domainsDir+file) as f:
			doms.append(f.read().splitlines())

	i=0
	ndoms=0
	ncombs=0
	nvars=0
	for c in files:
		res = [] # array with domains combinations for a client
		e = {} # element (type: dictionary) to append in result array
		cust_code = c.split('_-_')[0] # customer code
		i+=1
		d=doms[i-1]
		if verbose:
			print("%i - %s 	%i doms (%i combs using %i tlds)" % (i,cust_code,len(d),len(d)*len(tlds),len(tlds)),end="")
		ndoms+=len(d)
		for url in d:
			domWithTLDs = []
			u = url.rsplit('.',1)[0].lower() # name of the domain
			#generate combinations with the name and the tlds:
			for tld in tlds:
				domWithTLDs.append(u+tld)
			for domain in domWithTLDs:
				dfuzz = DomainFuzz(domain)
				dfuzz.generate_originals()
				if args.technics=='addition':
					dfuzz.generate_addition()
				if args.technics=='bitsquatting':
					dfuzz.generate_bitsquatting()
				if args.technics=='homoglyph':
					dfuzz.generate_homoglyph()
				if args.technics=='hyphenation':
					dfuzz.generate_hyphenation()
				if args.technics=='insertion':
					dfuzz.generate_insertion()
				if args.technics=='omission':
					dfuzz.generate_omission()
				if args.technics=='repetition':
					dfuzz.generate_repetition()
				if args.technics=='replacement':
					dfuzz.generate_replacement()
				if args.technics=='subdomains':
					dfuzz.generate_subdomains()
				if args.technics=='transposition':
					dfuzz.generate_transposition()
				if args.technics=='vowelswap':
					dfuzz.generate_vowelswap()
				res.append(dfuzz.domains)
				nvars += len(dfuzz.domains)
		if verbose:
			print(" - %i variations in total"%(len(dfuzz.domains)*len(res)))
		#res = list(set(res)) #TODO: REMOVE DUPlicates in res
		e['customer'] = cust_code
		e['domains'] = res
		result.append(e)

	if verbose:
		print("TOTAL domains:",ndoms)
		print("TOTAL combinations: %i (using %i tlds)"%(ndoms*len(tlds),len(tlds)))
		print("TOTAL variations:",nvars)
		# print("removing duplicates")
		# c=0
		# for r in result:
		# 	c+=len(r['domains'])
		#print("TOTAL COMBINATIONS:",c,"(%i duplicates domains removed)"%(ndoms*len(tlds)-c))

	return result

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('tldsJSONFile',help='e.g.: files/tlds-44-all.json')
	parser.add_argument('domainsDirectory',help='e.g.: files/DAT/')
	parser.add_argument('outputDictFile',help='e.g.: dict-44tlds.json')
	parser.add_argument('-v','--verbose',action='store_true')
	parser.add_argument('-t', '--technics', type=str,
		choices=['addition','bitsquatting', 'homoglyph', 'hyphenation', 'insertion', 'omission', 'repetition', 'replacement', 'subdomains', 'transposition', 'vowelswap'],
		default=['addition','bitsquatting', 'homoglyph', 'hyphenation', 'insertion', 'omission', 'repetition', 'replacement', 'subdomains', 'transposition', 'vowelswap'],
		help='typosquatting technics included (default: all)')
	args = parser.parse_args()

	results = genDict(args.tldsJSONFile,args.domainsDirectory,args.verbose,args.technics)

	# print results as a json to outputDictFile
	with open(args.outputDictFile,'w') as f:
		print(json.dumps(results,indent=2,sort_keys=True),file=f)
