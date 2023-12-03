import re
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day02_test_input{suffix}.txt"
else:
    input_file = f"day02_input.txt"

data = utils.input_as_lines(input_file)

game_re = re.compile(r"^Game (\d+): (.+)$")

p1_total = 0

for line in data:
    matches = game_re.match(line)
    game_no = int(matches.group(1))
    rounds = matches.group(2).split("; ")
    is_possible = True

    for round in rounds:
        colours = [s.split(" ") for s in round.split(", ")]
        for c in colours:
            n = int(c[0])
            if (
                (c[1] == "red" and n > 12)
                or (c[1] == "green" and n > 13)
                or (c[1] == "blue" and n > 14)
            ):
                is_possible = False
                break

        if not is_possible:
            break

    if is_possible:
        p1_total += game_no

print(f"Part 1: {p1_total}")

p2_total = 0

for line in data:
    matches = game_re.match(line)
    game_no = int(matches.group(1))
    rounds = matches.group(2).split("; ")
    is_possible = True

    mins = {"red": 1, "green": 1, "blue": 1}

    for round in rounds:
        colours = [s.split(" ") for s in round.split(", ")]
        for c in colours:
            n = int(c[0])
            colour = c[1]
            mins[colour] = max(mins[colour], n)

    power = 1
    for v in mins.values():
        power *= v

    p2_total += power

print(f"Part 2: {p2_total}")
