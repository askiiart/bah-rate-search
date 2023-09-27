#!/usr/bin/env python3
import requests
import csv
import os
import zipfile
import sys

try:
    zip_code = sys.argv[1]
except IndexError:
    print("Run this again with an argument")
    print("For example: python3 bah-rate-search.py 90210")
    exit(1)

try:
    os.mkdir("./data")
except FileExistsError:
    pass

YEAR = "2023"
PAY_GRADE = "E-5"
DEPENDENTS = False

# Download and unzip BAH rates
bah_zip = requests.get(
    f"https://www.travel.dod.mil/Portals/119/Documents/BAH/BAH_Rates_All_Locations_All_Pay_Grades/ASCII/BAH-ASCII-{YEAR}.zip"
)

if not (os.path.exists(f"./data/sorted_zipmha{YEAR[2:]}.txt") and os.path.exists(f"./data/bahw{'' if DEPENDENTS else 'o'}{YEAR[2:]}.txt")):
    open("./data/bah-rates.zip", "wb").write(bah_zip.content)
    with zipfile.ZipFile("./data/bah-rates.zip", "r") as zip_ref:
        zip_ref.extractall("./data")

pay_grade_to_rank = {
    "E-1": 1,
    "E-2": 2,
    "E-3": 3,
    "E-4": 4,
    "E-5": 5,
    "E-6": 6,
    "E-7": 7,
    "E-8": 8,
    "E-9": 9,
    "W-1": 10,
    "W-2": 11,
    "W-3": 12,
    "W-4": 13,
    "W-5": 14,
    "O1E": 15,
    "O2E": 16,
    "O3E": 17,
    "O-1": 18,
    "O-2": 19,
    "O-3": 20,
    "O-4": 21,
    "O-5": 22,
    "O-6": 23,
    "O-7+": 24,
}

with open(f"./data/sorted_zipmha{YEAR[2:]}.txt", "rt") as f:
    sorted_zipmha = csv.reader(f, delimiter=" ")
    zip_to_code = {}
    for row in sorted_zipmha:
        zip_to_code[row[0]] = row[1]

with open(f"./data/bahw{'' if DEPENDENTS else 'o'}{YEAR[2:]}.txt", "rt") as f:
    reader = csv.reader(f)
    rates = {}
    for row in reader:
        rates[row[0]] = row[1:]

# Here's the original version, which I'm keeping here as a comment just because it's so long
# print(f"BAH rate: {with_dependents[zip_to_code[zip_code]][pay_grade_to_rank[PAY_GRADE] - 1] if DEPENDENTS else without_dependents[zip_to_code[zip_code]][pay_grade_to_rank[PAY_GRADE] - 1]}")
print(
    f"BAH rate: {rates[zip_to_code[zip_code]][pay_grade_to_rank[PAY_GRADE] - 1]}")
