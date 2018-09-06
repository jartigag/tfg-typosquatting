dicts=typoDicts/*
mkdir output-typoDicts; mkdir time-typoDicts
for dict in $dicts ;
do echo "processing $dict..";
/usr/bin/time -o time-$dict.txt \
	python3 retrieveData.py -d $dict -o output-$dict &
done
