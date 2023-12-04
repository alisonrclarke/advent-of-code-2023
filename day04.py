import sys
from collections import defaultdict

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day04_test_input{suffix}.txt"
else:
    input_file = f"day04_input.txt"

data = utils.input_as_lines(input_file)

p1_score = 0

for line in data:
    splits = line.split(":")[1].split("|")
    winners = [s for s in splits[0].strip().split(" ") if s]
    mine = [s for s in splits[1].strip().split(" ") if s]
    n_matches = len([s for s in mine if s in winners])
    if n_matches:
        p1_score += 2 ** (n_matches - 1)

print(f"Part 1: {p1_score}")

p2_score = 0
copies = defaultdict(lambda: 1)

for i, line in enumerate(data):
    splits = line.split(":")[1].split("|")
    winners = [s for s in splits[0].strip().split(" ") if s]
    mine = [s for s in splits[1].strip().split(" ") if s]
    n_matches = len([s for s in mine if s in winners])
    if n_matches:
        for j in range(i + 1, i + 1 + n_matches):
            copies[j + 1] += copies[i + 1]

for i in range(len(data)):
    p2_score += copies[i + 1]

print(f"Part 2: {p2_score}")
