import multiprocessing
import pathlib
from datetime import datetime

from utils import get_input, read_input


def get_map_ranges(raw_lists):
    ranges = []
    for l in raw_lists:
        n_l = [int(l) for l in l.split(sep=" ")]
        src = range(n_l[1], n_l[1] + n_l[2])
        dest = range(n_l[0], n_l[0] + n_l[2])
        ranges.append((src,dest))
    return ranges


def get_locations(kwargs):
    seeds = kwargs.get("seeds", [])
    map_ranges = kwargs.get("map_ranges", dict())
    #locations = []
    min_loc = -1
    print(seeds)
    for s in seeds:
        #linked_list = dict()
        #print(s)
        map_dest = "seed"
        while map_dest != "location":
            map_src = map_dest
            #print(map_dest)
            #linked_list[map_src] = s
            map_k = [k for k in map_ranges.keys() if k.startswith(map_src)][0]
            map_dest = map_k.replace(f"{map_src}-to-", "").split(" ")[0]
            #print(map_ranges[map_k])
            for r in map_ranges[map_k]:
                #print(r[0])
                d = r[1][r[0].index(s)] if s in r[0] else s
                if d != s:
                    break
            s = d
            #print(f"{s} - {r} - {d}")
        #linked_list[map_dest] = d
        #locations.append(d)
        min_loc = d if d < min_loc or min_loc == -1 else min_loc
    #print("ll", linked_list)
    return min_loc


def main():
    input_file = "input.txt"

    if not pathlib.Path(input_file).exists():
        str_input = get_input(year=2023, day=datetime.now().day)

    files = ["example.txt", input_file]

    for f in files:
        list_input = read_input(f, sep="\n\n")
        inputs = dict()
        for lines in list_input:
            inputs[lines.split(sep=":")[0]] = lines.split(sep=":")[1].strip().split(sep="\n")
        #print(inputs)
        map_ranges = dict()
        for map in inputs.keys():
            if "map" in map:
                ranges = get_map_ranges(inputs[map])
                #ranges = get_map_ranges_dedup(inputs[map])
                #print(ranges)
                map_ranges[map] = ranges
        p1_seeds = [int(n) for s in inputs["seeds"] for n in s.split(sep=" ")]
        #print(map_ranges)
        p1 = get_locations(dict(seeds=set(p1_seeds), map_ranges=map_ranges))

        print(f"{f} - Part 1: {p1}")
        p2_seeds = []
        #print(len(p1_seeds))
        for i in range(0, len(p1_seeds), 2):
            #print(i)
            #print(range(p1_seeds[i], p1_seeds[i]+p1_seeds[i+1]))
            # Works example but not input
            #p2_seeds += list(range(p1_seeds[i], p1_seeds[i]+p1_seeds[i+1]))
            p2_seeds.append(range(p1_seeds[i], p1_seeds[i]+p1_seeds[i+1]))
        #print(p2_seeds)
        #print(len(p2_seeds))
        p2_seeds = sorted(p2_seeds, key=lambda x: x.start) # merge_ranges(p2_seeds)
        #print(p2_seeds)
        #print(len(p2_seeds))
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            p2_locations = pool.map(get_locations, [dict(seeds=p2, map_ranges=map_ranges) for p2 in p2_seeds])
        print(f"{f} - Part 2: {min(p2_locations)}")


if __name__ == "__main__":
    main()
