input="list.txt"

while read -r line
do
	name=$(echo ${line} | awk -F';' '{print $1}')
	name=$(echo -e "${name}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
	uni=$(grep -m 1 -P "\t\t${name}\t\t" ../students-finder-engine/all_mathematicians.txt)
	if [ -n "$uni" ]; then
		echo "${uni}"
	fi
done < ${input}
