import pathlib
from datetime import datetime

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2023, day=datetime.now().day)

files = ["example.txt", input_file]

for f in files:
    list_input = read_input(f)
    result = 0
    for l in list_input:
        d = [int(s) for s in l if s.isdigit()]
        n = int(f"{d[0]}{d[-1]}")
        result += n
    print(f"{f} - Part 1: {result}")
