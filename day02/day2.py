from aoc_helper import *

# def is_valid2(s, twice_only = False):
#     if twice_only and len(s) % 2 != 0:
#         return True

#     if len(s) > 1 and len(set(s)) == 1:        
#         return False
    
#     for i in range(2,(len(s)//2)+1):
#         if s[0:i] == s[i:]:
#             return False
#         if not twice_only and s[0:i]*(len(s)//i) == s:
#             return False
#     return True

def is_valid(s):
    if len(s) == 1:
        return [True, True]
    
    # part 1, it valid if it's an odd length or not a mirror
    mid = len(s)//2
    part1 = len(s) % 2 != 0 or s[0:mid] != s[mid:]

    # part 2, it's valid if it's not all the same or a repeat
    part2 = len(set(s)) != 1       
    for i in range(2,(len(s)//2)+1):
        part2 = part2 and s[0:i]*(len(s)//i) != s        
        if not part2:
            break

    return [part1, part2]

        
#with open("test.txt") as file:
with open("day2.txt") as file:
    lines = file.read().strip().splitlines()

nums = lines[0].split(",")
part1 = 0
part2 = 0
for n in nums:
    start,end = [int(x) for x in n.split("-")]
    for v in range(start,end+1):
        number = str(v)
        part1_validity, part2_validity = is_valid(number)
        if not part1_validity:
            part1 += v
        if not part2_validity:
            part2 += v
answer(part1)
answer(part2)

