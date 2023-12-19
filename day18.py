import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day18_test_input{suffix}.txt"
else:
    input_file = f"day18_input.txt"

data = utils.input_as_lines(input_file)


def find_loop(positions_touched):
    # Work across rows to determine which positions are inside path
    x_vals = [int(p.real) for p in positions_touched]
    y_vals = [int(p.imag) for p in positions_touched]
    x_range = range(min(x_vals), max(x_vals) + 1)
    y_range = range(min(y_vals), max(y_vals) + 1)

    total = 0
    for j in y_range:
        line_total = 0
        in_loop = False
        # s = ""  # For debugging
        for i in x_range:
            if complex(i, j) in positions_touched:
                # Check if there's a line N of here - if so, change state
                if complex(i, j - 1) in positions_touched:
                    in_loop = not in_loop

            if complex(i, j) in positions_touched or in_loop:
                total += 1
                line_total += 1

            # s += '#' if complex(i, j) in positions_touched else '.'
        # print(s, line_total)
    return total


def find_loop2(path: list):
    # breakpoint()
    # Path is a list of corners touched in order, not every tile touched
    # Work across rows to determine which positions are inside path
    x_vals = sorted(set([int(p.real) for p in path]))
    y_vals = sorted(set([int(p.imag) for p in path]))
    x_range = range(min(x_vals), max(x_vals) + 1)
    y_range = range(min(y_vals), max(y_vals) + 1)

    total = 0
    for y_idx, j in enumerate(y_vals):
        line_total = 0
        in_loop = False
        # s = ""  # For debugging
        i = x_vals[0]
        x_idx = 0
        while i < x_vals[-1] and x_idx < len(x_vals):
            print(f"({i}, {j})")
            i = x_vals[x_idx]
            if complex(i, j) in path:
                # we're at a corner - check which way
                path_index = path.index(complex(i, j))
                next_pos = path[path_index + 1 % len(path)]
                prev_pos = path[path_index - 1 % len(path)]
                if next_pos.imag == j or prev_pos.imag == j:
                    # Next pos is on the same row, so add distance between them to total
                    if next_pos.imag == j:
                        line_total += abs(next_pos.real - i) + 1
                        i = max(next_pos.real, i)
                    else:
                        line_total += abs(prev_pos.real - i) + 1
                        i = max(prev_pos.real, i)
                    # breakpoint()
                    print(f"x_idx is: {x_idx}")
                    x_idx = next(
                        (x_idx + idx for idx, x in enumerate(x_vals[x_idx:]) if x >= i),
                        len(x_vals),
                    )
                    print(f"x_idx now {x_idx} (after incrementing for i)")
                    in_loop = True
                else:
                    # Next pos is up or down
                    line_total += 1
                    in_loop = not in_loop

            elif in_loop:
                print(f"in loop, {i}, {j}, adding ", (i - x_vals[x_idx - 1]))
                line_total += i - x_vals[x_idx - 1]
                # breakpoint()

            # increase index
            x_idx += 1

        print("Line total", j, line_total)
        # duplicate line_value until next y_val
        if y_idx < len(y_vals) - 1:
            # FIXME: can't do this - see row 3 in example
            # Just use every y?
            print(f"Adding next {(y_vals[y_idx+1] - j - 1)} rows with same total")
            total += (y_vals[y_idx + 1] - j - 1) * line_total

    return total


direction_map = {"R": 1, "L": -1, "D": 1j, "U": -1j}
pos = 0
positions_touched = {pos}
path = [0]
for line in data:
    direction, steps, colour = line.split(" ")
    step = direction_map[direction]
    n_steps = int(steps)
    path.append(pos + n_steps * step)
    for i in range(n_steps):
        pos += step
        positions_touched.add(pos)

p1_total = find_loop(positions_touched)
print(f"Part 1: {p1_total}")

p1_total_2 = find_loop2(path)
print(f"Part 1 (using find_loop2): {p1_total_2}")


# Part 2
direction_map2 = {"0": 1, "1": 1j, "2": -1, "3": -1j}

pos = 0
path = [0]
for line in data:
    # print(line.rsplit(' ', maxsplit=1))
    instruction = line.rsplit(" ", maxsplit=1)[1]
    n_steps = int(instruction[2:7], 16)
    step = direction_map2[instruction[7]]
    # print(n_steps, step)

    pos += n_steps * step
    path.append(pos)

# Too slow for part 2; Change this to a sparse map and just keep track of corners/directions?

# p2_total = find_loop2(positions_touched)
# print(f"Part 2: {p2_total}")
