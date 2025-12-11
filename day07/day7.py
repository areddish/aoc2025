from aoc_helper import *

p1 = 0
p2 = 0

memo = {}
def many_worlds(loc, splitters, end):
    x,y = loc
    while (x,y) not in splitters and y < end:
        y = y + 1

    if (x,y) in memo:
        return memo[(x,y)]
    
    result = 1
    if y < end:
        assert (x,y) in splitters
        result = many_worlds((x-1,y), splitters, end) + many_worlds((x+1,y), splitters, end)
    memo[(x,y)] = result
    return result


#with open("test.txt") as file:
with open("day7.txt") as file:
    lines = file.read().strip().splitlines()

    start = (None,None)
    splitters = set()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "S":
                start = (x,y)
            elif ch == "^":
                splitters.add((x,y))

    beams = {start:1}
    max_y = start[1]
    while max_y < len(lines):
        next_beams = {}
        for beam in beams:          
            x,y = beam
            y = y+1
            max_y = y
            if (x,y) in splitters:
                p1 += 1
                next_beams[(x-1, y)] = 1
                next_beams[(x+1, y)] = 1
            else:
                next_beams[(x,y)] = None        
        beams = next_beams
    answer(p1)

    p2 = many_worlds(start, splitters, len(lines))
    answer(p2)