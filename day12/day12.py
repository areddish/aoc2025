from collections import defaultdict, deque
from aoc_helper import *

def pretty_print(p):
    for y in range(len(p)):
        for x in range(len(p[0])):
            print(p[y][x], end="")
        print()
    
def rot(p):
    result = []
    for x in range(len(p[0])-1,-1,-1):
        row = []
        for y in range(len(p)):
            row.append(p[y][x])
        result.append(row)
    return result

def v_flip(p):
    result = []
    for y in range(len(p)):
        row = []
        for x in range(len(p[0])-1,-1,-1):
            row.append(p[y][x])
        result.append(row)
    return result

def h_flip(p):
    result = []
    for y in range(len(p)-1,-1,-1):
        row = []
        for x in range(len(p[0])):
            row.append(p[y][x])
        result.append(row)
    return result


#with open("test.txt") as file:
with open("day12.txt") as file:
    lines = file.read().strip()

    parts = lines.split("\n\n")

    pieces = []
    tree = []
    i = 0
    while i < len(parts):
        tok = parts[i].split("\n")
        if "x" in tok[0]:
            for t in tok:
                ps = t.split(" ")
                w,h = [int(x) for x in ps[0][:-1].split("x")]
                tree.append((w,h,[int(x) for x in ps[1:]]))
        else:
            index = int(tok[0].split(":")[0])        
            assert len(pieces) == index
            pieces.append([list(x) for x in tok[1:]])
        i += 1

    def count(p):
        val = 0
        for y in range(len(p)):
            for x in range(len(p[0])):
                if p[y][x] == "#":
                    val += 1
        return val
    
    counts = [count(piece) for piece in pieces]
    possible = 0
    for item in tree:
        w,h,alloc = item
        area = w*h
        best_fit_area = sum([counts[i] * alloc[i] for i in range(len(alloc))])
        if best_fit_area <= area:
            possible += 1
    answer(possible)