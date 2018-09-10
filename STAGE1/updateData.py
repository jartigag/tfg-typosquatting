#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.4)
#date: 09/09/2018 (adapted for STAGE1)
#version: 0.4 ( notifications )
#from ElasticSearch, UPDATE DATA of whois, ip, mx records, webs for each domain
#if the domain has changed.
#
#usage: updateData.py custCode elasticSearchIndex [-v]

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
from retrieveData import Domain,convertDatetime,check_whois,get_ip,check_web,check_subdomains#,get_dns
from insertES import updateES, getESDocs

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
		mailServer.sendmail(sender_gmail,receiver_gmail,message.as_string())
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
		mailServer.sendmail(sender_gmail,receiver_gmail,message.as_string())
	except Exception as e:
		print('email error: ',e)

def convertDatetime(date):
	if isinstance(date, datetime): #if argument's type is datetime
		return date.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(date, str): #if argument's type is string
		return datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
	else:
		return False

def updateData(custCode,indexName,verbose):

	data = getESDocs(indexName,custCode) # in this array goes the initial data, each customer at once
	msg = ''
	nchanges = 0
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

			#if d_ES.test_freq=='': d_ES.test_freq='0' #TEMP PATCH
			# if today is reviewing date:
			if convertDatetime(d_ES.timestamp) + timedelta(int(d_ES.test_freq)) <= datetime.today():
				start_time = time()
				d_updated.copy(d_ES)
				d_updated.timestamp = convertDatetime(datetime.now())
				check_whois(d_updated); get_ip(d_updated)
				check_web(d_updated); #get_dns(d)
				end_time = time()
				d_updated.resolve_time = "{:.2f}".format(end_time-start_time)

				if verbose:
					print("%s - [%i/%i]"%(custCode,data.index(dom)+1,len(data)),
					"[-]" if d_updated.ip==[] else "[x]", d_updated.domain, "(%s secs)"%(d_updated.resolve_time))

				updateES(d_updated.domain,d_updated.__dict__, indexName)

				# if something has changed:
				for field in vars(d_updated):
					if field=="timestamp" or field=="resolve_time" or field=="owner_change" or field=="creation_date" or field=="reg_date":
						continue
					elif vars(d_updated)[field] != vars(d_ES)[field]:
						nchanges += 1
						msg += '{} in {} field. \
NOW: {} BEFORE: {}\n'.format(d_updated.domain,field,vars(d_updated)[field],vars(d_ES)[field])
						if verbose:
							print("	%s has changed in its field %s: %s %s"
								%(d_updated.domain,field,
								vars(d_updated)[field],vars(d_ES)[field]))

	except Exception as e:
		print('updateData error:', e)

	if msg!='': #if there's news:
		send_email('{} changes for {}\
 in typosquatting database!'.format(nchanges,custCode), msg)
		send_email2('{} changes for {}\
 in typosquatting database!'.format(nchanges,custCode), msg)
		if verbose:
			print("mail with {} changes for {} sent.".format(nchanges,custCode))

	if verbose:
		print("update finished.")

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('custCode',help='e.g.: TEF_ES (usually extracted by multiUpDat.sh)')
	parser.add_argument('elasticSearchIndex')
	parser.add_argument('-v','--verbose',action='store_true')
	args = parser.parse_args()

	updateData(args.custCode,args.elasticSearchIndex,args.verbose)
