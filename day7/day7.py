from collections import defaultdict
from aoc_helper import *


import networkx as nx

def count_paths_efficiently(G, source, target):
    """
    Counts paths in a DAG from source to target using Dynamic Programming.
    Time Complexity: O(V + E)
    """
    # 1. Check if it's actually a DAG (optional but recommended)
    if not nx.is_directed_acyclic_graph(G):
        raise ValueError("Graph is not a DAG!")

    # 2. Initialize the path count for all nodes to 0
    path_counts = {node: 0 for node in G.nodes()}
    path_counts[source] = 1

    # 3. Process nodes in topological order
    # This ensures we process a node only after all its predecessors are done
    for node in nx.topological_sort(G):
        if node == source:
            continue
        
        # The number of paths to 'node' is the sum of paths to its predecessors
        # (predecessors are nodes that have an edge pointing TO 'node')
        count = sum(path_counts[pred] for pred in G.predecessors(node))
        path_counts[node] = count

    return path_counts[target]

p1 = 0
p2 = 0

memo = {}
def many_worlds(loc, splitters, end, visited=set(), from_=None):
    x,y = loc
    while (x,y) not in splitters and y < end:
        y = y + 1

    if loc in memo:
        return memo
    
    if (x,y) in visited:
        return 0
    
    if y >= end:
        memo[(x,y)] = 1
        #print("end", (x,y))
        return 1
    
    visited.add((x,y))
    # go left
    assert (x,y) in splitters
    res = 0
    if (x-1,y) not in visited:
        res += many_worlds((x-1,y), splitters, end, set(visited), (x,y))
    if (x+1,y) not in visited:
        res += many_worlds((x+1,y), splitters, end, set(visited), (x,y))
    memo[from_] = res
    memo[(x,y)] = res
    return res
    

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
            
        #p1 += len(next_beams) - len(beams)
        beams = next_beams
    answer(p1)

    # G = nx.DiGraph()    
    # max_y = start[1]
    # while max_y < len(lines):
    #     next_beams = {}
    #     for beam in beams:
    #         x,y = beam
    #         y = y+1
    #         max_y = y
    #         if (x,y) in splitters:
    #             p1 += 1
    #             next_beams[(x-1, y)] = 1
    #             next_beams[(x+1, y)] = 1
    #         else:
    #             next_beams[(x,y)] = 1
            
    #     #p1 += len(next_beams) - len(beams)
    #     beams = next_beams

    answer(many_worlds(start, splitters, len(lines)))

