import functools
import re
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ''
    input_file = f'day12_test_input{suffix}.txt'
else:
    input_file = f'day12_input.txt'

data = utils.input_as_lines(input_file)

def matches_sizes(s, group_sizes):
    p = r'^\.*'
    for (i, g) in enumerate(group_sizes):
        p += rf'#{{{g}}}'
        if i == len(group_sizes) - 1:
            p += r'\.*$'
        else:
            p += r'\.+'

    # if re.match(p, s):
    # print(s, group_sizes, p, re.match(p, s))

    return re.match(p, s)

@functools.cache
def permutations(n):
    if n == 1:
        return ['#', '.']
    else:
        perms = []
        for p in permutations(n - 1):
            perms.extend([['#', *p], ['.', *p]])
        return perms


@functools.cache
def find_permutations(s, group_sizes):
    chars = list(s)
    query_indexes = [i for i, c in enumerate(chars) if c == '?']
    perms = permutations(len(query_indexes))
    total = 0
    checked = []
    for p in perms:
        char_list = chars.copy()
        for i, idx in enumerate(query_indexes):
            char_list[idx] = p[i]
        s2 = ''.join(char_list)
        if s2 not in checked and matches_sizes(''.join(char_list), group_sizes):
            total += 1
            checked.append(s)

    return total

@functools.cache
def find_permutations2(s, group_sizes):
    # Massive thanks to u/StaticMoose for the tutorial on this!
    # My original method (above) was far too slow.
    if len(group_sizes) == 0:
        if '#' in s:
            # No groups left
            return 0
        else:
            return 1
    elif len(s) == 0:
        return 0

    if s[0] == '#':
        # Need to match first group size chars as #s
        # If string is too short or there are any dots in there, there's no match
        if '.' in s[:group_sizes[0]] or len(s) < group_sizes[0]:
            return 0
        elif len(s) == group_sizes[0]:
            if len(group_sizes) == 1:
                return 1
            else:
                return 0
        else:
            if s[group_sizes[0]] in "?.":
                return find_permutations2(s[group_sizes[0]+1:], tuple(group_sizes[1:]))
            else:
                return 0
    elif s[0] == '.':
        return find_permutations2(s[1:], group_sizes)
    else:
        hash_perms = find_permutations2('#' + s[1:], group_sizes)
        dot_perms = find_permutations2('.' + s[1:], group_sizes)
        return hash_perms + dot_perms


p1_total = 0
for line in data:
    s, cond = line.split(' ')
    group_sizes = tuple([int(c) for c in cond.split(',')])
    p1_total += find_permutations2(s, group_sizes)

print(f"Part 1: {p1_total}")

p2_total = 0
for i, line in enumerate(data):
    s, cond = line.split(' ')
    group_sizes = tuple([int(c) for c in cond.split(',')])
    p2_total += find_permutations2('?'.join([s]*5), group_sizes*5)

print(f"Part 2: {p2_total}")
