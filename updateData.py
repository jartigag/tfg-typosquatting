#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.6)
#date: 25/09/2018
#version: 0.6 ( priority criteria based on dns )
#from ElasticSearch, UPDATE DATA of each domain
#if the domain has changed.
#
#usage: updateData.py custCode technic elasticSearchIndex [-v]

import argparse
from datetime import timedelta, datetime
from time import time
import json
import smtplib
from email.mime.text import MIMEText
from elasticsearch import Elasticsearch
from retrieveData import Domain,convertDatetime,get_dns
		#,check_whois,get_ip,check_web,check_subdomains
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

def updateData(custCode,technic,indexName,verbose):

	# in this array goes the initial data, each customer at once:
	data = getESDocs(indexName,custCode)
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

			# if today is reviewing date:
			if convertDatetime(d_ES.timestamp)+timedelta(int(d_ES.test_freq))\
							<= datetime.today():
				start_time = time()
				d_updated.copy(d_ES)
				d_updated.timestamp = convertDatetime(datetime.now())
				get_dns(d_updated)
				#get_ip(d_updated); check_web(d_updated)
				end_time = time()
				d_updated.resolve_time = "{:.2f}".format(end_time-start_time)

				if verbose:
					print("%s - [%i/%i]"%(custCode,data.index(dom)+1,len(data)),
					"[-]" if d_updated.ip==[] else "[x]", d_updated.domain,
					"(%s secs)"%(d_updated.resolve_time))

				updateES(d_updated.domain,d_updated.__dict__, indexName)

				# if something has changed:
				for field in vars(d_updated):
					if field=="timestamp" or field=="resolve_time"\
					 or field=="owner_change" or field=="creation_date"\
					 or field=="reg_date":
						continue
					elif vars(d_updated)[field] != vars(d_ES)[field]:
						nchanges += 1
						d_updated.priority = 'high'
						d_updated.status = 'very suspicious'
						msg += '{} in {} field. NOW: {} BEFORE: {}\n'\
.format(d_updated.domain,field,vars(d_updated)[field],vars(d_ES)[field])
						if verbose:
							print(" %s has changed in its field %s: %s %s"
									%(d_updated.domain,field,
									vars(d_updated)[field],vars(d_ES)[field]))

	except Exception as e:
		print('updateData error:', e)

	if msg!='': #if there's news:
		with open('notifs-content.txt','a') as f:
			print('{} changes for {}\
 in typosquatting database!'.format(nchanges,custCode), file=f)
			print(msg, "\n", file=f)
		if verbose:
			print("notif. with {} changes for {} ready.".format(nchanges,custCode))

	if verbose:
		print("update finished.")

if __name__ == '__main__':

		parser = argparse.ArgumentParser()
		parser.add_argument('custCode',
				help='e.g.: TEF_ES (usually extracted by multiUpDat.sh)')
		parser.add_argument('technic',
				help='e.g.: addition. it\'s the typosquatting technic')
		parser.add_argument('elasticSearchIndex')
		parser.add_argument('-v','--verbose',action='store_true')
		args = parser.parse_args()

		updateData(args.custCode,args.technic,args.elasticSearchIndex,args.verbose)