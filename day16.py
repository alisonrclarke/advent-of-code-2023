import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day16_test_input{suffix}.txt"
else:
    input_file = f"day16_input.txt"

data = utils.input_as_lines(input_file)

# Hmmm....
sys.setrecursionlimit(50000)


def find_path(positions: list[tuple[complex, complex]], visited):
    if not positions:
        return visited

    current, previous = positions.pop()
    # print("find_path", current, previous, len(positions), len(visited))
    if (current, previous) in visited:
        # print("Already found")
        return find_path(positions, visited)

    # Check current is in range - just carry on with next position if not
    if (
        current.real < 0
        or current.real >= len(data[0])
        or current.imag < 0
        or current.imag >= len(data)
    ):
        return find_path(positions, visited)

    prev_move = current - previous
    current_symbol = data[int(current.imag)][int(current.real)]
    next = []
    if current_symbol == ".":
        next.append(current + prev_move)
    elif current_symbol == "\\":
        if prev_move == 1:
            # has moved E to this symbol - bounce S
            next.append(current + 1j)
        elif prev_move == -1:
            # has moved W to this symbol - bounce N
            next.append(current - 1j)
        elif prev_move == 1j:
            # has moved S to this symbol - bounce E
            next.append(current + 1)
        else:
            # has moved N to this symbol - bounce W
            next.append(current - 1)
    elif current_symbol == r"/":
        if prev_move == 1:
            # has moved E to this symbol - bounce N
            next.append(current - 1j)
        elif prev_move == -1:
            # has moved W to this symbol - bounce S
            next.append(current + 1j)
        elif prev_move == 1j:
            # has moved S to this symbol - bounce W
            next.append(current - 1)
        else:
            # has moved N to this symbol - bounce E
            next.append(current + 1)
    elif current_symbol == "|":
        if prev_move.real == 0:
            # Moving vertically so just keep going
            next.append(current + prev_move)
        else:
            # Split N/S
            next.extend([current + 1j, current - 1j])
    elif current_symbol == "-":
        if prev_move.imag == 0:
            # Moving horizontally so just keep going
            next.append(current + prev_move)
        else:
            # Split E/W
            next.extend([current + 1, current - 1])
    else:
        print("Help!")
        breakpoint()

    positions.extend([(n, current) for n in next])
    visited.add((current, previous))
    new_visited = find_path(positions, visited)
    return new_visited


# for line in data:
#     print(line)
# print()

all_visited = find_path([(0 + 0j, -1 + 0j)], set())
visited_positions = set([v[0] for v in all_visited])

# for j, row in enumerate(data):
#     s = ''
#     for i, c in enumerate(row):
#         if complex(i, j) in visited_positions:
#             s += '#'
#         else:
#             s += '.'
#     print(s)

print(f"Part 1: {len(visited_positions)}")

# Part 2: iterate
max_val = 0

for j in range(len(data)):
    # From left
    all_visited = find_path([(complex(0, j), complex(-1, j))], set())
    val = len(set([v[0] for v in all_visited]))
    max_val = max(max_val, val)

    # From right
    n = len(data[0]) - 1
    all_visited = find_path([(complex(n, j), complex(n + 1, j))], set())
    val = len(set([v[0] for v in all_visited]))
    max_val = max(max_val, val)

for i in range(len(data[0])):
    # From top
    all_visited = find_path([(complex(i, 0), complex(i, -1))], set())
    val = len(set([v[0] for v in all_visited]))
    max_val = max(max_val, val)

    # From right
    n = len(data) - 1
    all_visited = find_path([(complex(i, n), complex(i, n + 1))], set())
    val = len(set([v[0] for v in all_visited]))
    max_val = max(max_val, val)

print(f"Part 2: {max_val}")
