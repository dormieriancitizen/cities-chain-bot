#!/bin/bash
# wget "http://download.geonames.org/export/dump/cities500.zip"

unzip -c cities500.zip | \
awk 'BEGIN {FS="\t"; OFS="|"}; $19 !~ /^202[5-9]-/ && $19 !~ /^2024-(0[6-9]|1[0-2])-/ && $19 !~ /^2024-05-(0[2-9]|[1-3][0-9])/ {sub(/^\x27/, "", $3); print $3, $15, $11, $9}' | \
sort -u > cityNames.txt

rm -r cities
mkdir -p cities
cd ./cities
cat ../cityNames.txt | while read -r name; do echo "$name" >> "$(echo "${name:0:1}" | tr '[:upper:]' '[:lower:]').txt"; done

cd ..
python3 chainGen.py > chain500.txt
echo "Chain Length: $(wc -l chain500.txt)"