input="unis_pruned.txt"

rm dataset.txt 2> /dev/null

while read -r line
do
	id=$(echo "${line}" | awk -F'\t\t' '{print $1}')
	uni=$(echo "${line}" | awk -F'\t\t' '{print $3}')
	bio=$(cat id_texts/${id})
	bio=$(echo ${bio})
	p="${bio}\t\t${uni}"
	echo -n "${bio}" >> dataset.txt
	echo -e -n "\t\t" >> dataset.txt
	echo "${uni}" >> dataset.txt
done < ${input}
