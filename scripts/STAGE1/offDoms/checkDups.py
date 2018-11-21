#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

files = []
doms = []
for f in os.listdir(os.getcwd()+'/csv'):
	files.append(f)
for file in files:
	with open('csv/'+file) as f:
		doms.append(f.read().splitlines())

for d in doms:
	pos = doms.index(d)
	for i in range(pos+1,len(doms)):
		if set(d) & set(doms[i]):
			print("duplicated domain(s) in %s and %s" % (files[pos],files[i]))
			print(set(d) & set(doms[i]),'\n')
