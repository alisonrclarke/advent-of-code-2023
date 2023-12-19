import operator
import re
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day19_test_input{suffix}.txt"
else:
    input_file = f"day19_input.txt"

data = utils.input_as_lines(input_file)

workflows = {}
workflow_re = re.compile(
    r"(?P<name>[a-z]+)\{(?P<instructions>([^,]+,)+)(?P<default>\w+)\}"
)
operator_map = {"<": operator.lt, ">": operator.gt}


def apply_workflow(workflow_name, part):
    global workflows
    instructions, default = workflows[workflow_name]
    for field, op, val, output in instructions:
        if op(part[field], val):
            return output
    return default


for i, line in enumerate(data):
    if line == "":
        break
    m = workflow_re.match(line)
    instruction_strings = m.group("instructions").split(",")[:-1]
    instructions = []
    for inst in instruction_strings:
        field = inst[0]
        op = operator_map[inst[1]]
        val_str, output = inst[2:].split(":")
        instructions.append((field, op, int(val_str), output))

    workflows[m.group("name")] = (instructions, m.group("default"))

p1_total = 0
for line in data[i + 1 :]:
    field_strs = line[1:-1].split(",")
    part = {f.split("=")[0]: int(f.split("=")[1]) for f in field_strs}
    workflow_or_result = "in"
    while workflow_or_result not in ["A", "R"]:
        workflow_or_result = apply_workflow(workflow_or_result, part)

    if workflow_or_result == "A":
        p1_total += sum(part.values())

print(f"Part 1: {p1_total}")

# Part 2
all_accept_paths = {}
all_reject_paths = {}


# Go through workflows, find all path(s) from 'in' to 'A'
def find_accept_paths(from_workflow, current_path):
    global all_accept_paths, all_reject_paths
    # TODO: make this work with multiple paths to A
    instructions, default = workflows[from_workflow]
    paths = []
    default_instructions = []
    # breakpoint()
    for field, op, val, output in instructions:
        inst_path = current_path + [(from_workflow, [(field, op, val)])]

        # Work out how to get to default workflow
        # default_op = lambda x, val: not op(x, val)
        if op == operator.lt:
            default_op = operator.gt
            default_val = val - 1
        else:
            default_op = operator.lt
            default_val = val + 1

        default_instructions.append((field, default_op, default_val))

        if output == "A":
            all_accept_paths[from_workflow] = inst_path
            paths.append(inst_path)
        elif output == "R":
            # No path - keep going
            all_reject_paths[from_workflow] = inst_path
        else:
            # Go to next workflow
            next_paths = find_accept_paths(output, inst_path)
            for p in next_paths:
                paths.append(p)

    # Check default too
    inst_path = current_path + [(from_workflow, default_instructions)]
    if default == "A":
        all_accept_paths[from_workflow] = inst_path
        paths.append(inst_path)
    elif default == "R":
        # No path - keep going
        all_reject_paths[from_workflow] = inst_path
    else:
        # Go to next workflow
        next_paths = find_accept_paths(default, inst_path)
        for p in next_paths:
            paths.append(p)

    return paths


def count_possibilities(paths, max_val=4000):
    all_possibilities = 1
    all_ranges = []
    for p in paths:
        ranges = {k: range(1, max_val + 1) for k in ["x", "m", "a", "s"]}
        for _, conditions in p:
            for field, op, val in conditions:
                start = ranges[field].start
                stop = ranges[field].stop
                if not op(ranges[field].start, val):
                    start = val + 1
                if not op(ranges[field].stop, val):
                    stop = val
                ranges[field] = range(start, stop)

        all_ranges.append(ranges)

        path_possibilities = 1
        for r in ranges.values():
            path_possibilities *= len(r)
            all_possibilities += path_possibilities

    print(f"Possibilities before overlap: {all_possibilities}")
    # Now find overlaps between ranges and subtract, as they've been added more than once
    # FIXME: this is getting to a negative value on the main dataset!
    for i, r1 in enumerate(all_ranges):
        for r2 in all_ranges[i + 1 :]:
            overlaps = {}
            for k in r1:
                start = max(r1[k].start, r2[k].start)
                stop = min(r1[k].stop, r2[k].stop)
                if stop > start:
                    overlaps[k] = range(start, stop)

            if len(overlaps) == 4:
                overlap_possibilities = 1
                for r in overlaps.values():
                    overlap_possibilities *= len(r)

                all_possibilities -= overlap_possibilities
                print(f"Possibilities after overlap: {all_possibilities}")

    return all_possibilities


paths = find_accept_paths("in", [])
p2_total = count_possibilities(paths)
print(f"Part 2: {p2_total}")
