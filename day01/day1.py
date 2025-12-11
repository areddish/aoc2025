from collections import defaultdict
from aoc_helper import *

l1 = []
l2 = []
l2_counter = defaultdict(int)
#with open("test.txt") as file:
with open("day1.txt") as file:
    lines = file.read().strip().splitlines()

dial = 50
land_password = 0
click_password = 0

class Dial:
    def __init__(self):
        self.dial = 50

    def right(self):
        self.dial += 1
        if self.dial > 99:
            self.dial = 0
            return 1
        return 0 if self.dial != 0 else 1

    def left(self):
        self.dial -= 1
        if self.dial < 0:
            self.dial = 99
            return 1
        return 0 if self.dial != 0 else 1

dial = Dial()
lands = 0
clicks = 0
for l in lines:
    dir = l[0]
    distance = int(l[1:])
    if dir == "L":
        for _ in range(distance):
            dial.left()
            if dial.dial == 0:
                clicks += 1
        if dial.dial == 0:
            lands += 1
    else:
        assert dir == "R"
        for _ in range(distance):
            dial.right()
            if dial.dial == 0:
                clicks += 1
        if dial.dial == 0:
            lands += 1
answer(lands)
answer(clicks)


# for l in lines:
#     dir = l[0]
#     distance = int(l[1:])
#     distance = distance * (1 if dir == "R" else -1)
#     dial += distance
#     while dial < 0:
#         click_password += 1
#         dial += 100
#     while dial > 99:
#         click_password += 1
#         dial -= 100
#     # dial %= 100
#     # if dial < 0:
#     #     dial = 100 + dial
#     if dial == 0:
#         land_password += 1
# answer(land_password)
# answer(click_password)
#answer(ans)