import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day11_test_input{suffix}.txt"
else:
    input_file = f"day11_input.txt"

data = utils.input_as_lines(input_file)

galaxies = []
empty_rows = []
empty_cols = []

for j, row in enumerate(data):
    row_galaxies = [complex(i, j) for i, c in enumerate(row) if c == "#"]
    if row_galaxies:
        galaxies.extend(row_galaxies)
    else:
        empty_rows.append(j)

# Check for empty cols
for i in range(len(data[0])):
    galaxy_in_col = next((g for g in galaxies if g.real == i), None)
    if not galaxy_in_col:
        empty_cols.append(i)

# Iterate over galaxies
p1_total = 0
for i, g1 in enumerate(galaxies):
    for g2 in galaxies[i + 1 :]:
        diff = g2 - g1

        row_dist = abs(diff.real)
        for j in empty_cols:
            if (j > g1.real and j < g2.real) or (j > g2.real and j < g1.real):
                row_dist += 1

        col_dist = abs(diff.imag)
        for j in empty_rows:
            if (j > g1.imag and j < g2.imag) or (j > g2.imag and j < g1.imag):
                col_dist += 1

        p1_total += row_dist + col_dist

print(f"Part 1: {p1_total}")

# Part 2
p2_total = 0
for i, g1 in enumerate(galaxies):
    for g2 in galaxies[i + 1 :]:
        diff = g2 - g1

        row_dist = abs(diff.real)
        for j in empty_cols:
            if (j > g1.real and j < g2.real) or (j > g2.real and j < g1.real):
                row_dist += 999999

        col_dist = abs(diff.imag)
        for j in empty_rows:
            if (j > g1.imag and j < g2.imag) or (j > g2.imag and j < g1.imag):
                col_dist += 999999

        p2_total += row_dist + col_dist

print(f"Part 2: {p2_total}")
