#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 19/07/2018
#version: 0.2 (based on retrieveData.py v0.4)
# the same as retrieveData.py, but making requests like crazy
#
#recommended execution: /usr/bin/time -o time.txt python3 retrieveData.py dictFile.json outputFile.json >> logFile.log

#TO-DO LIST (18/07/2018)
#TODO: try-except to control when we are blocked

import argparse
from datetime import date, timedelta, datetime
from time import time
import whois
import dns.resolver
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import socket
import json
from retrieveData import check_whois, get_ip, get_mx, check_web
from multiprocessing import Pool

class Domain:
	def __init__(self):
		self.status = 'not resolving'
		self.owner = ''
		self.reg_date = convertDatetime(datetime.now())
		self.owner_change = convertDatetime(datetime.now())
		self.creation_date = convertDatetime(datetime.now())
		self.ip = []
		self.mx = []
		self.web = [] # http reqs
		self.webs = [] # https reqs
		self.domain = ''
		self.subdomains = ''
		self.test_freq = ''
		self.generation = ''
		self.customer = ''
		self.priority = ''
		self.timestamp = convertDatetime(datetime.now())

def convertDatetime(date):
	if isinstance(date, datetime): #if argument's type is datetime
		return date.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(date, str): #if argument's type is string
		return datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
	else:
		return False

def retrieveDomainsDataFromFile(dictFile):
	results = []
	data = json.load(open(dictFile))
	#data = data[0:2] ## PARA PRUEBA CORTA
	ps = []
	with Pool(processes=30) as pool:
		results = pool.map(check_all,data)
	#reminder: pool.map calls check_all(e), since data = [e0,e1,e2,e3...]
	return results

def check_all(e): #e = {'customer':'TEF','domains':['tef.com','tef.es']}
	res = []
	#e['domains'] = e['domains'][0:5] ## PARA PRUEBA CORTA
	for dom in e['domains']:
		d = Domain()
		d.domain = dom
		d.customer = e['customer']
		start_time = time()
		check_whois(d)
		get_ip(d)
		get_mx(d)
		check_web(d)
		end_time = time()
		print("cust %s - [%i/%i]"%(e['customer'],e['domains'].index(dom)+1,len(e['domains'])),
			"[-]" if d.ip==[] else "[x]",
			"%s"%(d.domain),
			"(%.2f secs)"%(end_time-start_time))
		res.append(d)
	return res

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('dictFile',help='e.g.: dict-37tlds.json')
	parser.add_argument('outputFile',help='e.g.: output-37tlds.json')
	args = parser.parse_args()

	results = retrieveDomainsDataFromFile(args.dictFile)

	# print results as a json (a list of customers. each of these customers is an array of jsons (domains), actually) to outputFile
	with open(args.outputFile,'w') as f:
		print("[",end="",file=f)
		for customer in results:
			print("[",end="",file=f)
			for domain in customer:
				if not customer.index(domain)==len(customer)-1:
					print(json.dumps(domain.__dict__, indent=2, sort_keys=True),end=",\n",file=f)
				else:
					print(json.dumps(domain.__dict__, indent=2, sort_keys=True),end="",file=f)
			if not results.index(customer)==len(results)-1:
				print("],",file=f)
			else:
				print("]",file=f)
		print("]",file=f)
