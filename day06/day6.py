from collections import defaultdict
from aoc_helper import *
import re
p1 = 0
p2 = 0

def mul(l):
    res = 1
    for n in l:
        res = res * n
    return res

def read_rect(start_col, end_col, lines):
    digits = []
    rtl_digits = []

    #Read normal
    for row in range(len(lines)):
        digits.append(int(lines[row][start_col:end_col]))

    #Read rtl
    for c in range(start_col, end_col):
        digit = ""
        for row in range(len(lines)):
            digit = digit + lines[row][c]
        rtl_digits.append(int(digit))
    return digits, rtl_digits

#with open("test.txt") as file:
with open("day6.txt") as file:
    lines = file.read().strip().splitlines()
    
    ops = []
    for ch in lines[-1]:
        if ch == "+" or ch == "*":
            ops.append(ch)
    lines.pop()

    # make sure the lines are all same sized
    for i in range(1, len(lines)):
        assert len(lines[i]) == len(lines[0])
        lines[i] = lines[i] + " "

    col = 0
    current_column = [""]*(len(lines))

    # Find the column limits. 0,cur_index - len(lines)-1,max_index
    # then we can read the numbers
    cur_index = 0
    p1_digits = []
    p2_digits = []
    while cur_index < len(lines[0]):
        max_index = 0
        for row in range(len(lines)):    
            max_index = max(lines[row].index(" ", cur_index), max_index)      
        digits,rtl_digits = read_rect(cur_index, max_index, lines)
        #print(max_index, digits, rtl_digits)
        p1_digits.append(digits)
        p2_digits.append(rtl_digits)
        cur_index = max_index + 1

    op_map = { "*": mul, "+": sum}
    for i,op in enumerate(ops):
        p1 += op_map[op](p1_digits[i])
        p2 += op_map[op](p2_digits[i])
        
    answer(p1)
    answer(p2)