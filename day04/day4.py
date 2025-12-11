from collections import defaultdict
from aoc_helper import *

p1 = 0

def count(loc, board):
    x,y = loc
    removed = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (x+dx,y+dy) == loc:
                continue
            if board.get((x+dx,y+dy), None) == "@":
                removed.append((x+dx,y+dy))
    return removed

#with open("test.txt") as file:
with open("day4.txt") as file:
    lines = file.read().strip().splitlines()

    board = defaultdict(int)
    y = 0
    for line in lines:
        for x,c in enumerate(line):
            if c == "@":
                board[(x,y)] = "@"
        y += 1

    for x,y in board:
        if len(count((x,y), board)) < 4:
            p1 += 1

    answer(p1)

    p2 = 0
    while True:
        inner_count = 0
        for x,y in board:
            if board.get((x,y), None) == "@" and len(count((x,y), board)) < 4:
                inner_count += 1
                board[(x,y)] = "x"
        p2 += inner_count
        if inner_count == 0:
            break
        
    answer(p2)
