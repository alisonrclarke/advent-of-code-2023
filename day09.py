import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day09_test_input{suffix}.txt"
else:
    input_file = f"day09_input.txt"

data = utils.input_as_lines(input_file)


part_1_total = 0
part_2_total = 0

for line in data:
    current_vals = [int(s) for s in line.split(" ")]
    first_vals = [current_vals[0]]
    last_vals = [current_vals[-1]]

    while not all(n == 0 for n in current_vals):
        next_vals = [current_vals[i + 1] - n for i, n in enumerate(current_vals[:-1])]
        first_vals.append(next_vals[0])
        last_vals.append(next_vals[-1])
        current_vals = next_vals

    p1_total = 0
    for n in reversed(last_vals):
        p1_total += n

    part_1_total += p1_total

    first_vals.reverse()
    prev = 0
    for i, n in enumerate(first_vals):
        val = n if i == 0 else n - prev
        prev = val

    part_2_total += val


print(f"Part 1: {part_1_total}")
print(f"Part 2: {part_2_total}")
