from aoc_helper import *
from collections import Counter
import heapq

def straight_line_dist(p1, p2):
    # ignore sqrt as it's not needed for this
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2
    
#with open("test.txt") as file:
with open("day8.txt") as file:
    lines = file.read().strip().splitlines()
    
    boxes = []
    for line in lines:
        boxes.append(tuple(nums(line)))
    
    # Pre-compute all distances between junction boxes and store them
    # in a priority Q
    distance_q = []
    for i in range(len(boxes)-1):
        for j in range(i+1, len(boxes)):
            heapq.heappush(distance_q, (straight_line_dist(boxes[i], boxes[j]), boxes[i], boxes[j]))

    # To track a circuit we'll just assign a circuit number to the node. Two nodes with the same
    # circuit number are connected.
    # Also track who's connected for easy lookup
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
            # add n2 to n1's circuit
            circuits[n2] = circuits[n1]
        elif n2 in circuits:
            # add n1 to n2's circuit
            circuits[n1] = circuits[n2]
        else:
            # new connection, new circuit
            circuits[n1] = next_circuit_num
            circuits[n2] = next_circuit_num
            next_circuit_num += 1

    match = 0
    dist, box1, box2 = 0, 0, 0
    while len(circuits) < len(boxes) or len(set(circuits.values())) != 1:
        dist, box1, box2 = heapq.heappop(distance_q)

        if (box1,box2) in connected:
            continue

        update_circuit(box1, box2, circuits)
        match += 1

        if match == 1000:            
            m1, m2, m3 = Counter(circuits.values()).most_common(3)
            answer(m1[1]*m2[1]*m3[1])
    answer(box1[0] * box2[0])