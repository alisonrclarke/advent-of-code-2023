import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day17_test_input{suffix}.txt"
else:
    input_file = f"day17_input.txt"

data = utils.input_as_lines(input_file)

# Hmmm....
sys.setrecursionlimit(50000)

# Map from path of up to 3 values to min dist to end_pos
visited = {}


def find_shortest_path(
    current_path: list[complex], end_pos, next_positions: list[list], current_min
):
    global visited
    # current_path is last 3 positions in path
    # next_positions is next steps from current_path
    # visited maps paths of 3 steps to minimum values
    current_pos = current_path[-1]
    if not next_positions:
        if current_pos == end_pos:
            return current_min
        else:
            breakpoint()

    try:
        current_value = data[int(current_pos.imag)][int(current_pos.real)]
    except:
        breakpoint()
    next_pos = next_positions.pop()
    # print("find_path", current, previous, len(next_positions), len(visited))
    next_path = current_path[-2:] + [next_pos]
    next_path_hash = str(next_path)
    if next_path_hash in visited:
        # print("Already found")
        next_min = visited[next_path_hash]
    else:
        # FIXME: Work out next positions?
        next_positions = []
        for step in (1, -1, 1j, -1j):
            # Get next possible position and check it's valid
            # (in range and not 3 steps in same direction)
            # TODO: avoid doubling back
            next_next_pos = next_pos + step
            next_next_path = [next_next_pos] + current_path[:2]
            print(next_next_pos, len(data[0]), len(data))
            print(next_next_pos.real < len(data[0]))
            print(next_next_pos.imag < len(data))
            if (
                next_next_pos != current_pos
                and next_next_pos.real >= 0
                and next_next_pos.real < len(data[0])
                and next_next_pos.imag >= 0
                and next_next_pos.imag < len(data)
                and not all(
                    next_next_path[i + 1] - next_next_path[i] == step
                    for i in range(len(current_path))
                )
            ):
                print("OK, adding")
                next_positions.append(next_next_pos)

        next_min = find_shortest_path(next_path, end_pos, next_positions, 999999999)

    min_value = min(current_value + next_min, current_min)
    visited[next_path] = min_value
    return min_value


def find_shortest_path2(current_pos, end_pos, queue):
    global visited
    # current_path is last 3 positions in path
    # next_positions is next steps from current_path
    # visited maps paths of 3 steps to minimum values


# Set up queue - for each point, every path of length 3 that gets to it
def find_paths_len_n(current_path, n):
    print(current_path, n)
    pos = current_path[-1]
    if n == 0:
        return []

    paths = []
    for step in (1, -1, 1j, -1j):
        # Get next possible position and check it's valid
        # (in range and not 3 steps in same direction)
        next_pos = pos + step
        prev_pos = current_path[-1] if current_path else None
        next_path = [next_pos] + current_path[:n]
        # print(next_pos, all(next_path[i+1] - next_path[i] == step for i in range(len(current_path))))
        has_3_same_steps = len(next_path) > 2 and all(
            next_path[i + 1] - next_path[i] == step for i in range(len(next_path))
        )
        # print(next_path, has_3_same_steps)

        if (
            next_pos not in current_path
            and next_pos.real >= 0
            and next_pos.real < len(data[0])
            and next_pos.imag >= 0
            and next_pos.imag < len(data)
            and not has_3_same_steps
        ):
            paths.append(next_path)
            print(f"Adding {next_path}")  # This sort of looks OK for the total paths?

    # print(paths)

    all_paths = []
    for p in paths:
        n_minus_one_paths = find_paths_len_n(p, n - 1)
        print(f"Paths for n-1: {n_minus_one_paths}")  # Not getting anything returned
        for p2 in n_minus_one_paths:
            all_paths.append([p] + p2)

    print(all_paths)
    return all_paths


queue = find_paths_len_n([0], 3)
print(len(queue))

# Get queue working, then try wiki's Dijkstra algorithm as loop.
# queue holds all possible 3-step paths, so can use as vertices
#
#
# end_pos = complex(len(data[0])-1, len(data)-1)
# min_value = find_shortest_path([0], end_pos, [1, 1j], 999999999)
# print(f"Part 1: {min_value}")
