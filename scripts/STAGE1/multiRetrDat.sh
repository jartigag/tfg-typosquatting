#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 25/08/2018
#version: 0.2
#
# execute retrieveData.py on multiple processes (one for each customer)
# usage: bash multiRetrDat.sh ESindexFrom ESindexTo

echo "$(date) - running script.."
# custList = []
# for c in os.listdir(customersDomainsDirectory):
#       custList.append(c.split('_-_')[0]) # customer code

arrFiles=(files/DAT/*)
#for filename in ${arrFiles[@]:0:3}
for filename in ${arrFiles[@]}
do
        name=$(basename $filename)
        cust=${name%_-_*} #cust=filename.split('_-_')[0]
        /usr/bin/time -o times/time-retrDat-$cust.txt \
                python3 retrieveData.py $cust -e $1 -i $2 -v \
                >> logs/logs-retrDat/log-$cust.log #&
        echo "$(date) - $cust's data retrieved and inserted in ES"
done
#ps -AF | grep python3
echo "$(date) - script done."
