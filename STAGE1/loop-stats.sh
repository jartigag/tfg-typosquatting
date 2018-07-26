for i in {7..18}
do
	bash stats-retrieveData-logs.sh log-files/multi-dict-44tlds/log$i.log \
	> log-files/multi-dict-44tlds/stats-log$i.txt
done
