import math
import pathlib
from datetime import datetime

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2023, day=datetime.now().day)

files = ["example.txt", input_file]
max_c = {
    "red": 12,
    "green": 13,
    "blue": 14
}
for f in files:
    result = 0
    list_input = read_input(f)
    p2_results = []
    for i, l in enumerate(list_input):
        exceeds_max = False
        sets = l.split(sep=":")[1].strip().split(sep=";")
        p2_max = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        for s in sets:
            for c, max_v in max_c.items():
                idx = s.find(c)
                if idx != -1:
                    st = idx - 2 if idx > 1 else idx - 1
                    d = int(s[idx-3 if idx > 2 else idx-2:idx-1].strip())
                    if d > p2_max[c]:
                        p2_max[c] = d
                    # print(f"{i}: {s} - {st, idx} - {d, c, max_v}")
                    if d > max_v:
                        # print("exceeds max")
                        exceeds_max = True
        if not exceeds_max:
            result += i+1
        p2_results.append(p2_max)
    print(f"{f} - Part 1: {result}")
    print(f"{f} - Part 2: {sum([math.prod(v.values()) for v in p2_results])}")
