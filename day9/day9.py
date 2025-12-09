from collections import defaultdict
from aoc_helper import *
import numpy as np
from scipy.spatial import ConvexHull

part1 = 0
part2 = 0

pts = []

def area(p1, p2):
    return (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)

def cross_product(o, a, b):
    """Returns positive if OAB is counter-clockwise, negative if clockwise, 0 if collinear."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def monotone_chain_convex_hull(points):
    """Computes the Convex Hull of a set of 2D points."""
    # 1. Sort the points (lexicographically by x, then y)
    points = sorted(points)

    # 2. Build lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # 3. Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper hull (remove duplicate last point of lower)
    return lower[:-1] + upper[:-1]

def is_point_in_convex_polygon(point, hull_vertices):
    """
    point: (x, y) tuple
    hull_vertices: List of (x, y) tuples in Counter-Clockwise order
    """
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Check the sign of the cross product for the first edge
    # to establish the "correct" side (inside could be + or - depending on winding)
    base_sign = None
    
    n = len(hull_vertices)
    for i in range(n):
        p1 = hull_vertices[i]
        p2 = hull_vertices[(i + 1) % n] # Wrap around to the first point
        
        cp = cross_product(p1, p2, point)
        
        # Handle cases where point is exactly on the line (cp == 0)
        if cp == 0:
            continue
            
        current_sign = cp > 0
        
        if base_sign is None:
            base_sign = current_sign
        elif base_sign != current_sign:
            return False # Point is on the "wrong" side of this edge

    return True
def contains(p1, p2, shape):
    global pts

    x1 = min(p1[0],p2[0])
    x2 = max(p1[0],p2[0])
    y1 = min(p1[1],p2[1])
    y2 = max(p1[1],p2[1])

    if not is_in_hull((x1,y1), shape) or not is_in_hull((x1,y2), shape) or not is_in_hull((x2,y1), shape) or not is_in_hull((x2,y2), shape):
        return False

# check for colinear with bounds?
#     
    # hull = ConvexHull([(x1,y1),(x2,y2),(x1,y2),(x2,y1)])
    # for p in pts:
    #     if p == (x1,y1) or p == (x2,y2) or p == (x1,y1) or p == 
    #     if is_in_hull(p, hull):
    #         return False
                          
    # startx = min(p1[0],p2[0])
    # endx = max(p1[0],p2[0])+1
    # starty = min(p1[1],p2[1])
    # endy = max(p1[1],p2[1])+1

    # for y in range(starty+1, endy, 2):
    #     for x in range(startx+1, endx, 2):
    #         if not is_in_hull((x,y), shape):
    #             return False
            
    return True

# 2. Define a function to check new points
def is_in_hull(point, hull):
    """
    Checks if 'point' is inside the 'hull'.
    point: a single point (x, y) or (x, y, z)
    hull: a scipy.spatial.ConvexHull object
    """
    # hull.equations is an array of equations for the planes
    # eq[:-1] is the normal vector, eq[-1] is the offset
    # We check: dot(normal, point) + offset <= 0
    return all(np.dot(eq[:-1], point) + eq[-1] <= 1e-12 for eq in hull.equations)

#with open("test.txt") as file:
with open("day9.txt") as file:
    lines = file.read().strip().splitlines()
    for l in lines:
        pts.append(tuple(nums(l)))

    candidate_rectangles = []
    tested = set()
    for i in range(len(pts)):
        for j in range(len(pts)):
            if i == j:
                continue

            p1 = pts[i]
            p2 = pts[j]
            if (p1,p2) in tested:
                continue

            tested.add((p1,p2)) 
            candidate_rectangles.append((area(p1,p2), p1, p2))
            
    candidate_rectangles.sort(reverse=True)
    answer(candidate_rectangles[0][0])

    shape = ConvexHull(pts)# monotone_chain_convex_hull(pts)
    print(shape)
    for candidate in candidate_rectangles:
        answer_area, p1, p2 = candidate
        print("Checking with area:", answer_area)
        if contains(p1, p2, shape):
            answer(answer_area)
            break
    