#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo
#date: 11/08/2018
#version: 0.1
# remove invalid domains and duplicates from the official domains .xls files and dump results

#usage: sanitizeDoms.py directory

import argparse
import os

files = []
doms = []

def load_files(directory):
	for f in os.listdir(os.getcwd()+'/'+directory):
		files.append(f)
	for file in files:
		with open(directory+file) as f:
			doms.append(f.read().splitlines())

def check_dups():
	for d in doms:
		pos = doms.index(d)
		for i in range(pos+1,len(doms)):
			if set(d) & set(doms[i]):
				print("duplicated domain(s)\n%s <-> %s" % (files[pos],files[i]))
				print(set(d) & set(doms[i]),'\n')

def check_invalids():
	#TODO
	pass

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('directory',help='e.g.: STAGE1/offDoms/csv')
	args = parser.parse_args()

	load_files(args.directory)
	check_dups()
	#check_invalids()

#duplicated domains has been removed from .dat files 
# (IBER_-_IBER_COR_-_Dominios.dat)
#
#invalid domains has been removed from .dat files
# (VIVO,MERC,AMA,MAFH,DGP,TEF_ES_-_Domains.dat)
#
#duplicates has been removed from .dat files
# (TEF_CORP,TEF_XX-_-Domains)
