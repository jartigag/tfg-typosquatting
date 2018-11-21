#!/bin/bash
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.3)
#date: 03/08/2018
#version: 0.3 (a clearer way of showing percents)
#
# extract some numbers from typoHits output

totalReg=$(grep 'NS:' $1 | wc -l) # number of registered domains
totalMX=$(grep 'MX:' $1 | wc -l) # number of domains with mx servers associated
totalIP=$(grep -E "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" $1 | wc -l)
# number of domains with ip address associated

percent() {
	echo "$(echo "scale=$3;$1*100/$2" | bc -l)"
}

printf "%-15s %-15s %-15s %-15s\n" "technic:" "reg:" "mx:" "ip:"
printf "%-13s %-13s %-17s %-17s\n" "" "(% of total)" \
	"[% in each technic]" "[% in each technic]"
for t in Various Original Repetition Hyphenation Transposition Vowel-swap Omission \
Subdomain Addition Homoglyph Replacement Bitsquatting Insertion
do
	reg=$(grep "$t" $1 | wc -l)
	mx=$(grep "$t" $1 | grep 'MX:' | wc -l)
	ip=$(grep "$t" $1 | grep -E "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | wc -l)
	printf "%-15s %-15s %-15s %-15s\n" \
	"$t" "$reg ($(percent $reg $totalReg 0)%)" \
	"$mx [$(percent $mx $reg 0)%]" \
	"$ip [$(percent $ip $reg 0)%]"
done

totalVars=$(grep -o "[0-9]\+ domain" $1 | awk '{ SUM += $1} END { print SUM }')

printf "%-15s %-15s %-15s %-15s\n" "" "-----------" "-----------" "-----------"
printf "%-15s %-15s %-15s %-15s\n" "total:" \
"$totalReg ($(percent $totalMX $totalVars 3)%" \
"$totalMX ($(percent $totalMX $totalReg 0)%)" \
"$totalIP ($(percent $totalIP $totalReg 0)%)"
printf "%-6s %-22s %-16s %-16s\n" "" "of $totalVars variations)" \
	"(% of total reg)" "(% of total reg)"

# technic:        reg: (% total)  mx: [% reg]     ip: [% reg]
# Various         4265 (0%)       2121 [49%]      3951 [92%]
# Original        6444 (1%)       3049 [47%]      4847 [75%]
# Repetition      11587 (2%)      4343 [37%]      11488 [99%]
# Hyphenation     11646 (2%)      4325 [37%]      11491 [98%]
# Transposition   18878 (3%)      9151 [48%]      18587 [98%]
# Vowel-swap      20104 (3%)      10293 [51%]     19680 [97%]
# Omission        25255 (4%)      13436 [53%]     23753 [94%]
# Subdomain       36745 (6%)      20777 [56%]     36390 [99%]
# Addition        40478 (7%)      26588 [65%]     39204 [96%]
# Homoglyph       79188 (14%)     31251 [39%]     78716 [99%]
# Replacement     83718 (14%)     37822 [45%]     81975 [97%]
# Bitsquatting    92593 (16%)     42100 [45%]     90671 [97%]
# Insertion       131058 (23%)    51326 [39%]     130536 [99%]
#                 -----------     -----------     -----------
# total:          561959 (.707%)  256582 (45%)    551289 (98%)
#                 (% of variatns) (% of reg)      (% of reg)
# total variations: 36285593
