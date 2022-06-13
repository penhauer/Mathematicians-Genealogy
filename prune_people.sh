input="unis.txt"

while read -r line
do
	uni=$(echo "${line}" | awk -F'\t\t' '{print $3}')
	is_ok=$(grep -m 1 "${uni}" pruned_unis.txt)
	if [ -n "$is_ok" ]; then
		echo "${line}"
	fi
done < ${input}
