file_handles = {}

try:
    with open("../cityNames.txt", "r") as file:
        for i, name in enumerate(file):
            name = name.strip()
            if not name:
                continue  # Skip empty lines
            
            first_letter = name[0].lower()
            if first_letter not in file_handles:
                file_handles[first_letter] = open(f"{first_letter}.txt", "a")
            
            file_handles[first_letter].write(name + "\n")

            if i % 500 == 0:
                print(f"{i} cities parsed")

finally:
    for f in file_handles.values():
        f.close()
