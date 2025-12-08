from aoc_helper import *
from collections import defaultdict
from math import sqrt
import heapq

p1 = 0
p2 = 0

def straight_line_dist(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2
    
#with open("test.txt") as file:
with open("day8.txt") as file:
    lines = file.read().strip().splitlines()
    
    boxes = []
    for l in lines:
        x,y,z = nums(l)
        boxes.append((x,y,z))
    
    distance_q = []

    MAX = len(boxes)**8
    for i in range(len(boxes)-1):
        for j in range(i+1, len(boxes)):
            heapq.heappush(distance_q, (straight_line_dist(boxes[i], boxes[j]), boxes[i], boxes[j]))

    graph = defaultdict(list)
    circuits = {}
    connected = set()
    next_circuit_num = 1
    def update_circuit(n1, n2, circuits):
        global next_circuit_num
        global connected
        connected.add((n1,n2))
        connected.add((n2,n1))
        if n1 in circuits and n2 in circuits:
            # merge the two circuits to n1's
            val = circuits[n1]
            merge_val = circuits[n2]
            for box in circuits:
                if circuits[box] == merge_val:
                    circuits[box] = val
        elif n1 in circuits:
            assert n2 not in circuits
            circuits[n2] = circuits[n1]
        elif n2 in circuits:
            assert n1 not in circuits
            circuits[n1] = circuits[n2]
        else:
            circuits[n1] = next_circuit_num
            circuits[n2] = next_circuit_num
            next_circuit_num += 1

    # needs to take into consideration the connectedness of them

    match = 0
    while match < 1000:
        dist, b1, b2 = heapq.heappop(distance_q)
        print(b1, b2)

        if (b1,b2) in connected: #circuits.get(b1, -1) == circuits.get(b1, -1):
            continue
        # graph[min_row].append(min_col)
        # graph[min_col].append(min_row)
        update_circuit(b1, b2, circuits)
        match += 1

    val_counts = defaultdict(int)
    for node in circuits:
        val_counts[circuits[node]] += 1

    #m1, m2, m3 = sorted([len(graph[x]) for x in graph], reverse=True)[:3]
    m1, m2, m3 = sorted(val_counts.values(), reverse=True)[:3]
    p1 = m1 * m2 * m3
    print(m1,m2,m3)
    answer(p1)
    # print(graph)

    # print(circuits)
    # print(val_counts)