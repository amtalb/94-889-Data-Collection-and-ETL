head -n 1000 ${1} | tr [:upper:] [:lower:] | tr ' ' '_' | sed 's/#/num/' | csvsql -i postgresql --db-schema ${2} --tables ${3}
