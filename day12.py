import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ''
    input_file = f'day12_test_input{suffix}.txt'
else:
    input_file = f'day12_input.txt'

data = utils.input_as_lines(input_file)

for line in data:
    chars, cond = line.split()