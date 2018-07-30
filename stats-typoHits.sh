#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 30/07/2018
#version: 0.1
#
# extract some numbers from typoHits output

total=$(cat $1 | grep 'NS:' | wc -l) # number of registered domains

for t in Various Original Repetition Hyphenation Transposition Vowel-swap Omission \
Subdomain Addition Homoglyph Replacement Bitsquatting Insertion
do
	n=$(cat $1 | grep  "$t" | wc -l)
	printf "%-15s %-8s %-8s\n" "$t" "$n" "($(echo "scale=1;$n*100/$total" | bc -l)%)"
done

printf "%-15s %-8s\n" "" "------"
printf "%-15s %-8s\n" "total:" "$total"

# Various         2402     (.7%)   
# Original        3980     (1.2%)  
# Repetition      6628     (2.0%)  
# Hyphenation     6726     (2.0%)  
# Transposition   10884    (3.3%)  
# Vowel-swap      11747    (3.6%)  
# Omission        15290    (4.7%)  
# Subdomain       20187    (6.2%)  
# Addition        23649    (7.2%)  
# Homoglyph       46631    (14.3%) 
# Replacement     48453    (14.9%) 
# Bitsquatting    53955    (16.5%) 
# Insertion       74646    (22.9%) 
#                 ------  
# total:          325178