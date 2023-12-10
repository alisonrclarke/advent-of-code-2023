import math
import re
import sys
from collections import defaultdict

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day08_test_input{suffix}.txt"
else:
    input_file = f"day08_input.txt"

data = utils.input_as_lines(input_file)

instructions = data[0]

paths = {}
part2_start_nodes = []

line_re = re.compile(r"(\w+) = \((\w+), (\w+)\)")
for line in data[2:]:
    m = line_re.match(line)
    paths[m.group(1)] = (m.group(2), m.group(3))
    if m.group(1)[-1] == "A":
        part2_start_nodes.append(m.group(1))


current = "AAA"
i = 0

# while True:
#     next_inst = instructions[i % len(instructions)]
#     i += 1
#     # Get path
#     if next_inst == 'L':
#         current = paths[current][0]
#     else:
#         current = paths[current][1]
#
#     if current == 'ZZZ':
#         break

print(f"Part 1: {i}")

# Part 2

current_nodes = part2_start_nodes
i = 0

shortest_paths = []
for n in part2_start_nodes:
    i = 0
    current = n
    current_path = [n]
    shortest_path = None

    while True:
        next_inst = instructions[i % len(instructions)]
        i += 1

        # Get path
        if next_inst == "L":
            current = paths[current][0]
        else:
            current = paths[current][1]

        current_path.append(current)

        if current[-1] == "Z":
            if shortest_path is None:
                shortest_path = i
                # print("Got a path, going round again to check how long it takes")
            else:
                # We've got to the end point again, so we can check that it took the same numebr of steps. This means that the LCM
                # method will work.
                # print(f"Got here again; i is now {i}, shortest_path {shortest_path}, i / shortest_path = {i / shortest_path}")
                assert i / shortest_path == 2
                break

    shortest_paths.append(shortest_path)

# OK, so we can use LCM to find the shortest path for all original items
print(f"Part 2: {math.lcm(*shortest_paths)}")
