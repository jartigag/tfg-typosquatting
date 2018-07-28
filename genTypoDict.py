#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#date: 28/07/2018
#version: 0.3 (registered stats)
# GENerate a DICTionary of DOMAINS from a list of Official Domains and a list of ccTLDs,
# including TYPOsquatting variations

#usage: genTypoDict.py [-v] tldsJSONFile domainsDirectory outputDictFile [-t technic1 technic2]

#TODO: REMOVE DUPlicates in res
#TODO?: adapt generate_json to create a dict of registered domains only

import argparse
import os
import json
from dnstwist import DomainFuzz, DomainThread, generate_json
import queue
import time

def genDict(tldsFile,domainsDir,verbose,technics):
	files = []
	doms = []
	result = [] # array with all domains for all clients, as ["customer":cust_code,"domains":res]
	registered = [] # array with all registered domains for all clients, as ["customer":cust_code,"domains":reg]
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
		reg = [] # array with registered domains for a client
		e = {} # element (type: dictionary) to append in result array
		r = {} # element (type: dictionary) to append in registered array
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
				if 'addition'in args.technics:
					dfuzz.generate_addition()
				if 'bitsquatting'in args.technics:
					dfuzz.generate_bitsquatting()
				if 'homoglyph'in args.technics:
					dfuzz.generate_homoglyph()
				if 'hyphenation'in args.technics:
					dfuzz.generate_hyphenation()
				if 'insertion'in args.technics:
					dfuzz.generate_insertion()
				if 'omission'in args.technics:
					dfuzz.generate_omission()
				if 'repetition'in args.technics:
					dfuzz.generate_repetition()
				if 'replacement'in args.technics:
					dfuzz.generate_replacement()
				if 'subdomains'in args.technics:
					dfuzz.generate_subdomains()
				if 'transposition'in args.technics:
					dfuzz.generate_transposition()
				if 'vowelswap'in args.technics:
					dfuzz.generate_vowelswap()
				res.extend(dfuzz.domains)
				nvars += len(dfuzz.domains)
				#the same as result, but with registered domains:
				reg.extend(procRegs(dfuzz.domains))
		if verbose:
			print(" - %i variations in total	"%(len(res)),end="")
			hits_total = len(reg)
			hits_percent = 100 * hits_total / len(res)
			print(' %d hits (%d%%)' % (hits_total, hits_percent))
		#res = list(set(res)) #TODO: REMOVE DUPlicates in res
		e['customer'] = cust_code
		e['domains'] = res
		result.append(e)
		r['customer'] = cust_code
		r['domains'] = reg
		registered.append(r)

	if verbose:
		print("TOTAL official domains:",ndoms)
		print("TOTAL combinations: %i (using %i tlds)"%(ndoms*len(tlds),len(tlds)))
		print("TOTAL variations:",nvars,"(x%.2f domain combinations)"%(nvars/(ndoms*len(tlds))))
		# print("removing duplicates")
		# c=0
		# for r in result:
		# 	c+=len(r['domains'])
		#print("TOTAL COMBINATIONS:",c,"(%i duplicates domains removed)"%(ndoms*len(tlds)-c))

	return result

def procRegs(domains):
	regCustomer = []
	jobs = queue.Queue()
	global threads
	threads = []
	for i in range(len(domains)):
		jobs.put(domains[i])
	for i in range(4): #param: 4 threads
		worker = DomainThread(jobs)
		worker.setDaemon(True)
		worker.option_whois = True
		worker.start()
		threads.append(worker)
	while not jobs.empty():
		time.sleep(10**-9) #to prevent "RuntimeError: can't start new thread" or "Too much open files"
	for worker in threads:
		worker.stop()
	for d in domains:
		if 'dns-ns' in d or 'dns-a' in d:
			r = {}
			r['fuzzer'] = d['fuzzer']
			r['domain-name'] = d['domain-name']
			regCustomer.append(r)
	return regCustomer

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('tldsJSONFile',help='e.g.: files/tlds-44.json')
	parser.add_argument('domainsDirectory',help='e.g.: files/DAT/')
	parser.add_argument('outputDictFile',help='e.g.: dict-44tlds.json')
	parser.add_argument('-v','--verbose',action='store_true')
	parser.add_argument('-t', '--technics', type=str, nargs='+',
		choices=['addition','bitsquatting', 'homoglyph', 'hyphenation', 'insertion', 'omission', 'repetition', 'replacement', 'subdomains', 'transposition', 'vowelswap'],
		default=['addition','bitsquatting', 'homoglyph', 'hyphenation', 'insertion', 'omission', 'repetition', 'replacement', 'subdomains', 'transposition', 'vowelswap'],
		help='typosquatting technics included (default: all)')
	args = parser.parse_args()

	results = genDict(args.tldsJSONFile,args.domainsDirectory,args.verbose,args.technics)

	# print results as a json to outputDictFile
	with open(args.outputDictFile,'w') as f:
		print(json.dumps(results,indent=2,sort_keys=True),file=f)
