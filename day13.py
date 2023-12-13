import math
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day13_test_input{suffix}.txt"
else:
    input_file = f"day13_input.txt"

data = utils.input_as_lines(input_file)
data.append("")


def find_reflections(rows_or_cols, prev_ans=None):
    reflections = 0
    for i in range(0, len(rows_or_cols) - 1):
        # 0 => check r0 = r1 (sum 1, 1 check)
        # 1 => check r0 = r3 and r1 = r2 (sum 3, 2 checks)
        # 2 => check r0 = r5, r1=r4, r2=r3, (sum 5, 3 checks)
        # 3 => check r1 = r6, r2=r5, r3=r4, (sum 7, 3 checks)
        # 4 => (sum 9, 2 checks)
        # 5 => (sum 11, 1 checks = len(rows_or_cols)-1-i)
        j_range = min(i + 1, len(rows_or_cols) - 1 - i)

        if all(rows_or_cols[i - j] == rows_or_cols[i + j + 1] for j in range(j_range)):
            if prev_ans is None or i + 1 != prev_ans:
                return i + 1

    return None


pattern = []
p1_total = 0
p2_total = 0

for row in data:
    if row == "":
        # end of pattern - check for symmetry and reset
        if row_idx := find_reflections(pattern):
            p1_total += 100 * row_idx

        cols = [
            "".join([pattern[j][i] for j in range(len(pattern))])
            for i in range(len(pattern[0]))
        ]
        if col_idx := find_reflections(cols):
            p1_total += col_idx

        # Part 2 calculation:
        for j, r in enumerate(pattern):
            found = False
            for i, c in enumerate(r):
                new_c = "#" if c == "." else "."
                new_r_l = list(r)
                new_r_l[i] = new_c
                new_r = "".join(new_r_l)
                new_pattern = pattern[:j] + [new_r] + pattern[j + 1 :]
                # for r2 in new_pattern:
                #     print(r2)
                # print()

                row_idx2 = find_reflections(new_pattern, row_idx)
                if row_idx2 and row_idx2 != row_idx:
                    p2_total += 100 * row_idx2
                    # print(f"Found pattern with smudge at ({i}, {j}), row {row_idx2}")
                    found = True
                    break

                cols = [
                    "".join([new_pattern[j][i] for j in range(len(new_pattern))])
                    for i in range(len(new_pattern[0]))
                ]
                col_idx2 = find_reflections(cols, col_idx)
                if col_idx2 and col_idx2 != col_idx:
                    p2_total += col_idx2
                    # print(f"Found pattern with smudge at ({i}, {j}), col {col_idx2}")
                    found = True
                    break

            if found:
                break

        pattern = []
    else:
        pattern.append(row)

print(f"Part 1: {p1_total}")
print(f"Part 2: {p2_total}")
