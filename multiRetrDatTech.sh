#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.5)
#date: 03/10/2018
#version: 0.5 (customer as an argument)
#
# execute retrieveData.py CUST_CODE on multiple processes (one for each technic)
# usage: bash multiRetrDatTech.sh ESindexFrom ESindexTo cust_code

echo "$(date) - running multiRetrDatTech.sh.."

arrFiles=(DAT/*)

for technic in original various bitsquatting homoglyph hyphenation insertion \
    omission repetition replacement subdomain transposition vowel-swap addition
do
    echo python3 retrieveData.py $3 $technic -e $1 -i $2 -v
    /usr/bin/time -o times/time-retrDat-$3-$technic.txt \
            python3 retrieveData.py $3 $technic -e $1 -i $2 -v \
            >> logs/logs-retrDat/log-$3-$technic.log &
done
wait
echo "$(date) - multiRetrDatTech.sh done."
