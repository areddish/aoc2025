from collections import defaultdict, deque
from aoc_helper import *

memo = {}
def bfs_dp(nodes, current, hasFft, hasDac):
    if (current, hasFft, hasDac) in memo:
        return memo[(current, hasFft, hasDac)]
    
    if current == "out":
        result = 1 if hasDac and hasFft else 0
        memo[(current, hasFft, hasDac)] = result
        return result
    
    hasFft |= current == "fft"
    hasDac |= current == "dac"

    result = 0
    for dest in nodes[current]:
        result += bfs_dp(nodes, dest, hasFft, hasDac)

    memo[(current, hasFft, hasDac)] = result
    return result

def bfs(nodes, start="you", end="out"):
    Q = deque(nodes[start])

    visited = set()
    count = 0  
    while Q:
        dest = Q.popleft()

        if dest == end:
            count += 1
            continue

        visited.add(dest)
        for n in nodes[dest]:
            if n not in visited:
                Q.append(n)

    return count

#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day11.txt") as file:
    lines = file.read().strip().splitlines()

    nodes = defaultdict(list)
    for l in lines:
        p = l.split(" ")
        for dest in p[1:]:
            nodes[p[0][:-1]].append(dest)

    answer(bfs(nodes))
    answer(bfs_dp(nodes, "svr", False, False))