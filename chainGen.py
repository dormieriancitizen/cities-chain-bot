from pathlib import Path

import typing
import subprocess

POP_LIMIT = 500

def file_len(fname):
    # the magic of getting someone else to do it for you
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

def city_chain(letter:str):
    def pick_city(letter,files,counts) -> typing.Tuple[str,str]:
        while True:
            letter_file = files[letter]
            city_line = letter_file.readline()

            counts[letter] += -1

            if city_line == "":
                # File is done
                print(f"Chain ended with {letter}")
                return "", "d"

            city_info = city_line.rstrip().split("|")

            if len(city_info) < 4:
                # Malformed in line
                continue
            
            if int(city_info[1]) < POP_LIMIT:
                # city doesn't have population data
                continue

            city = city_info[0]
            city_country = city_info[3]
            city_admin1 = city_info[2]

            if city:
                newletter = city[-1].lower()
                if not newletter.isalpha():
                    continue
                # print(f"{newletter}: {counts[newletter]}")
                if counts[letter] > 450 and counts[newletter] < 500:
                    # Try to find a better one
                    # print(f"{newletter} is nearly depleted, trying to find a better one")
                    continue

            if city_admin1 and not city_admin1 == "00":
                loc = f"{city_admin1}, {city_country}"
            else:
                loc = f"{city_country}"

            return city+", "+loc, newletter
    try:
        cities_info_folder = Path("cities")
        cities_files = {file.stem: file.open("r") for file in cities_info_folder.iterdir() if file.is_file()}

        counts = {}

        for letterFileStem, file in cities_files.items():
            counts[letterFileStem] = file_len(f"cities/{letterFileStem}.txt")

        used_cities: set[str] = set()

        # with open("used.txt","r") as used:
        #     for line in used:
        #         used_cities.add(line.rstrip())

        city: str = ""

        while True:            
            city, newletter = pick_city(letter,cities_files,counts)

            if city == "":
                return

            if city not in used_cities:
                letter = newletter

                yield city
                used_cities.add(city)

                city = ""
    finally:
        for file in cities_files.values():
            file.close()

# counts = {}
# for letter in "qwertyuiopasdfghjklzxcvbnm":
  # counts[letter] = len([city for city in city_chain(letter)])
# 
# print(counts)
# 
for city in city_chain("e"):
    print(city)
