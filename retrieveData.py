#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 25/06/2018
#version: 0.2 (based on the draft script dnsCheck.py)
#for a dictionary of domains, RETRIEVE DATA of whois (status, owner, registration_date, owner_change, creation_date)
#and get their ip, mx records and if domain/subdomains returns something.
#results of each domain are stored in an array of Domain objects with all their collected info.

#TODO: Creation Date, Updated Date could be took from whois
#TODO: all .web in results are ['False']..

#recommended execution: /usr/bin/time -o time.txt python3 retrieveData.py dict.txt output.dat

import argparse
from datetime import date, timedelta, datetime
import whois
import dns.resolver
import requests
import socket
import json

class Domain:
    def __init__(self):
        self.status = 'not resolving'
        self.owner = ''
        self.reg_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.owner_change = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.ip = ''
        self.mx = []
        self.web = []
        self.domain = ''
        self.subdomains = '' #TODO
        self.test_freq = '' #TODO
        self.generation = '' #TODO (venía dado en dictionary.txt)
        self.customer = '' #TODO (venía dado en dictionary.txt)
        self.priority = '' #TODO
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def retrieveDomainsDataFromFile(file):
    results = []
    with open(file) as f:
            domains = f.read().splitlines()
    for dom in domains:
        d = Domain()
        d.domain = dom

        # check whois
        try:
            w = whois.query(dom)
            d.status = 'resolving'
            d.owner = w.name
            d.reg_date = w.last_updated.strftime('%Y-%m-%d %H:%M:%S')
            d.owner_change = w.creation_date.strftime('%Y-%m-%d %H:%M:%S')
            d.creation_date = w.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            #TODO: sometimes it fails because whois parses the result wrongly (ej: "ValueError: Unknown date format: 'registrar: the registrar, s.l.u'")
            pass

        # get ip
        try:
            d.ip = str(socket.gethostbyname(dom))
        except:
            pass

        # check if there are mx records
        try:
            d.mx = []
            ans = dns.resolver.query(dom, 'MX')
            for rdata in ans:
                d.mx.append(str(rdata.exchange))
        except:
            pass

        # check if the url returns something
        '''
        try:
            requests.get('https://' + dom, verify=False)
            #TODO: ignore "InsecureRequestWarning: Unverified HTTPS request is being made."
            #       it stops when d.web = False
            web_bool = 'True'
        except:
            web_bool = 'False'
        d.web.append(web_bool)
        '''

        # check if the knowns subdomains return something
        '''
        for sub in subdomains:
            try:
                requests.get('http://' + sub)
                web_bool = 'True'
            except:
                web_bool = 'False'
            web_array.append(web_bool)
        '''

        results.append(d)
        #print("[%i/%i]"%(domains.index(dom),len(domains)),
        #    "\033[1m","[-]" if d.status=='not resolving' else "[x]","%s:\033[0m"%(d.domain),
        #    d.__dict__) #DEBUGGING

    return results

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dictFile')
    parser.add_argument('outputFile')
    args = parser.parse_args()

    results = retrieveDomainsDataFromFile(args.dictFile)

    # print results as a json (an array of jsons, actually) to outputFile
    with open(args.outputFile,'w') as f:
        print("[",end="",file=f)
        for r in results:
            if not results.index(r)==len(results)-1:
                print(json.dumps(r.__dict__, indent=2, sort_keys=True),end=",\n",file=f)
            else:
                print(json.dumps(r.__dict__, indent=2, sort_keys=True),end="",file=f)
        print("]",file=f)
