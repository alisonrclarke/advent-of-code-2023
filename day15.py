import re
import sys
from collections import OrderedDict

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day15_test_input{suffix}.txt"
else:
    input_file = f"day15_input.txt"

data = utils.input_as_string(input_file)


def hash_algorithm(s):
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value


p1_total = 0
p2_total = 0
boxes = [OrderedDict() for _ in range(256)]

for s in data.split(","):
    p1_total += hash_algorithm(s)

    label, focal_length_s = re.split(r"-|=", s)
    box_no = hash_algorithm(label)
    focal_length = int(focal_length_s) if focal_length_s else None
    box = boxes[box_no]

    if focal_length is None:
        # No focal length, must be a -
        if label in box:
            del box[label]

    else:
        # Think this does both steps in an ordereddict?
        box[label] = focal_length

p2_total = 0
for box in boxes:
    for i, (label, focal_length) in enumerate(box.items()):
        p2_total += (hash_algorithm(label) + 1) * (i + 1) * focal_length


print(f"Part 1: {p1_total}")
print(f"Part 2: {p2_total}")
