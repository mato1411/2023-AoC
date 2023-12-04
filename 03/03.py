import pathlib
from datetime import datetime
import re
import math

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2023, day=datetime.now().day)


def get_adjacent_cells(matrix, row, col, col_ignore):
    adjacent_cells = []
    for i in range(max(0, row - 1), min(row + 2, len(matrix))):
        for j in range(max(0, col - 1), min(col + 2, len(matrix[0]))):
            if i != row or j != col:
                if i == row and j in col_ignore:
                    continue
                adjacent_cells.append((i, j, matrix[i][j]))
    return adjacent_cells


def solve(input_lines):
    matrix = [list(line) for line in input_lines]
    numbers_with_special_chars = []
    numbers_wout_special_chars = []
    all_chars = set()
    all_special_chars = set()
    asterisk_coords = dict()
    for i, row in enumerate(input_lines):
        numbers_in_row = re.findall(r'\d+', row)
        if len(set(numbers_in_row)) != len(numbers_in_row):
            duplicates = dict()
            for ns in set(numbers_in_row):
                duplicates[ns] = 0
                for nl in numbers_in_row:
                    if ns == nl:
                        duplicates[ns] += 1
            # print(f"duplicates, row: {i}", [f"{k}:{v}" for k, v in duplicates.items() if v > 1])
        j_last_n = 0
        for n in numbers_in_row:
            j_start = j_last_n
            while True:
                j = row[j_start:].find(n) + j_start
                if j < j_last_n:
                    exit(1)
                j_last_n = j + len(n)
                break
            is_adjacent_to_special_char = False
            for n_pos in range(j, j + len(n)):
                if n_pos == j:
                    ignore_cols = range(j, j + 1)
                elif n_pos == j + 1:
                    ignore_cols = range(j -1, j + 1)
                else:
                    ignore_cols = range(j - 2, j +1)
                for x, y, char in get_adjacent_cells(matrix, i, n_pos, ignore_cols):
                    all_chars.add(char)
                    if not char.isalpha() and not char.isdigit() and char != ".":
                        all_special_chars.add(char)
                        numbers_with_special_chars.append(int(n))
                        # print("n", n)
                        is_adjacent_to_special_char = True
                        if char == "*":
                            default_value = dict(retries=0, numbers=[])
                            value = asterisk_coords.get(f"{x}:{y}", default_value)
                            value["retries"] += 1
                            value["numbers"].append(int(n))
                            asterisk_coords[f"{x}:{y}"] = value
                        break
                if is_adjacent_to_special_char:
                    break
            if not is_adjacent_to_special_char:
                numbers_wout_special_chars.append((i, j, int(n)))
    # print(numbers_wout_special_chars)
    # print(asterisk_coords)
    p2 = 0
    for k, v in asterisk_coords.items():
        if v["retries"] == 2:
            p2 += math.prod(v["numbers"])
    return sum(numbers_with_special_chars), p2


files = ["example.txt", input_file]

for f in files:
    list_input = read_input(f)
    # print(list_input)
    print(solve(list_input))
