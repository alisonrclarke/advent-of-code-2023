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

# Part 2: find enclosed spaces
p2_total = 0

x_bounds = (min(p[0] for p in path), max(p[0] for p in path))
y_bounds = (min(p[1] for p in path), max(p[1] for p in path))

# Replace start_pos in grid with actual val
start_char = None
neighbours = sorted([path[1], path[-2]])
dist = (path[1][0] - path[-2][0], path[1][1] - path[-2][1])

if dist[1] == 0:  # same row
    start_char = "-"
elif dist[0] == 0:  # same col
    start_char = "|"
elif dist == (1, -1):
    start_char = "F" if neighbours[0][0] == start_pos[0] else "J"
else:
    start_char = "7" if neighbours[0][0] == start_pos[0] else "L"

rows[start_pos[1]] = rows[start_pos[1]].replace("S", start_char)

# Iterate over rows from left to right, counting times we traverse the loop
# to work out whether we're inside
for j, row in enumerate(rows):
    in_loop = False
    s = ""  # For printing
    for i, c in enumerate(row + "."):
        if (i, j) in path:
            # Only count paths that escape upwards as ones that change the state, to avoid double-counting the edges
            if c in ("L", "|", "J"):
                in_loop = not in_loop
        else:
            if in_loop:
                p2_total += 1

        s += c if (i, j) in path else ("0" if in_loop else ".")

    print(s)

print(f"Part 2: {p2_total}")
