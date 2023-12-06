import re
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day06_test_input{suffix}.txt"
else:
    input_file = f"day06_input.txt"

data = utils.input_as_lines(input_file)
times = [int(s) for s in re.split(r"\s+", re.split(r":\s+", data[0])[1])]
distances = [int(s) for s in re.split(r"\s+", re.split(r":\s+", data[1])[1])]
assert len(times) == len(distances)

p1_total = 1
for i, t in enumerate(times):
    winning_moves = 0
    d = distances[i]
    for j in range(t + 1):
        d2 = j * (t - j)
        if d2 > d:
            winning_moves += 1
            # FIXME: could break here and calculate number
    p1_total *= winning_moves

print(f"Part 1: {p1_total}")

# Part 2
time = int("".join([s for s in re.split(r"\s+", re.split(r":\s+", data[0])[1])]))
distance = int("".join([s for s in re.split(r"\s+", re.split(r":\s+", data[1])[1])]))

winning_moves = 0
for j in range(time + 1):
    d2 = j * (time - j)
    if d2 > distance:
        winning_moves += 1
        # FIXME: could break here and calculate number

print(f"Part 2: {winning_moves}")
