#!/usr/bin/bash

./extract_ids
mkdir names-and-ids
cat names-and-ids/* | sort --numeric-sort | uniq > all_mathematicians.txt
cat all_mathematicians.txt | awk '{print $1}' | sort --numeric-sort --check
if [[ $? == 1 ]]; then
	echo "there is a problem with mathematicians files"
	exit 1
fi
