bash find_bio_uni.sh | sort -u | sed 's/[[:space:]]*$//' | awk -F'\t\t' 'NF==3 {print $0}'
