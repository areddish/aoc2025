from collections import defaultdict
from aoc_helper import *
import heapq

def bfs(nodes):
    Q = []
    for n in nodes["you"]:
        Q.append((n, ["you"]))

    visited = set()
    count = 0
    count2 = 0
    
    while Q:
        print(Q)
        dest, path = Q.pop(0)

        if dest == "out":
            print(path)
            count += 1
            if "dac" in path and "fft" in path:
                count2 += 1

        visited.add(dest)
        for n in nodes[dest]:
            if n not in visited:
                Q.append((n, [n] + list(path)))
        
    return count, count2

with open("test.txt") as file:
#with open("day11.txt") as file:
    lines = file.read().strip().splitlines()

    nodes = defaultdict(list)
    for l in lines:
        p = l.split(" ")
        for dest in p[1:]:
            nodes[p[0][:-1]].append(dest)

    p1, p2 = bfs(nodes)
    answer(p1)
    answer(p2)