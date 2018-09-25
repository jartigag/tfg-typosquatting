#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 24/09/2018
#version: 0.1 ( all notifs. in one email )
#send notifs-content.txt by email
#
#usage: sendNotifs.py

from updateData import send_email, send_email2

#get how many notifs there are in total:
numbNotifs = 0
with open('notifs-content.txt','r') as f:
	for line in f:
		if "changes for" in line:
			numbNotifs+=int(line.split()[0])

#send notifications:
with open('notifs-content.txt','r') as f:
	send_email('{} changes \
		in typosquatting database (stage 2)!'.format(numbNotifs),f.read())
	send_email2('{} changes \
		in typosquatting database (stage 2)!'.format(numbNotifs),f.read())

#clean temp file
with open('notifs-content.txt','w') as f:
	print("",file=f)
