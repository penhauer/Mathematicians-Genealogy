awk -F'\t\t' '{print $3}' unis.txt | sort | uniq -c | sort -nr | awk '$1 > 4 {$1=""; print $0}' | awk '{gsub(/^[ \t]+|[ \t]+$/, "")}1'
