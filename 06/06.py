import pathlib
import re
from datetime import datetime

from utils import get_input, read_input


def get_record_breaking_opportunitues(max_times, records):
    all_record_breaking_opportunities = 1
    for t, r in zip(max_times, records):
        record_breaking_opportunities = 0
        for a in range(1, t+1):
            d = (t - a) * a
            if d > r:
                record_breaking_opportunities += 1
        all_record_breaking_opportunities *= record_breaking_opportunities
    return all_record_breaking_opportunities


input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2023, day=datetime.now().day)

files = ["example.txt", input_file]

for f in files:
    list_input = read_input(f)
    # print(list_input)
    max_times_p1 = [int(n) for n in re.findall(r'\d+', list_input[0].split(sep=":")[1].strip())]
    records_p1 = [int(n) for n in re.findall(r'\d+', list_input[1].split(sep=":")[1].strip())]
    p1 = get_record_breaking_opportunitues(max_times_p1, records_p1)
    print(f"{f} - Part 1: {p1}")
    max_time_p2 = [int("".join([str(n) for n in max_times_p1]))]
    record_p2 = [int("".join([str(n) for n in records_p1]))]
    p2 = get_record_breaking_opportunitues(max_time_p2, record_p2)
    print(f"{f} - Part 2: {p2}")
