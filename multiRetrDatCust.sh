#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.5)
#date: 03/10/2018
#version: 0.5 (for c in cust_code: bash multiRetrDatTech.sh)
#
# execute multiRetrDatCust.sh iterating through customers
# usage: bash multiRetrDatCust.sh ESindexFrom ESindexTo

echo "$(date) - running multiRetrDatCust.sh.."

arrFiles=(DAT/*)

for i in ${!arrFiles[@]}
#The keys are accessed using an exclamation point: ${!array[@]}, 
#the values are accessed using ${array[@]}
do
    name=$(basename ${arrFiles[$i]})
    cust=${name%_-_*} #cust=filename.split('_-_')[0]
    echo "$(date) - $cust's data running.."
    time bash multiRetrDatTech.sh $1 $2 $cust
done
echo "$(date) - multiRetrDatCust.sh done."
