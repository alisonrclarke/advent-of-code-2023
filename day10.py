import math
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day10_test_input{suffix}.txt"
else:
    input_file = f"day10_input.txt"

rows = utils.input_as_lines(input_file)

# use pos as (x, y) where x is col number and y is row number
# so index in rows is rows[y][x]
start_pos = next(
    (i, j) for j, row in enumerate(rows) for i, c in enumerate(row) if c == "S"
)

print(f"Start pos: {start_pos}")
current_pos = start_pos

# Work out where we can go from current_pos
# Just find the first pos and go round the loop
next_pos = None
if rows[current_pos[1] - 1][current_pos[0]] in ["|", "7", "F"]:
    next_pos = (current_pos[0], current_pos[1] - 1)
elif rows[current_pos[1]][current_pos[0] - 1] in ["-", "L", "F"]:
    next_pos = (current_pos[0] - 1, current_pos[1])
elif rows[current_pos[1]][current_pos[0] + 1] in ["-", "J", "7"]:
    next_pos = (current_pos[0] + 1, current_pos[1])
elif rows[current_pos[1] + 1][current_pos[0]] in ["|", "J", "L"]:
    next_pos = (current_pos[0], current_pos[1] + 1)
else:
    print("Couldn't find next pos")
    sys.exit(1)

print(f"Next pos: {next_pos}")

path = [start_pos, next_pos]

while next_pos != start_pos:
    current_pos = path[-1]
    prev_pos = path[-2]
    c = rows[current_pos[1]][current_pos[0]]
    if c == "-":
        if prev_pos == (current_pos[0] - 1, current_pos[1]):
            next_pos = (current_pos[0] + 1, current_pos[1])
        else:
            next_pos = (current_pos[0] - 1, current_pos[1])
    elif c == "|":
        if prev_pos == (current_pos[0], current_pos[1] - 1):
            next_pos = (current_pos[0], current_pos[1] + 1)
        else:
            next_pos = (current_pos[0], current_pos[1] - 1)
    elif c == "L":
        if prev_pos == (current_pos[0] + 1, current_pos[1]):
            next_pos = (current_pos[0], current_pos[1] - 1)
        else:
            next_pos = (current_pos[0] + 1, current_pos[1])
    elif c == "J":
        if prev_pos == (current_pos[0] - 1, current_pos[1]):
            next_pos = (current_pos[0], current_pos[1] - 1)
        else:
            next_pos = (current_pos[0] - 1, current_pos[1])
    elif c == "7":
        if prev_pos == (current_pos[0] - 1, current_pos[1]):
            next_pos = (current_pos[0], current_pos[1] + 1)
        else:
            next_pos = (current_pos[0] - 1, current_pos[1])
    elif c == "F":
        if prev_pos == (current_pos[0] + 1, current_pos[1]):
            next_pos = (current_pos[0], current_pos[1] + 1)
        else:
            next_pos = (current_pos[0] + 1, current_pos[1])
    else:
        print("Unknown char {c}")
        break

    path.append(next_pos)

part1 = int((len(path) - 1) / 2)
print(f"Part 1: {part1}")

