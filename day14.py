import functools
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day14_test_input{suffix}.txt"
else:
    input_file = f"day14_input.txt"

data = utils.input_as_lines(input_file)


@functools.cache
def move_to_start(s: str, reverse_=False):
    if reverse_:
        l = list(s)
        l.reverse()
        s = "".join(l)

    splits = s.split("#")
    new_splits = []
    for s2 in splits:
        n = len([c for c in s2 if c == "O"])
        new_splits.append("O" * n + "." * (len(s2) - n))

    new_s = "#".join(new_splits)
    if reverse_:
        l = list(new_s)
        l.reverse()
        return "".join(l)
    else:
        return new_s


def get_score(s):
    total = 0
    for i, c in enumerate(s):
        if c == "O":
            # print(f"rock in row {i}, score {len(s) - i}")
            total += len(s) - i
    return total


def transpose(rows_or_cols: list[str]):
    cols_or_rows = [""] * len(rows_or_cols)
    for row_or_col in rows_or_cols:
        for i, c in enumerate(row_or_col):
            cols_or_rows[i] += c
    return cols_or_rows


# Get data as column strings to make re-ordering to the north easier
cols = transpose(data)

p1_total = 0
for col in cols:
    new_col = move_to_start(col)
    p1_total += get_score(new_col)

print(f"Part 1: {p1_total}")

# Part 2 - spin!
cycles = []
final_cols = None
for n in range(1000000000):
    # Move north
    for j, col in enumerate(cols):
        cols[j] = move_to_start(col)

    # Move west - back to rows
    rows = transpose(cols)
    for i, row in enumerate(rows):
        rows[i] = move_to_start(row)

    # Move south - back to cols
    cols = transpose(rows)
    for j, col in enumerate(cols):
        cols[j] = move_to_start(col, reverse_=True)

    # Move east - back to rows
    rows = transpose(cols)
    for i, row in enumerate(rows):
        rows[i] = move_to_start(row, reverse_=True)

    # Back to cols for start
    cols = transpose(rows)

    cycle_string = "".join(cols)
    if cycle_string in cycles:
        # We have a loop! Can work out final state from here
        cycle_index = cycles.index(cycle_string)
        cycle_length = len(cycles) - cycle_index
        remaining_cycles = 1000000000 - n
        cycles_to_add = remaining_cycles % cycle_length
        last_state = cycles[cycles_to_add - cycle_length - 1]
        final_cols = [
            last_state[i : i + len(cols[0])]
            for i in range(0, len(last_state), len(cols[0]))
        ]
        break

    cycles.append(cycle_string)


p2_total = 0
for col in final_cols:
    p2_total += get_score(col)

print(f"Part 2: {p2_total}")
