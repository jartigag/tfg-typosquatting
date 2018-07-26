#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 17/07/2018
#version: 0.1
# GENerate 2 DICTionaries from a log: fast-dict and slow-dict

#usage: gen2Dicts.py [-v] logFile outputDictFile (-v mainly to debug, significantly faster without it)

import argparse
import json

def genDict(logFile,verbose):
	file = open(logFile).readlines()
	resFast = [] # array with all fast domains for all clients
	resSlow = [] # array with all slow domains for all clients

	# initialize results arrays:
	for i in range(0,50+1): #50 customers
		resFast.append({'customer':'','domains':[]})
		resSlow.append({'customer':'','domains':[]})

	for l in file:
		secs = int(l.split()[6].split('.')[0][1:])
		if file.index(l)%10000==0:  #DEBUGGING (to check if all domains are processed)
			if verbose:
				print('[*]',file.index(l))
				c=0
				for r in resFast:
					c+=len(r['domains'])
				print("by now, fast domains:",c)
				c=0
				for r in resSlow:
					c+=len(r['domains'])
				print("by now, slow domains:",c)
		if secs>=10: # criteria for classify as slow or fast
			e = {}
			e['customer'] = l.split()[4]
			e['domain'] = l.split()[5]
			for i in range(0,len(resSlow)-1):
				if resSlow[i]['customer']==e['customer']:
					#add actual domain to existing customer's domains list:
					resSlow[i]['domains'].append(e['domain'])
					break
				elif resSlow[i]['customer']=='':
					#add actual domain to this empty domains list:
					resSlow[i]['domains'].append(e['domain'])
					#and label as actual customer's domains list:
					resSlow[i]['customer'] = e['customer']
					break
		else:
			e = {}
			e['customer'] = l.split()[4]
			e['domain'] = l.split()[5]
			for i in range(0,len(resFast)-1):
				if resFast[i]['customer']==e['customer']:
					#add actual domain to existing customer's domains list:
					resFast[i]['domains'].append(e['domain'])
					break
				elif resFast[i]['customer']=='':
					#add actual domain to this empty domains list:
					resFast[i]['domains'].append(e['domain'])
					#and label the list as actual customer's domains list:
					resFast[i]['customer'] = e['customer']
					break
	if verbose:
		c=0
		for r in resFast:
			c+=len(r['domains'])
		print("TOTAL FAST DOMAINS:",c)
		c=0
		for r in resSlow:
			c+=len(r['domains'])
		print("TOTAL SLOW DOMAINS:",c)

	return resFast,resSlow

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('logFile',help='e.g.: log1.log')
	parser.add_argument('outputDictFile',help='e.g.: dictFromLog.json')
	parser.add_argument('-v','--verbose',action='store_true')
	args = parser.parse_args()

	fastRes,slowRes = genDict(args.logFile,args.verbose)

	# print fastRes as a json to fastDictFile
	with open('fast-'+args.outputDictFile,'w') as f:
		print("[",end="",file=f)
		for r in fastRes:
			if r['customer']!='':
				if fastRes[fastRes.index(r)+1]['customer']=='':
					print(json.dumps(r, indent=2, sort_keys=True),end="",file=f)
				else:
					print(json.dumps(r, indent=2, sort_keys=True),end=",\n",file=f)
		print("]",file=f)

	# print slowRes as a json to slowDictFile
	with open('slow-'+args.outputDictFile,'w') as f:
		print("[",end="",file=f)
		for r in slowRes:
			if r['customer']!='':
				if slowRes[slowRes.index(r)+1]['customer']=='':
					print(json.dumps(r, indent=2, sort_keys=True),end="",file=f)
				else:
					print(json.dumps(r, indent=2, sort_keys=True),end=",\n",file=f)
		print("]",file=f)
