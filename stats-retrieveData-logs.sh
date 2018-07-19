#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 10/07/2018
#version: 0.2
#
# extract some numbers from retrieveData logs

total=$(cat $1 | wc -l)

n=$(cat $1 | grep  "(.\." | wc -l)
echo "	>> 1-10 secs: $n ($(echo "scale=3;$n*100/$total" | bc -l)%)"

for i in {0..9}
do
	n=$(cat $1 | grep  "($i\." | wc -l)
	echo "$i-$(($i+1)) secs: $n ($(echo "scale=3;$n*100/$total" | bc -l)%)"
done

n=$(cat $1 | grep  "(..\." | wc -l)
echo "	>> 10-100 secs: $n ($(echo "scale=3;$n*100/$total" | bc -l)%)"

for i in {1..9}
do
	n=$(cat $1 | grep  "($i.\." | wc -l)
	echo "$(($i*10))-$(($i+1))0 secs: $n ($(echo "scale=3;$n*100/$total" | bc -l)%)"
	cat $1 | grep  "($i.\." | head -n 6
	if [ $n -gt 6 ]
	then
		echo "..."
	fi
done

echo "total: $total"
