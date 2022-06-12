for f in raw/*
do
        g=$(basename -- ${f})
        echo ${g}
        awk '/Died|Summary/{exit};NF' ${f} | tail -n 1  > birthplace/${g}
        printf '\n'
done
