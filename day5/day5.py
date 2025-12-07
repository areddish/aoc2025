from collections import defaultdict
from aoc_helper import *

p1 = 0
p2 = 0

def is_fresh(id, ranges):
    i = 0
    j = len(ranges) - 1
    while i <= j:
        mid = (i + j) // 2
        s,e = ranges[mid]
        if s <= id <= e:
            return True
        elif id < s:
            j = mid - 1
        else:
            i = mid + 1
    return False

#with open("test.txt") as file:
with open("day5.txt") as file:
    lines = file.read().strip()

    ranges, ids = [l.split("\n") for l in lines.split("\n\n")]
    print(ranges, ids)
        
    rs = []
    all_ids = set()
    for r in ranges:
        start,end = [int(x) for x in r.split("-")]
        rs.append((start, end))
#        for x in range(start,end+1):
#            all_ids.add(x)

    rs.sort(key=lambda x:x[0])
    # compress
    # 1-3, 1-5 => 1-5
    # 1-3, 2-5 => 1-5
    # 1-3, 4-5 => 1-3, 4-5
    # 1-10, 2-4 => 1-10
    rs_fixed = [rs[0]]
    for i in range(1, len(rs)):
        s,e = rs[i]
        cs, ce = rs_fixed[-1]

        if s <= cs:
            assert s == cs
            rs_fixed[-1] = (s, max(ce, e))
        elif cs <= s <= ce:
            rs_fixed[-1] = (min(s,cs), max(ce, e))
        elif cs <= e <= ce:
            continue
        else:
            rs_fixed.append((s,e))

    # validate
    for i in range(len(rs_fixed)-1):
        for j in range(i+1, len(rs_fixed)):
            s1,e1 = rs_fixed[i]
            s2,e2 = rs_fixed[j]
            assert s1 <= e1 and s1 < s2 and s1 < e2, f"{(s1, e1), (s2, e2)}"
            assert e1 < s2 and e1 < e2, f"{(s1, e1), (s2, e2)}"
            assert s2 <= e2, f"{(s1, e1), (s2, e2)}"
            assert e2 > s1 and e2 >= s2 and e2 > e1, f"{(s1, e1), (s2, e2)}"
            
    for id in ids:
        id = int(id)
        fresh = is_fresh(id, rs_fixed)
        print(f"Checking {id}", "FRESH" if fresh else "")
        if fresh:
            p1 += 1

    for range in rs_fixed:
        s,e = range
        p2 += (e-s) + 1
        
    answer(p1)
    answer(p2)