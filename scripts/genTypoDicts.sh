#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 28/07/2018
#version: 0.1
#
# execute genTypoDict.py with all the possible parameters
# usage: bash genTypoDicts.sh

#for n in 3 7 44 #number of tlds
$n=44
for technic in omission repetition addition
do
	/usr/bin/time -o times/time-dict-typo$n-tlds-$technic.txt \
		python3 genTypoDict.py -v files/tlds-$n.json files/DAT/ \
			dicts/dict-typo$n-tlds-$technic.json -t $technic \
		>> prints-dicts/prints-dict-typo$n-tlds-$technic.txt
done
