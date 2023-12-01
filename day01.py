import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day01_test_input{suffix}.txt"
else:
    input_file = f"day01_input.txt"

data = utils.input_as_lines(input_file)


p1_sum = 0
for line in data:
    digits = [c for c in line if c.isnumeric()]
    if digits:
        val = int(f"{digits[0]}{digits[-1]}")
        p1_sum += val

print(f"Part 1: {p1_sum}")

numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

for i in range(10):
    numbers[str(i)] = i

p2_sum = 0
pos = 0

for line in data:
    digits = []
    for i in range(len(line)):
        for n, d in numbers.items():
            if line[i:].startswith(n):
                digits.append(d)
                break

    val = int(f"{digits[0]}{digits[-1]}")
    p2_sum += val

print(f"Part 2: {p2_sum}")
