#!/bin/bash
wget "http://download.geonames.org/export/dump/cities500.zip"

unzip -c cities500.zip | \
awk 'BEGIN {FS="\t"; OFS="|"}; $19 ~ /^202[6-9]-/ {next}; {sub(/^\x27/, "", $3); print $3, $15, $11, $9}' | \
sort -u > cityNames.txt

rm -r cities
mkdir -p cities
cd ./cities
python3 ../parseCityNames.py

cd ..

python3 chainGen.py > chain.txt
echo "Chain Length: $(wc -l chain.txt)"


rm cityNames.txt
