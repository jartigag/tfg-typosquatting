#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 24/09/2018
#version: 0.2
#
# execute updateData.py on multiple processes (one for each customer)
# usage: bash multiUpDat.sh ESindex
#
# 30 2,10,18 * * * date >> ~/log-multiUpDat.txt
# 30 2,10,18 * * * bash ~/multiUpDat.sh results >> ~/log-multiUpDat.txt

echo "$(date) - running script.."
arrFiles=(DAT/*)
for filename in ${arrFiles[@]}
do
        name=$(basename $filename)
        cust=${name%_-_*} #cust=filename.split('_-_')[0]
        /usr/bin/time -o times/time-upDat-$cust.txt \
                python3 updateData.py $cust '*' $1 -v \
                >> logs/logs-upDat/log-$cust.log
        echo "$(date) - $cust's data updated"
done
python3 sendNotifs.py
echo "$(date) - script done."
