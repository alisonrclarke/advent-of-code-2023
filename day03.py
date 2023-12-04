import operator
import re
import sys
from functools import reduce

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day03_test_input{suffix}.txt"
else:
    input_file = f"day03_input.txt"

data = utils.input_as_lines(input_file)

p1_sum = 0

symbols_re = re.compile(r"[^\d\.]")

for j, row in enumerate(data):
    current_number = ""
    has_adjacent_symbol = False
    r_len = len(row)
    for i, c in enumerate(row):
        if c.isdigit():
            current_number += c
            # check for adjacent symbols
            if not has_adjacent_symbol:
                if (
                    j > 0
                    and (
                        (i > 0 and symbols_re.match(data[j - 1][i - 1]))
                        or symbols_re.match(data[j - 1][i])
                        or (i < r_len - 1 and symbols_re.match(data[j - 1][i + 1]))
                    )
                    or (
                        (i > 0 and symbols_re.match(data[j][i - 1]))
                        or (i < r_len - 1 and symbols_re.match(data[j][i + 1]))
                    )
                    or (
                        j < len(data) - 1
                        and (
                            (i > 0 and symbols_re.match(data[j + 1][i - 1]))
                            or symbols_re.match(data[j + 1][i])
                            or (i < r_len - 1 and symbols_re.match(data[j + 1][i + 1]))
                        )
                    )
                ):
                    has_adjacent_symbol = True
        else:
            if current_number and has_adjacent_symbol:
                p1_sum += int(current_number)
            current_number = ""
            has_adjacent_symbol = False

        # Get number at end of row
        if i == r_len - 1 and current_number and has_adjacent_symbol:
            p1_sum += int(current_number)


print(f"Part 1: {p1_sum}")


def find_numbers(s, i):
    """Find a number or numbers in string s around s[i]"""
    n_0 = ""
    k = i - 1
    while k >= 0:
        if s[k].isdigit():
            n_0 = s[k] + n_0
            k -= 1
        else:
            break

    n_1 = ""
    k = i + 1
    while k < len(s):
        if s[k].isdigit():
            n_1 += s[k]
            k += 1
        else:
            break

    if s[i].isdigit():
        return [int(n_0 + s[i] + n_1)]
    else:
        return [int(n) for n in [n_0, n_1] if n]


p2_sum = 0

gear_locations = []

for j, row in enumerate(data):
    current_number = ""
    has_adjacent_symbol = False
    r_len = len(row)
    for i, c in enumerate(row):
        if c == "*":
            numbers = []
            # we have a gear: look for adjacent numbers
            if j > 0 and any([c2.isdigit() for c2 in data[j - 1][i - 1 : i + 2]]):
                numbers.extend(find_numbers(data[j - 1], i))
            if i > 0 and data[j][i - 1].isdigit():
                numbers.extend(find_numbers(data[j][:i], i - 1))
            if i < r_len and data[j][i + 1].isdigit():
                numbers.extend(find_numbers(data[j][i + 1 :], 0))
            if j < len(data) - 1 and any(
                [c2.isdigit() for c2 in data[j + 1][i - 1 : i + 2]]
            ):
                numbers.extend(find_numbers(data[j + 1], i))

            # TODO: check length of numbers and multiply
            print(j, i, numbers)
            if len(numbers) > 1:
                p2_sum += reduce(operator.mul, numbers, 1)


print(f"Part 2: {p2_sum}")
