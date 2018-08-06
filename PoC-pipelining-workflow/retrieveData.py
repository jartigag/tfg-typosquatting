#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.4)
#date: 07/08/2018 (working on PoC, according the Workflow)
#version: 0.4 (based on ts-updater.py)
#given a dictionary of domains, RETRIEVE DATA of whois, ip, mx records, webs for each domain
#and classify it as low/high priority + status info.
#results of each domain are stored in an array of Domain objects with all their collected info.
#
#recommended execution: /usr/bin/time -o time.txt python3 retrieveData.py [-d dictFile.json] [-o outputFile.json] [-v] >> logFile.log

#TO-DO LIST for v0.5 (07/08/2018)
# - use DomainThread to parallel processing requests

import argparse
from datetime import date, timedelta, datetime
from time import time
import whois
import dns.resolver
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import socket
import json
from dnstwist import DomainThread
import sys

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
		self.subdomains = '' #TODO
		self.test_freq = ''
		self.generation = '' #TODO
		self.customer = ''
		self.priority = ''
		self.timestamp = convertDatetime(datetime.now())
		self.resolve_time = '' #TODO

def convertDatetime(date):
	if isinstance(date, datetime): #if argument's type is datetime
		return date.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(date, str): #if argument's type is string
		return datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
	else:
		return False

def retrieveDomainsDataFromFile(dictFile,verbose):
	results = []
	data = json.load(open(dictFile))
	#data = data[0:1] ## PARA PRUEBA CORTA
	for e in data:
		for dom in e['domains']:
			d = Domain()
			d.domain = dom
			d.customer = e['customer']

			start_time = time()
			check_whois(d)
			get_ip(d)
			get_mx(d)
			check_web(d)
			#check_subomains(d)
			end_time = time()

			if verbose:
				print("cust%i - [%i/%i]"%(data.index(e)+1,e['domains'].index(dom)+1,len(e['domains'])),
					"[-]" if d.ip==[] else "[x]",
					"%s %s"%(d.customer,d.domain),
					"(%.2f secs)"%(end_time-start_time))

			results.append(d)

	return results

def check_whois(d):
	# CHECK WHOIS
	try:
		w = whois.query(d.domain)
		d.status = 'resolving' #FIXME: 2596 status (52,2%) stay as 'resolving', instead of 'to be verified' or 'parked'
		d.owner = w.name
		d.reg_date = convertDatetime(w.last_updated)
		d.owner_change = convertDatetime(w.last_updated)
		d.creation_date = convertDatetime(w.creation_date)
		# ASSIGN PRIORITY
		#domain resolves:
		if convertDatetime(d.reg_date)==False:
			pass #to discard wrong reg_dates
		elif convertDatetime(d.reg_date)+timedelta(days=7) < datetime.now():
			#registered less than 1 week ago:
			d.priority = 'high'
			d.status = 'to be verified'
		else:
			#registered more than 1 week ago:
			d.priority = 'low'
			d.status = 'parked'
	except:
		#TODO: sometimes it fails because whois parses the result wrongly
		#(ej: "ValueError: Unknown date format: 'registrar: the registrar, s.l.u'")
		#domain doesn't resolve:
		if datetime.now()-timedelta(seconds=200) <= convertDatetime(d.reg_date):
			#not registered (because reg_date is now, with a margin of 200 secs):
			d.priority = 'low'
			d.status = 'very low priority'
		elif convertDatetime(d.reg_date) > datetime.now()-timedelta(days=7):
			#registered less than 1 week ago:
			d.priority = 'high'
			d.status = 'very suspicious'
		else:
			#registered more than 1 week ago:
			d.priority = 'high'
			d.status = 'suspicious'
	# ASSIGN TEST_FREQ
	if d.priority=='high':
		d.test_freq = '1'
	elif d.priority=='low':
		d.test_freq = '14'

def get_ip(d):
	# GET IP
	try:
		d.ip.append(str(socket.gethostbyname(d.domain)))
	except:
		pass

def get_mx(d):
	# GET MX RECORDS
	try:
		ans = dns.resolver.query(d.domain, 'MX')
		for rdata in sorted(ans):
			d.mx.append(str(rdata.exchange))
	except:
		pass

def check_web(d):
	# CHECK WEB
	try:
		requests.get('http://' + dom)
		d.web.append(True)
	except:
		d.web.append(False)
	try:
		# in order to ignore "InsecureRequestWarning: Unverified HTTPS request is being made.":
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		requests.get('https://' + dom, verify=False)
		d.webs.append(True)
	except:
		d.webs.append(False)

def check_subdomains(d):
	# CHECK SUBDOMAINS
	'''
	#TODO: (fase2) generate subdomains with dnstwist:
	subdoms = []
	n=0
	for do in res:
		d = DomainFuzz(do)
		d.generate()
		for m in d.domains:
			if 'Subdomain' in m['fuzzer']:
				subdoms.append(m['domain-name'])
				n+=1
	if verbose:
		print("%i subdomains)" % (n))
	for s in subdoms:
		res.append(s)
	for sub in subdomains:
		try:
			requests.get('http://' + sub)
			web_bool = 'True'
		except:
			web_bool = 'False'
		web_array.append(web_bool)
	'''

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-d','--dictFile',help='e.g.: dict-37tlds.json')
	parser.add_argument('-o','--outputFile',help='e.g.: output-37tlds.json')
	parser.add_argument('-v','--verbose',action='store_true')
	args = parser.parse_args()

	if args.dictFile:
		results = retrieveDomainsDataFromFile(args.dictFile,args.verbose)
	else:
		for line in sys.stdin:
			domain=line.split()[1]
			# GET IP (just for PoC)
			try:
				print(domain,"-->",str(socket.gethostbyname(domain)))
			except:
				print(domain,"--> no ip")

	# print results as a json (an array of jsons, actually) to outputFile
	if args.outputFile:
		with open(args.outputFile,'w') as f:
			print(json.dumps(results,indent=2,sort_keys=True),file=f)
