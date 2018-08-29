#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.7)
#date: 29/08/2018
#version: 0.7 (all TODOs solved, except the subdomains one)
#given a dictionary of domains (from a file, from elasticsearch or piping it), RETRIEVE DATA of:
#whois, ip, dns/mx records, webs
#for each domain and classify it as low/high priority + status info.
#results of each domain are stored in an array of Domain objects with all their collected info.
#
#recommended execution: /usr/bin/time -o time.txt python3 retrieveData.py custCode [-d dictFile.json | -e GetINDEX] [-o outputFile.json | -i InsertINDEX] [-v] >> logFile.log

#WIP: solve all TODOs for v0.7

import argparse
from datetime import date, timedelta, datetime
from time import time
import dns.resolver
from dns.exception import DNSException
import whois
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import socket
import json
import sys
from elasticsearch import Elasticsearch, helpers
from insertES import insertESBulk, getESDocs
import os

REQUEST_TIMEOUT_DNS = 5

class Domain:
	def __init__(self):
		self.status = 'not resolving'
		self.owner = ''
		self.reg_date = convertDatetime(datetime.now())
		self.owner_change = convertDatetime(datetime.now())
		self.creation_date = convertDatetime(datetime.now())
		self.ip = []
		self.mx = []
		self.ns = []
		self.a = []
		self.aaaa = []
		self.web = [] # http reqs
		self.webs = [] # https reqs
		self.domain = ''
		self.subdomains = ''
		self.test_freq = '0'
		self.generation = ''
		self.customer = ''
		self.priority = ''
		self.timestamp = convertDatetime(datetime.now())
		self.resolve_time = ''

def convertDatetime(date):
	if isinstance(date, datetime): #if argument's type is datetime
		return date.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(date, str): #if argument's type is string
		return datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
	else:
		return False

def retrieveDomainsData(custCode,dictFile,elasticGetIndex,elasticInsertIndex,outputFile,verbose):
	if outputFile:
		outputF=open(outputFile,'w')
		print("[",end="",file=outputF)
	if dictFile:
		data = json.load(open(dictFile))
	elif elasticGetIndex:
		data = getESDocs(elasticGetIndex,custCode)
		if verbose:
			print(custCode,"loaded")
	#data = data[0:1] ## PARA PRUEBA CORTA
	for e in data:
		results = [] # for insertESBulk
		for dom in e['domains']: #e['domains'] contains all the variations of a combination (offDom+TLD)
			d = Domain()
			d.domain = dom['domain-name']
			d.generation = dom['fuzzer']
			d.customer = e['customer']
			start_time = time()
			get_dns(d)#; check_whois(d); get_ip(d); check_web(d); check_subomains(d)
			end_time = time()
			d.resolve_time = resolve_time = "{:.2f}".format(end_time-start_time)

			if verbose:
				print("%s - [%i/%i]"%(custCode,e['domains'].index(dom)+1,len(e['domains'])),
					"[-]" if d.ip==[] else "[x]", d.domain, "(%s secs)"%(d.resolve_time))

			if outputFile:
				# print results as a json to outputF:
				if e['domains'].index(dom)==len(e['domains'])-1: #if this dom is not the last one:
					print(json.dumps(d, indent=2, sort_keys=True),end=",\n",file=outputF)
				else:
					print(json.dumps(d, indent=2, sort_keys=True),end="\n",file=outputF)
			elif elasticInsertIndex:
				results.append(d.__dict__)
				#insertESBulk(d.__dict__,elasticInsertIndex)
		if elasticInsertIndex:
			insertESBulk(results,elasticInsertIndex)
	if outputFile:
		print("]",file=outputF)

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
		#domain doesn't resolve:
		if convertDatetime(d.reg_date) > datetime.now()-timedelta(seconds=200): #"now", with a margin of 200 secs
			#not registered (because reg_date is now):
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

def get_dns(d):
	resolv = dns.resolver.Resolver()
	resolv.lifetime = REQUEST_TIMEOUT_DNS
	resolv.timeout = REQUEST_TIMEOUT_DNS
	try:
		ans = resolv.query(d.domain, 'NS')
		#for rdata in sorted(ans):
		d.ns.append(answer_to_list(ans))
	except DNSException:
		pass

	if d.ns!=[]:
		try:
			ans = resolv.query(d.domain, 'A')
			#for rdata in sorted(ans):
			d.a.append(answer_to_list(ans))
		except DNSException:
			pass

		try:
			ans = resolv.query(d.domain, 'AAAA')
			#for rdata in sorted(ans):
			d.aaaa.append(answer_to_list(ans))
		except DNSException:
			pass

		try:
			ans = resolv.query(d.domain, 'MX')
			#for rdata in sorted(ans):
			d.mx.append(answer_to_list(ans))
		except DNSException:
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
	#TODO: append subdoms to main domain
	pass

def answer_to_list(answers):
	return sorted(list(map(lambda record: str(record).strip(".") if len(str(record).split(' ')) == 1 else str(record).split(' ')[1].strip('.'), answers)))

if __name__ == '__main__':

	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
		usage="%(prog)s [opt args]\npipelining e.g.: echo \"{'fuzzer': 'Original*', 'domain-name': 'movistar.com'}\" | %(prog)s [opt args]")
	parser.add_argument('custCode',help='TEF_ES (usually extracted by multiRetrDat.sh)')
	onlyOneGroup = parser.add_mutually_exclusive_group()
	onlyOneGroup.add_argument('-d','--dictFile',help='e.g.: dict-37tlds.json')
	onlyOneGroup.add_argument('-e','--elastic',metavar='INDEX',help='get data from ES')
	parser.add_argument('-o','--outputFile',help='e.g.: output-37tlds.json')
	parser.add_argument('-i','--insertElastic',metavar='INDEX',help='insert results (one domain at once) into ES')
	parser.add_argument('-v','--verbose',action='store_true')
	args = parser.parse_args()

	results = []
	nregs = 0

	if args.dictFile or args.elastic:
		if args.elastic:
			es = Elasticsearch(['http://localhost:9200'])
		retrieveDomainsData(args.custCode,args.dictFile,args.elastic,args.insertElastic,args.outputFile,args.verbose)
	else:
		# GET DNS with DomainThreads (just for piping-PoC)
		for line in sys.stdin:
			domain_str = '{'+line.split('{')[1] # e.g.: domain_str = "{'fuzzer': 'Original*', 'domain-name': 'movistar.com'}"
			domain = json.loads(domain_str.replace( "'",'"')) # json needs property name enclosed in double quotes

			d = Domain()
			d.domain = domain['domain-name']

			get_dns(d)
			results.append(d)

			if args.verbose:
				if d.ns!=[]:
					print("REGISTERED!",d.domain)
					nregs+=1
				print(json.dumps({"domain": d.domain, "status": d.status, "ns": d.ns}))
				print("[%i vars checked, %i regs]"%(len(results),nregs))
