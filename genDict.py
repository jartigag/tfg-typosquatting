#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#author: Aruna Prem Bianzino (v0.1, typosquattinggeneration.py)
#date: 22/06/2018
#version: 0.3
#GENerate a DICTionary of DOMAINS from a list of Official Domains and a list of ccTLDs

import os
import subprocess
import json

files = []
doms = []
tlds = json.load(open('originalTLDs.dat'))
res = []

for f in os.listdir(os.getcwd()+'/DAT'):
	files.append(f)
for file in files:
	with open('DAT/'+file) as f:
		doms.append(f.read().splitlines())

i=0

for customer in files:
	i+=1
	#print("customer %i: %s" % (i,customer))
	for d in doms:
		#print("		%i official domains: %s" % (len(d),d))
		for url in d:
			u = url.rsplit('.',1)[0].lower()
			#generate combinations
			for tld in tlds:
				res.append(u+tld)
				'''
				#sort and save combinations in file
				command = 'cat temp.aux | grep -v "xn--" | sort -u >> "combs-' + customer + '.txt"'
				os.system(command)
				'''
# REMOVE DUPlicates in res and SORT alphabetically:				
res = sorted(list(set(res)))
for r in res:
	print(r)
