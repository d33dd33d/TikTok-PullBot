import os

combo_file = input("[?] Enter combo file name >>> ")

with open(combo_file, "r") as file:
    lines = [line.strip() for line in file]

for line in lines:
    os.system(f"python check.py {line}")
    print(f"{line} processed.")

# made by https://github.com/d33dd33d