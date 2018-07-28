#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 28/07/2018
#version: 0.1
#
# execute dnstwist.py with offDoms+TLDs >> output.txt
# usage: bash typoHits.sh

echo "$(date) - running script.."
i=1
cat merge-doms.txt | while read domain
do
   python2 dnstwist.py $domain -r >> totalOutput-typoHits.txt
   echo -ne "$i\033[0K\r"
   ((i++))
done 
echo "$(date) - script done."
