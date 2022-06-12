#!/usr/bin/bash

./extract_ids
cat names-and-ids/* | sort --numeric-sort | uniq > all.txt
cat all.txt | awk '{print $1}' | sort --numeric-sort --check
if [[ $? == 1 ]]; then
	echo "there is a problem with mathmaticians files"
	exit 1
fi
