#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 08/09/2018
#version: 0.1
#
# execute updateData.py on multiple processes (one for each customer)
# usage: bash multiUpDat.sh ESindex
#
# crontab: 0 2,10,18 * * * date >> ~/STAGE1/log-multiUpDat.sh
# crontab: 0 2,10,18 * * * bash ~/STAGE1/multiUpDat.sh data >> ~/STAGE1/log-multiUpDat.sh

echo "$(date) - running script.."
# custList = []
# for c in os.listdir(customersDomainsDirectory):
#       custList.append(c.split('_-_')[0]) # customer code

arrFiles=(~/STAGE1/files/DAT/*)
#for filename in ${arrFiles[@]:0:3}
for filename in ${arrFiles[@]}
do
        name=$(basename $filename)
        cust=${name%_-_*} #cust=filename.split('_-_')[0]
        /usr/bin/time -o ~/STAGE1/times/time-upDat-$cust.txt \
                python3 ~/STAGE1/updateData.py $cust $1 -v \
                >> ~/STAGE1/logs/logs-upDat/log-$cust.log #&
        echo "$(date) - $cust's data updated"
done
#ps -AF | grep python3
echo "$(date) - script done."
