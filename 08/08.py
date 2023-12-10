import copy
import math
import pathlib
from datetime import datetime

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2023, day=datetime.now().day)

files = ["example.txt", "example1.txt", "example_p2.txt", input_file]

for e, f in enumerate(files):
    list_input = read_input(f, sep="\n\n")
    # print(list_input)
    inst = [int(n) for n in list_input[0].replace("L", "0").replace("R", "1")]
    desert_nw = [l.split(sep="=") for l in list_input[1].split("\n")]
    desert = dict()
    for node in desert_nw:
        desert[node[0].strip()] = [n.replace("(", "").replace(")", "").strip() for n in node[1].strip().split(sep=",")]
    # print(inst)
    # print(desert)
    start = "AAA"
    end = "ZZZ"
    current_node = start
    p1_steps, p2_steps = 0, 0
    while current_node != end:
        if current_node not in desert:
            break
        # print(current_node)
        for i in inst:
            p1_steps += 1
            current_node = desert[current_node][i]
            if current_node == end:
                break
    print(f"{f} - Part 1: {p1_steps}")
    if e < 2:
        continue
    current_nodes = [n for n in desert.keys() if n.endswith("A")]
    end_nodes = {n for n in desert.keys() if n.endswith("Z")}
    first_match_iters = []
    for current_node in current_nodes:
        print(current_node)
        z_iter = 0
        find_end_count = 0
        while True:
            for i in inst:
                current_node = desert[current_node][i]
                z_iter += 1
                if current_node in end_nodes:
                    print("\t", z_iter, current_node)
                    find_end_count += 1
                    if find_end_count == 1:
                        first_match_iters.append(z_iter)
            if find_end_count == 5:
                break
    print(f"{f} - Part 2: {math.lcm(*first_match_iters)}")
