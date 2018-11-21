#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 09/08/2018
#version: 0.1
#
# split typoDict.json in cust_codeDict.json files
# usage: bash splitTypoDict.sh compact-typoDict.json

mkdir typoDicts
lastCustCode="-"
i=-1 # first 2 typoDicts are invalid and will be removed
while read line
do
	custDict=${line::-1} # line="{custDict},"
	quotedCustCode=$(echo $custDict | jq -c -M '.customer')
	custCode=${quotedCustCode//\"} # remove double quotes \"

	#all domains in same file ($custCode-typoDict.json)
	if [[ $custCode == $lastCustCode ]]
	then
		# continue with last custCode
		echo "$custDict," >> typoDicts/$custCode-typoDict.json
	else
		# new custCode
		truncate -s-2 typoDicts/$lastCustCode-typoDict.json # remove ",\n"
		echo "" >> typoDicts/$lastCustCode-typoDict.json
		echo "]" >> typoDicts/$lastCustCode-typoDict.json # close last dict
		printf "..$lastCustCode typoDict done\n"
		((i++))
		printf "$i - making $custCode typoDict..	"
		echo "[" >> typoDicts/$custCode-typoDict.json # open new dict
		echo "$custDict," >> typoDicts/$custCode-typoDict.json
	fi
	lastCustCode=$custCode
done < $1
rm typoDicts/-typoDict.json # because lastCustCode="-"
rm typoDicts/--typoDict.json # because first custDict = ${"["::-1}
