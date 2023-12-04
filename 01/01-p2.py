import pathlib
from datetime import datetime

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2023, day=datetime.now().day)

files = ["example.txt", "example-p2.txt", input_file]

c_numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

for f in files:
    list_input = read_input(f)
    result = 0
    sub_strings = [f"{k},{v}".split(sep=",") for k, v in c_numbers.items()]
    sub_strings = [i for sublist in sub_strings for i in sublist]
    for e, l in enumerate(list_input):
        lowest_i = 10000000000
        lowest_v = ""
        highest_i = 10000000000
        highest_v = ""
        for c in sub_strings:
            i = l.find(c)
            if i != -1 and i < lowest_i:
                lowest_i = i
                lowest_v = c
            i = l[::-1].find(c[::-1])
            if i != -1 and i < highest_i:
                highest_i = i
                highest_v = c
        n_l = lowest_v if lowest_v.isdigit() else c_numbers[lowest_v]
        n_h = highest_v if highest_v.isdigit() else c_numbers[highest_v]
        n = int(f"{n_l}{n_h}")
        result += n
    print(f"{f} - Part 2: {result}")
