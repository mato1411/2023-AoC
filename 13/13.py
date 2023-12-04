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
    print(list_input)
    result = 0
    print(f"{f} - Part 1: {result}")
    print(f"{f} - Part 2: {result}")
