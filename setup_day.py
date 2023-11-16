import os
import sys

day = int(sys.argv[1])

python_file = f"day{day:02}.py"
if os.path.exists(python_file):
    print(
        f"File {python_file} exists; not overwriting (but will create input files if they do not exist)"
    )
else:
    with open(python_file, "w") as f:
        f.write(
            f"""import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ''
    input_file = f'day{day:02}_test_input{{suffix}}.txt'
else:
    input_file = f'day{day:02}_input.txt'

data = utils.input_as_lines(input_file)
"""
        )

input_file = f"day{day:02}_input.txt"
if not os.path.exists(input_file):
    open(input_file, "w").close()

test_input_file = f"day{day:02}_test_input.txt"
if not os.path.exists(test_input_file):
    open(test_input_file, "w").close()
