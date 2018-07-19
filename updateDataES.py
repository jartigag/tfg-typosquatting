#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 16/07/2018 (using helpers.scan to scroll ES)
#version: 0.2 (based on ts-updater.py)
#from ElasticSearch, UPDATE DATA of whois, ip, mx records, webs for each domain
#if the domain has changed.
#
#usage: updateDataES.py elasticSearchIndex [-v]

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
from retrieveData import check_whois, get_ip, get_mx, check_web, Domain

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

def convertDatetime(date):
	if isinstance(date, datetime): #if argument's type is datetime
		return date.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(date, str): #if argument's type is string
		return datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
	else:
		return False

def updateData(indexName,verbose):
	es = Elasticsearch(['http://localhost:9200'])
	try:
		allElements = helpers.scan(es,index=indexName, preserve_order=True, query={"query": {"match": {"_index": indexName}}})
		for oneElement in list(allElements):
			d_ES = Domain()
			d_updated = Domain()
			elem = oneElement['_source']['doc']
			# We have to catch all data per data as domain, status, web...
			#TODO: can this be shorter?
			d_ES.status = elem['status']
			d_ES.owner = elem['owner']
			d_ES.reg_date = elem['reg_date']
			d_ES.owner_change = elem['owner_change']
			d_ES.creation_date = elem['creation_date']
			d_ES.ip = elem['ip']
			d_ES.mx = elem['mx']
			d_ES.web = elem['web']
			#d_ES.webs = elem['webs']
			d_ES.domain = elem['domain']
			d_ES.subdomains = elem['subdomains']
			d_ES.test_freq = elem['test_freq']
			d_ES.generation = elem['generation']
			d_ES.customer = elem['customer']
			d_ES.priority = elem['priority']
			d_ES.timestamp = elem['timestamp']

			if d_ES.status=='resolving': # that is, incomplete data:
				#TODO: fix in retrieveData.py
				continue #ignore it (by now)

			# if today is reviewing date:
			if convertDatetime(d_ES.timestamp) + timedelta(int(d_ES.test_freq)) <= datetime.today():
				start_time = time()
				d_updated.domain = d_ES.domain
				check_whois(d_updated) #TODO: w.creation_date[-1] ¿?
				get_ip(d_updated)
				get_mx(d_updated)
				check_web(d_updated)
				end_time = time()
				if verbose:
					#print("cust%i - [%i/%i]"%(data.index(e)+1,e['domains'].index(dom)+1,len(e['domains'])),
					#TODO: index of the domain?
					print("[-]" if d_updated.ip==[] else "[x]",
						"%s %s"%(d_updated.customer,d_updated.domain),
						"(%.2f secs)"%(end_time-start_time))

				# In this part of the script will look if data are diferent of elasticsearch data
				'''
					# by now, this has no sense because whois.query('adomain.com').owner it's always 'adomain.com'
					if d_ES.owner != d_updated.owner:
						subject = str(d_updated.owner)+'\'s owner has changed'
						msg1 = 'Domain: ' + str(d_updated.domain) + ' timestamp: ' + str(d_updated.timestamp)
						msg2 = '\nOld owner: ' + str(d_ES.owner)
						msg3 = '\nNew owner: ' + str(owner0) +'\nIP:' + str(ip0) + ' MX:' + str(mx0)
						msg = msg1 + msg2 + msg3
						send_email(subject, msg)
						# if ip0 == '' or ip0 is None:
						# 	priority0 = 'high'
						# 	status0 = 'very suspect'
						# else:
						# 	priority0 = 'high'
						# 	status0 = 'suspect'
					else:
						if d_updated.ip==[] and d_updated.owner!='':
							d_updated.priority = 'low'
							d_updated.status = 'parking'
						else:
							d_updated.priority = 'low'
							d_updated.status = 'very low priority'
					if d.priority=='high':
						d.test_freq = 1
					elif d.priority=='low':
						d.test_freq = 14
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
					# We don't want the same data in our txt
					with open('changes_in_domain.txt', 'r') as f:
						for i in f.readlines():
							if i == dd1 or i == dd1 + '\n':
								pass
							else: # if data hasn't been created:
								with open('changes_in_domain.txt', 'a') as f:
									f.write('\n' + dd1 + '\n' + dd2 + '\n' + dd3 + '\n')
				else:
					d_updated.test_freq = '14'
					d_updated.priority = 'low'
					d_updated.status = 'parking'

				try:
					body = '{"doc": {'
					field_names = d_updated.__dict__
					for i in field_names:
						if not list(field_names).index(i)==len(field_names)-1:
							body+='"'+i+'":"'+str(field_names[i])+'",'
						else:
							body+='"'+i+'":"'+str(field_names[i])+'"}}'
					es.update(index=indexName, doc_type='string', body=body, id=d_updated.domain)
					if verbose:
						print('Uploaded:', d_updated.domain)
				except Exception as e:
					print('Not uploaded:', d_updated.domain)
					print('data insertion error:', str(e))
	except Exception as e:
		print('updateData error:', e)

	#if verbose:
	#	print('TOTAL UPDATED DOMAINS:', actualElement)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('elasticSearchIndex')
	parser.add_argument('-v','--verbose',action='store_true')
	args = parser.parse_args()

	updateData(args.elasticSearchIndex,args.verbose)
