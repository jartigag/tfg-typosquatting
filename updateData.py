#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#date: 26/08/2018
#version: 0.3 ()
#from ElasticSearch, UPDATE DATA of whois, ip, mx records, webs for each domain
#if the domain has changed.
#
#usage: updateData.py customersDomainsDirectory elasticSearchIndex [-v]

#TO-DO LIST (26/08/2018):
# - insert d_updated correctly

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
from retrieveData import check_whois,get_ip,check_web,check_subdomains,Domain,convertDatetime#,get_dns
from insertES import updateES, getESDocs
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

def send_email2(subject, msg):
	sender_gmail = 'typosquattingnotifications.11p@gmail.com'
	password_gmail = 'innovation123abc..'
	receiver_gmail = 'tags.threats.analysis@telefonica.com'
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
	#custList = custList[:1] ## PARA PRUEBA CORTA
	for custCode in custList:
		data = getESDocs(indexName,custCode)
		if verbose:
			print(custCode,"loaded")

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

				'''
				if d_ES.status=='resolving': # that is, incomplete data:
					#TODO: fix in retrieveData.py
					continue #ignore it (by now)
				'''

				if d_ES.test_freq=='': d_ES.test_freq='0' #TEMP PATCH
				# if today is reviewing date:
				if convertDatetime(d_ES.timestamp) + timedelta(int(d_ES.test_freq)) <= datetime.today():
					start_time = time()
					d_updated.domain = d_ES.domain
					check_whois(d_updated); get_ip(d_updated); check_web(d_updated)#; check_subdomains(d_updated); get_dns(d_updated)
					end_time = time()

					if verbose:
						print("cust%i"%(dataPos),
							"[-]" if d_updated.ip==[] else "[x]",
							"%s %s"%(d_updated.customer,d_updated.domain),
							"(%.2f secs)"%(end_time-start_time))

					updateES(d_updated.__dict__, indexName)

					# if something has changed:
					'''
					if d_updated.ip!=d_ES.ip or d_updated.mx!=d_ES.mx or d_updated.web!=d_ES.web or d_updated.webs!=d_ES.webs:
						dd1 = 'DOMAIN: %s , Date: %s' % (str(d_updated.domain), str(d_updated.timestamp))
						dd2 = 'Old data: ip: %s -> r.date: %s -> mx: %s -> owner-change: %s -> subdom: %s -> web:%s -> webS:%s' % (str(d_ES.ip), str(d_ES.reg_date),
																										  str(d_ES.mx), str(d_ES.owner_change),
																										  str(d_ES.subdomains), str(d_ES.web),str(d_ES.webs))
						dd3 = 'New data: ip: %s -> r.date: %s -> mx: %s -> owner-change: %s -> subdom: %s -> web:%s -> webS:%s' % (str(d_updated.ip), str(d_updated.reg_date),
																										  str(d_updated.mx), str(d_updated.owner_change),
																										  str(d_updated.subdomains), str(d_updated.web),str(d_updated.webs))
						subject = 'News in ip, mx or web'
						msg = dd1 + '\n' + dd2 + '\n' + dd3
						send_email(subject, msg)
						send_email2(subject, msg)
					'''

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
