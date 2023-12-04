import pathlib
from datetime import datetime
import re
from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2023, day=datetime.now().day)

files = ["example.txt", input_file]

for f in files:
    list_input = read_input(f)
    # print(list_input)
    p1 = 0
    instances_of_cards = dict()
    for i, c in enumerate([l.split(sep=":")[1].split(sep="|") for l in list_input]):
        instances_of_cards[i] = instances_of_cards.get(i, 0) + 1
        exp_numbers = re.findall(r'\d+', c[0].strip())
        act_numbers = re.findall(r'\d+', c[1].strip())
        points, n_matches = 0, 0
        matches = []
        for n in exp_numbers:
            if n in act_numbers:
                matches.append(n)
                n_matches += 1
                # Number of points depends on the number of matches
                # Matches: 1 2 3 4 5 6  7  8  9   10  11  12   13
                # Points:  1 1 2 4 8 16 32 64 128 256 512 1024 2048
                if n_matches <= 2:
                    points += 1
                else:
                    points += 2 ** (n_matches - 2)
        p1 += points
        for instance in range(0, instances_of_cards[i]):
            for n in range(1, n_matches+1):
                instances_of_cards[i+n] = instances_of_cards.get(i+n, 0) + 1
    # print(instances_of_cards)
    print(f"{f} - Part 1: {p1}")  # 20117
    print(f"{f} - Part 2: {sum(instances_of_cards.values())}")  # 13768818
