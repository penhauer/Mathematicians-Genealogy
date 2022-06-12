input="list.txt"

while read -r line
do
	name=$(echo ${line} | awk -F';' '{print $1}')
	name=$(echo -e "${name}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
	uni=$(ggrep -m 1 -P "\t${name}\t" names-and-ids/sorted.txt)
	if [ -n "$uni" ]; then
		echo "${uni}"
	fi
done < ${input}
