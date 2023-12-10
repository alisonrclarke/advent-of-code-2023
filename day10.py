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

print(path[part1])
x_bounds = (min(p[0] for p in path), max(p[0] for p in path))
y_bounds = (min(p[1] for p in path), max(p[1] for p in path))
print(x_bounds, y_bounds)

possible_nests = {}

current_nest = None
for y in range(y_bounds[0], y_bounds[1] + 1):
    for x in range(x_bounds[0], x_bounds[1] + 1):
        # if not current_nest:
        surrounds = [(x, y - 1), (x-1, y), (x-1, y-1), (x+1, y-1)]
        current_nest = next(
            (k for k, n in possible_nests.items() if any(
                p in surrounds for p in n)),
            None
        )
        # print(x, y, current_nest)

        c = rows[y][x]
        if c == ".":
            if current_nest:
                possible_nests[current_nest].append((x, y))
            else:
                possible_nests[(x, y)] = [(x, y)]



p2_total = 0

for pos, nest in possible_nests.items():
    print()
    
    print(nest)
    for j, row in enumerate(rows):
        s = ""
        for i, c in enumerate(row):
            s += "0" if (i, j) in nest else row[i]

        print(s)
    print()
    out_of_bounds = False
    for n in nest:
        if n[0] < x_bounds[0] or n[0] > x_bounds[1] or n[1] < y_bounds[0] or n[1] > y_bounds[1]:
            out_of_bounds = True
            break

        # also if outside loop don't need to count
        row_path = [p[0] for p in path if p[1] == n[1]]
        row_bounds = (min(row_path), max(row_path))
        if n[0] < row_bounds[0] or n[0] > row_bounds[1]:
            out_of_bounds = True
            break

        col_path = [p[1] for p in path if p[0] == n[0]]
        col_bounds = (min(col_path), max(col_path))
        if n[1] < col_bounds[0] or n[1] > col_bounds[1]:
            out_of_bounds = True
            break

    if out_of_bounds:
        print("out of bounds")
        continue

    has_odd_count = False
    for n in nest:
        print(n, nest)
        count = 0
        print(x_bounds, (x_bounds[1] - x_bounds[0])/2 + x_bounds[0])
        if n[0] < (x_bounds[1] - x_bounds[0])/2 + x_bounds[0]:
            print("rtl")
            for i in range(n[0]-1, x_bounds[0]-2, -1):
                print(i, n[1])
                if (i, n[1]) in path:
                    print('in path')
                    idx = path.index((i, n[1]))
                    if i == n[0]-1 or ((i+1, n[1]) not in path[idx-1:idx+2]):
                        # breakpoint()
                        print('incrementing')
                        count += 1
        else:
            # Go left to right
            print("ltr")
            for i in range(n[0]+1, x_bounds[1]+2):
                print(i, n[1])
                if (i, n[1]) in path:
                    print('in path')
                    idx = path.index((i, n[1]))
                    if i == n[0]+1 or ((i-1, n[1]) not in path[idx-1:idx+2]):
                        # breakpoint()
                        print('incrementing')
                        count += 1

        # TODO: also check vertical counts?
        
        print("total times crossed", count)
        if count % 2 == 1:
            has_odd_count = True
            break
    
    if has_odd_count:
        p2_total += len(nest)
        print("total now", p2_total)

print(p2_total)
