#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.2)
#date: 09/07/2018
#version: 0.2
#
# execute retrieveData continuously
#usage: bash continuum-retrieveData.sh path/to/dictFile.json

i=1
file=$(mktemp)
progress() {
	t=0
	while [ -e $file ]
	do
		echo -ne "$t secs elapsed..\033[0K\r"
		sleep 1
		((t++))
	done
}
dictFile=$(basename "${1%.*}")
mkdir log-files/$dictFile
while :
do
	echo "$(date) - running script.."
	progress &
	progress_pid=$!
	/usr/bin/time -o log-files/$dictFile/time$i.txt \
	python3 retrieveData.py -v $1 log-files/$dictFile/output$i.json \
	>> log-files/$dictFile/log$i.log
	kill $progress_pid
	wait $progress_pid 2>/dev/null
	echo "$(date) - script done."
	echo "script executed $i times. let's go again!"
	i=$(($i + 1))
done
