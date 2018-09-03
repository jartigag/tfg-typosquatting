#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#date: 31/08/2018
#version: 0.3 ( updateData(..,technic,..) )
#from ElasticSearch, UPDATE DATA of whois, ip, mx records, webs for each domain
#if the domain has changed.
#
#usage: updateData.py custCode elasticSearchIndex [-v]

#TO-DO LIST (29/08/2018):
# - notifications
# - include number of notifications

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

def updateData(custCode,technic,indexName,verbose):

	data = getESDocs(indexName,custCode,technic) # in this array goes the initial data, each customer at once
	if verbose:
		print(custCode,"loaded")

	try:
		for dom in data:
			d_ES = Domain()
			d_updated = Domain()

			for field in vars(d_ES):
				vars(d_ES)[field] = dom[field]
				#d_ES.status = dom['status'], d_ES.ip = dom['ip']...

			'''
			if d_ES.status=='resolving': # that is, incomplete data:
				#TODO: fix in retrieveData.py
				continue #ignore it (by now)
			'''

			if d_ES.test_freq=='': d_ES.test_freq='0' #TEMP PATCH
			# if today is reviewing date:
			if convertDatetime(d_ES.timestamp) + timedelta(int(d_ES.test_freq)) <= datetime.today():
				start_time = time()
				for field in vars(d_updated):
					vars(d_updated)[field] = vars(d_ES)[field]
				d_updated.timestamp = convertDatetime(datetime.now())
				check_whois(d_updated)#; get_ip(d_updated); check_web(d_updated); check_subdomains(d_updated); get_dns(d_updated)
				end_time = time()
				d_updated.resolve_time = resolve_time = "{:.2f}".format(end_time-start_time)

				if verbose:
					print("%s - [%i/%i]"%(custCode,data.index(dom)+1,len(data)),
					"[-]" if d_updated.ip==[] else "[x]", d_updated.domain, "(%s secs)"%(d_updated.resolve_time))

				updateES(d_updated.domain,d_updated.__dict__, indexName)

				# if something has changed:
				for field in vars(d_updated):
					if field=="timestamp" or field=="resolve_time" or field=="owner_change" or field=="creation_date" or field=="reg_date":
						continue
					elif vars(d_updated)[field] != vars(d_ES)[field]:
						subject = d_updated.domain+" has changed"
						msg = 'NOW:\n'+str(d_updated.__dict__)+'\n\nBEFORE:\n'+str(d_ES.__dict__)
						send_email(subject, msg)
						#send_email2(subject, msg)
						if verbose:
							print("	%s has changed: %s"%(d_updated.domain,str(d_updated.__dict__)))
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

	if verbose:
		print("update finished.")

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('custCode',help='e.g.: TEF_ES (usually extracted by multiUpDat.sh)')
	parser.add_argument('technic',help='e.g.: addition. it\'s the typosquatting technic')
	parser.add_argument('elasticSearchIndex')
	parser.add_argument('-v','--verbose',action='store_true')
	args = parser.parse_args()

	es = Elasticsearch(['http://localhost:9200'])
	updateData(args.custCode,args.technic,args.elasticSearchIndex,args.verbose)
