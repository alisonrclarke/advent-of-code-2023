import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day05_test_input{suffix}.txt"
else:
    input_file = f"day05_input.txt"

data = utils.input_as_lines(input_file)

seeds = [int(s) for s in data[0].split(": ")[1].split(" ")]
current_objs = seeds.copy()
next_objs = seeds.copy()

for line in data[2:]:
    if line == "":
        # end of section; add remaining objects as-is
        next_objs.extend(current_objs)
    elif "map:" in line:
        # set up new section
        current_objs = next_objs
        next_objs = []
    else:
        # line is: dest source range
        dst, src, rge = [int(s) for s in line.split(" ")]
        for i, obj in enumerate(current_objs.copy()):
            if obj >= src and obj < (src + rge):
                next_objs.append(dst + obj - src)
                current_objs.remove(obj)

next_objs.extend(current_objs)
print(f"Part 1: {min(next_objs)}")


# Part 2:
seed_ranges = [int(s) for s in data[0].split(": ")[1].split(" ")]
seeds = []
for i in range(int(len(seed_ranges) / 2)):
    seeds.append((seed_ranges[2 * i], seed_ranges[2 * i + 1]))

current_objs = seeds.copy()
next_objs = seeds.copy()

for line in data[2:]:
    if line == "":
        # end of section; add remaining objects as-is
        next_objs.extend(current_objs)
    elif "map:" in line:
        # set up new section
        # Filter out objects with range 0 (easier here than working out where I went wrong below)
        current_objs = [o for o in next_objs if o[1] > 0]
        next_objs = []
    else:
        # line is: dest source range
        dst, src, rge = [int(s) for s in line.split(" ")]
        working_objs = current_objs.copy()
        current_objs = []
        while working_objs:
            (s2, r2) = working_objs.pop(0)
            if s2 + r2 >= src and s2 < (src + rge):
                # Might need to split range if there are overlaps
                if s2 < src:
                    if s2 + r2 < src + rge:
                        # 2 groups:
                        # [s2, src) add back to working_objs
                        # [src, s2+r2) update and add to next_objs
                        current_objs.append((s2, src - s2))
                        next_objs.append((dst, r2 - (src - s2)))
                    else:
                        # this range surrounds [src, src+rge} so split into 3 groups:
                        # [s2, src) add back to working_objs
                        # [src, src + rge) update and add to next_objs
                        # [src + rge, s2+r2) add back to working_objs
                        current_objs.append((s2, src + rge - s2))
                        next_objs.append((dst, rge))
                        current_objs.append((src + rge, s2 + r2 - (src + rge)))
                elif s2 >= src:
                    if s2 + r2 < src + rge:
                        # single group within src, src + rge - just update whole group
                        next_objs.append((dst + s2 - src, r2))
                    else:
                        # 2 groups:
                        # [s2, src+rge) update and add to next_objs
                        # [src+rge, s2+r2) add back to working_objs
                        next_objs.append((dst + s2 - src, src + rge - s2))
                        current_objs.append((src + rge, s2 + r2 - (src + rge)))
            else:
                current_objs.append((s2, r2))


next_objs.extend(current_objs)
print(next_objs)
print(f"Part 2: {min([n[0] for n in next_objs])}")
