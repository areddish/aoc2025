import re

def nums2(lines):
    nums = []
    for line in lines:
        nums.append([int(x) for x in re.findall(r"(\d+)", line)])
    return nums

def nums(line):
    return [int(x) for x in re.findall(r"(\d+)", line)]