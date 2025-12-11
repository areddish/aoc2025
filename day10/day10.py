from collections import defaultdict
from aoc_helper import *
import heapq
import z3

p1 = 0
p2 = 0

def configure_lights(start, goal, wiring, mapping={}):
    seen = set()
    Q = [(0, start)]
    heapq.heapify(Q)
    while Q:
        steps, cur = heapq.heappop(Q)
        seen.add(cur)
        if cur == goal:
            return steps
                   
        for button in wiring:
            next_cur = list(cur)
            for toggle in button:
                next_cur[toggle] = "." if next_cur[toggle] == "#" else "#"
            if "".join(next_cur) not in seen:
                heapq.heappush(Q, (steps+1, "".join(next_cur)))
            #Q.append((steps+1, "".join(next_cur)))
        
    assert False

#with open("test.txt") as file:
with open("day10.txt") as file:
    lines = file.read().strip().splitlines()

    start = (None,None)
    splitters = set()

    for line in lines:
        p = line.split(" ")
        diag = p[0][1:-1]
        wiring = tuple(tuple(nums(x)) for x in p[1:-1])
        joltage = nums(p[-1])
        # val = solve("."*len(diag), diag, wiring)
        # print(("."*len(diag), diag, wiring, joltage), val)
        #val = configure_lights("."*len(diag), diag, wiring)
        val = 0
        p1 += val

        presses = [ z3.Int(f"button{i}") for i in range(len(wiring))]
        s = z3.Optimize()
        s.add([press >= 0 for press in presses])
        s.add([z3.Sum(presses[j] for j,wire in enumerate(wiring) if k in wire) == jolt for k, jolt in enumerate(joltage)])
        s.minimize(z3.Sum(presses))
        s.check()
        m = s.model()
        for press in presses:
            p2 += m[press].as_long()

    answer(p1)
    answer(p2)
