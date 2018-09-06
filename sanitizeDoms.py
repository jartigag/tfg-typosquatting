#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo
#date: 24/08/2018
#version: 1.0
# remove invalid domains and duplicates 
# from the official domains .csv files and dump results

#usage: sanitizeDoms.py directory

import argparse
import os
from dnstwist import UrlParser

files = []
doms = []
initial_ndoms = 0
final_ndoms = 0

def load_files(directory):
	global initial_ndoms
	for f in os.listdir(os.getcwd()+'/'+directory):
		files.append(f)
	for file in files:
		with open(directory+file) as f:
			newdoms = f.read().splitlines()
			initial_ndoms += len(newdoms)
			doms.append(newdoms)

def check_dups():
	for customer_doms in doms:
		pos = doms.index(customer_doms)
		for other_customer_doms in doms[pos+1:]:
			other_pos = doms.index(other_customer_doms)
			if set(customer_doms) & set(other_customer_doms):
				print("\033[1mduplicated domain(s)\033[0m:\n%s <-> %s" % 
          (files[pos],files[other_pos]))
        # print domains in common:
				print(set(customer_doms) & set(other_customer_doms),'\n') 
				# remove dups from last other customer's doms:
        doms[other_pos] = \
        list( set(doms[other_pos]).difference(customer_doms) )

def check_invalids():
	global final_ndoms
	print("\033[1minvalid domain(s)\033[0m:")
	for customer_doms in doms:
		pos = doms.index(customer_doms)
    #flag to know if a linebreak at the end of the costumer must be printed:
		someInvalid = False
		for d in customer_doms:
			d_pos = customer_doms.index(d)
			try:
				decoded_d = d.encode('idna').decode('idna')
				UrlParser(decoded_d)
			except ValueError as err:
				if someInvalid==False:
					print(files[pos],end=": ")
				print('%s (%i)' % (decoded_d,d_pos),end=", ")
				someInvalid = True
				del doms[pos][d_pos]
			if someInvalid and d_pos==len(customer_doms)-1: print()
		final_ndoms += len(customer_doms)

def dump_data():
	for customer_doms in doms:
		pos = doms.index(customer_doms)
		f = open(files[pos].replace('.csv','.dat'),'w+')
		print(customer_doms,file=f)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('directory',help='e.g.: STAGE1/offDoms/csv/')
	args = parser.parse_args()

	load_files(args.directory)
	print(">> \033[1m%s\033[0m domains (before checking duplicates \
    and invalids):\n"%(initial_ndoms))
	check_dups()
	check_invalids()
	print("\n\n>> \033[1m%s\033[0m domains (after checking):"%(final_ndoms),
    "(%i less)\n"%(initial_ndoms-final_ndoms))
	dump_data()
