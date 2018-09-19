#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#date: 19/09/2018
#version: 0.3 (in rows of five)
#
# execute retrieveData.py on multiple processes (one for each customer)
# usage: bash multiRetrDat.sh ESindexFrom ESindexTo

echo "$(date) - running script.."

arrFiles=(DAT/*)

for i in ${!arrFiles[@]}
#The keys are accessed using an exclamation point: ${!array[@]}, the values are accessed using ${array[@]}
do
    echo "$i" #DEBUGGING
    if (( $i%5==0 )) #to run in rows of five
    then
    name5=$(basename ${arrFiles[$i]})
    name4=$(basename ${arrFiles[$i-1]})
    name3=$(basename ${arrFiles[$i-2]})
    name2=$(basename ${arrFiles[$i-3]})
    name1=$(basename ${arrFiles[$i-4]})
    cust5=${name5%_-_*} #cust=filename.split('_-_')[0]
    cust4=${name4%_-_*}
    cust3=${name3%_-_*}
    cust2=${name2%_-_*}
    cust1=${name1%_-_*}
    /usr/bin/time -o times/time-retrDat-$cust5.txt \
            python3 retrieveData.py $cust5 '*' -e $1 -i $2 -v \
            >> logs/logs-retrDat/log-$cust5.log &
    echo "$(date) - $cust5's data running.."
    /usr/bin/time -o times/time-retrDat-$cust4.txt \
            python3 retrieveData.py $cust4 '*' -e $1 -i $2 -v \
            >> logs/logs-retrDat/log-$cust4.log &
    echo "$(date) - $cust4's data running.."
    /usr/bin/time -o times/time-retrDat-$cust3.txt \
            python3 retrieveData.py $cust3 '*' -e $1 -i $2 -v \
            >> logs/logs-retrDat/log-$cust3.log &
    echo "$(date) - $cust3's data running.."
    /usr/bin/time -o times/time-retrDat-$cust2.txt \
            python3 retrieveData.py $cust2 '*' -e $1 -i $2 -v \
            >> logs/logs-retrDat/log-$cust2.log &
    echo "$(date) - $cust2's data running.."
    /usr/bin/time -o times/time-retrDat-$cust1.txt \
                python3 retrieveData.py $cust1 '*' -e $1 -i $2 -v \
                >> logs/logs-retrDat/log-$cust1.log #don't send to bg
        echo "$(date) - $cust1's data running.."
        fi
    done
    echo "$(date) - script done."
