import json
import os
import pathlib
import shutil
from heapq import heappop, heappush

import numpy as np
import requests

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
up_left = (-1, -1)
up_right = (-1, 1)
down_left = (1, -1)
down_right = (1, 1)

parent_path = pathlib.Path(__file__).parent.absolute()


def get_2d_arr(list_input, dtype):
    a = np.array(list(map(dtype, list_input[0])))
    a = np.expand_dims(a, axis=0)
    for n in list_input[1:]:
        len_diff = len(list_input[0]) - len(n)
        if len_diff:
            n = n.ljust(len(list_input[0]))
        a = np.append(a, [list(map(dtype, list(n)))], axis=0)
    return a


def get_directions_possible_of_xy(x, y, x_max, y_max, diag=True):
    directions_possible = []
    if x == 0 and y == 0:  # Top left corner
        if diag:
            directions_possible += [right, down, down_right]
        else:
            directions_possible += [right, down]
    elif x + 1 == x_max and y + 1 == y_max:  # Bottom right corner
        if diag:
            directions_possible += [up, left, up_left]
        else:
            directions_possible += [up, left]
    elif x == 0 and y + 1 == y_max:  # Top right corner
        if diag:
            directions_possible += [down, left, down_left]
        else:
            directions_possible += [down, left]
    elif x + 1 == x_max and y == 0:  # Bottom left corner
        if diag:
            directions_possible += [up, right, up_right]
        else:
            directions_possible += [up, right]
    elif x == 0:  # Top row
        if diag:
            directions_possible += [right, down, left, down_left, down_right]
        else:
            directions_possible += [right, down, left]
    elif y == 0:  # Lef column
        if diag:
            directions_possible += [up, right, down, down_right, up_right]
        else:
            directions_possible += [up, right, down]
    elif x + 1 == x_max:  # Bottom row
        if diag:
            directions_possible += [up, right, left, up_left, up_right]
        else:
            directions_possible += [up, right, left]
    elif y + 1 == y_max:  # Right column
        if diag:
            directions_possible += [up, down, left, up_left, down_left]
        else:
            directions_possible += [up, down, left]
    else:
        if diag:
            directions_possible += [
                up,
                right,
                down,
                left,
                down_left,
                down_right,
                up_right,
                up_left,
            ]
        else:
            directions_possible += [up, right, down, left]
    return directions_possible


def read_input(filename="example.txt", strip=True, sep="\n"):
    with open(filename) as f:
        if strip:
            inputs = f.read().strip().split(sep)
        else:
            inputs = f.read().split(sep)
    return inputs


def get_adjacent_data(a, node):
    x, y = node
    x_max = len(a) if isinstance(a, list) else a.shape[1]
    y_max = len(a[0]) if isinstance(a, list) else a.shape[1]
    dirs = get_directions_possible_of_xy(x, y, x_max, y_max, diag=False)
    adjacent_data = {}
    for d in dirs:
        adjacent_data[(x + d[0], y + d[1])] = a[x + d[0]][y + d[1]]
    return adjacent_data


def a_star_no_h(a, start, end):
    not_visited = [(0, start)]
    visited = {start}

    while not_visited:
        distance, node = heappop(not_visited)

        if node == end:
            return distance

        for neighbor, n_distance in get_adjacent_data(a, node).items():
            if neighbor not in visited:
                heappush(not_visited, (distance + n_distance, neighbor))

        visited.add(node)


def get_path_a_star(a, start, end):
    not_visited = {start}
    visited = set()
    distances = {start: 0}
    parents = {start: start}

    while not_visited:
        node = None

        for n in not_visited:
            if node is None or distances[n] < distances[node]:
                node = n

        if node is None:
            print("No path determined")
            return None

        if node == end:
            final_path = []

            while parents[node] != node:
                final_path.append(node)
                node = parents[node]

            final_path.append(start)
            final_path.reverse()

            return final_path

        for neighbor, distance in get_adjacent_data(a, node).items():
            if neighbor not in not_visited and neighbor not in visited:
                not_visited.add(neighbor)
                parents[neighbor] = node
                distances[neighbor] = distances[node] + distance
            else:
                if distances[neighbor] > distances[node] + distance:
                    distances[neighbor] = distances[node] + distance
                    parents[neighbor] = node
                    if neighbor in visited:
                        visited.remove(neighbor)
                        not_visited.add(neighbor)

        not_visited.remove(node)
        visited.add(node)

    print("No path determined")
    return None


def create_dirs_and_templates(overwrite=False):
    for i in range(1, 26):
        d_f_name = str(i).zfill(2)
        os.makedirs(d_f_name, exist_ok=True)
        py_file = os.path.join(d_f_name, d_f_name + ".py")
        ex_file = os.path.join(d_f_name, "example.txt")
        for s, d in zip(["template.py", "example.txt"], [py_file, ex_file]):
            if overwrite or not os.path.isfile(d):
                shutil.copyfile(s, d)


def _get_cookies_headers() -> dict[str, dict[str, str]]:
    with open(parent_path / ".env") as f:
        contents = json.loads(f.read().strip())
    return dict(
        cookies=contents, headers={"User-Agent": "https://github.com/mato1411/2023-AoC"}
    )


def get_input(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    r = requests.get(url, **_get_cookies_headers())
    print(f"Status code: {r.status_code}")
    print(parent_path / str(day).zfill(2) / "input.txt")
    with open(parent_path / str(day).zfill(2) / "input.txt", "w") as f:
        print(r.text)
        f.write(r.text)
    return r.text


if __name__ == "__main__":
    create_dirs_and_templates(overwrite=False)
