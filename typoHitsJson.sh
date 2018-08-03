#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 28/07/2018
#version: 0.1
#
# execute dnstwist.py with offDoms+TLDs >> regDoms.json
# usage: bash typoHitsJson.sh

echo "$(date) - running script.."
i=1
echo "[" >> regDoms-typoHits.json
cat merge-doms.txt | while read domain
do
	python2 dnstwist.py $domain -r -j -t 300 >> regDoms-typoHits.json
	echo "," >> regDoms-typoHits.json #TODO: don't print "," when dnstwist $domain don't get data
	echo -ne "$i\033[0K\r"
((i++))
done
echo "]" >> regDoms-typoHits.json
echo "$(date) - script done."
