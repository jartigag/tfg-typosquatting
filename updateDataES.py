#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#date: 22/08/2018
#version: 0.3 ()
#from ElasticSearch, UPDATE DATA of whois, ip, mx records, webs for each domain
#if the domain has changed.
#
#usage: updateDataES.py customersDomainsDirectory elasticSearchIndex [-v]

#TO-DO LIST (17/07/2018):
# show progress with an index var or something
# too many domains are checked in each execution. isn't the reviewing date condition correctly working?
# (this last fact was observed in data1. #TODO: check with data5)

import argparse
from datetime import timedelta, datetime
from time import time
import whois
import dns.resolver
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import socket
import json
import smtplib
from email.mime.text import MIMEText
from elasticsearch import Elasticsearch, helpers
from retrieveData import get_dns,check_whois,get_ip,check_web,check_subdomains,Domain,convertDatetime
from insertES import insertES, getESDocs
import os

def send_email(subject, msg):
	sender_gmail = 'typosquattingnotifications.11p@gmail.com'
	password_gmail = 'innovation123abc..'
	receiver_gmail = 'typosquattingnotifications.11p@gmail.com'
	try:
		mailServer = smtplib.SMTP('smtp.gmail.com', 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(sender_gmail, password_gmail)
		message = MIMEText(msg)
		message['From'] = sender_gmail
		message['To'] = receiver_gmail
		message['Subject'] = subject
		mailServer.sendmail(sender_gmail,
							receiver_gmail,
							message.as_string())
	except Exception as e:
		print('email error: ',e)

def updateData(customersDomainsDirectory,indexName,verbose):
	custList = []
	for c in os.listdir(customersDomainsDirectory):
		custList.append(c.split('_-_')[0]) # customer code

	data = [] # in this array goes the initial data, each customer at once
	if verbose:
		print("loading data from ES...")
	custList = custList[:1] ## PARA PRUEBA CORTA
	for custCode in custList:
		data = getESDocs(indexName,custCode)
		if verbose:
			print(custCode,"loaded")
	if verbose:
		print("all data loaded.")

	try:
		# just for printing progress:
		dataPos = 1
		lastCustCode = data[0]['customer']
		for dom in data:
			d_ES = Domain()
			d_updated = Domain()
			#elem = e['_source'] #elem = e['_source']['doc']
			# We have to catch all data per data as domain, status, web...
			#TODO: can this be shorter?
			d_ES.status = dom['status']
			d_ES.owner = dom['owner']
			d_ES.reg_date = dom['reg_date']
			d_ES.owner_change = dom['owner_change']
			d_ES.creation_date = dom['creation_date']
			d_ES.ip = dom['ip']
			d_ES.mx = dom['mx']
			d_ES.web = dom['web']
			d_ES.webs = dom['webs']
			d_ES.domain = dom['domain']
			d_ES.subdomains = dom['subdomains']
			d_ES.test_freq = dom['test_freq']
			d_ES.generation = dom['generation']
			d_ES.customer = dom['customer']
			d_ES.priority = dom['priority']
			d_ES.timestamp = dom['timestamp']
			if dom['customer']!= lastCustCode:
				dataPos+=1

			if d_ES.status=='resolving': # that is, incomplete data:
				#TODO: fix in retrieveData.py
				continue #ignore it (by now)

			# if today is reviewing date:
			if convertDatetime(d_ES.timestamp) + timedelta(int(d_ES.test_freq)) <= datetime.today():
				start_time = time()
				d_updated.domain = d_ES.domain
				get_dns(d_updated)#; check_whois(d); get_ip(d); check_web(d); check_subomains(d)
				end_time = time()

				if verbose:
					print("cust%i"%(dataPos),
						"[-]" if d_updated.ip==[] else "[x]",
						"%s %s"%(d_updated.customer,d_updated.domain),
						"(%.2f secs)"%(end_time-start_time))

				insertES(d_updated.__dict__,'updatedata1') #INDEX NAME

	except Exception as e:
		print('updateData error:', e)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('elasticSearchIndex')
	parser.add_argument('customersDomainsDirectory',help='e.g.: files/DAT/')
	parser.add_argument('-v','--verbose',action='store_true')
	args = parser.parse_args()

	es = Elasticsearch(['http://localhost:9200'])
	updateData(args.customersDomainsDirectory,args.elasticSearchIndex,args.verbose)
