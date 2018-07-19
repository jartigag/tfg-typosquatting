#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo
#date: 21/06/2018
#version: 0.1
# extract ccTLDs from .dat files (which contain official domains)

import os
import subprocess
import json

files = []
doms = []
tlds = []

for f in os.listdir(os.getcwd()+'/DAT'):
	files.append(f)
for file in files:
	with open('DAT/'+file) as f:
		doms.append(f.read().splitlines())

# now all domains are in separated lists inside doms (which is also a list)

# SANITIZE DOMAINS:
for d in doms:
	for u in d:
		if '/' in u:
			print("error:",u,"in",files[doms.index(d)])
			u = u.split('/',1)[0] # discard path behind /
		if '.com.' in u or '.org.' in u or '.co.' in u or '.nom.' in u: #TODO: generalize this condition
			tlds.append('.'+u.rsplit('.',2)[1].lower()+'.'+u.rsplit('.',2)[2].lower())
		else:
			try:
				tlds.append('.'+u.rsplit('.',1)[1].lower())
			except Exception as e:
				# find queries that aren't domains
				print("error:",u,"in",files[doms.index(d)])

# once errors in .dat files has been found and removed,
# REMOVE DUPlicates in tlds and SORT alphabetically:
tlds = sorted(list(set(tlds)))

# get the ccTLDs in obtained tlds:
result = []
ccTlds = json.load(open('all-cc-TLDs.txt'))
for t in tlds:
	for c in ccTlds:
		if c==t:
			result.append(t)

print(result)
