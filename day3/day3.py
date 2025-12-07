from collections import defaultdict
from aoc_helper import *

#with open("test.txt") as file:
with open("day3.txt") as file:
    lines = file.read().strip().splitlines()

p1 = 0
p2 = 0

def to_digit(l):
    res = 0
    tens = 0
    for x in l[::-1]:
        res += x * (10**tens)
        tens += 1
    return res

memo = {}
def find_max(battery):
    #print("find_max: ", battery)
    if len(battery) < 12:
        assert False, "invalid"
        return 0

    key = tuple(sorted(battery))
    if key in memo:
        return memo[key]
    
    vals = []
    for x in range(0, len(battery)-1):
        test_batteries = battery[0:x]+battery[x+1:]
        val = to_digit(test_batteries)
        vals.append((val, test_batteries))

    ranked = sorted(vals, key=lambda v:v[0])
    maxv = ranked[-1]
    if len(maxv[1]) == 12:
        memo[key] = maxv[0]
        return maxv[0] 

    return find_max(maxv[1])
    
def prep(battery):
    print("PREP: ",battery)
    i = 0
    while len(battery) > 12:
        if i + 1 >= len(battery):
            i = 0
        
        if battery[i] <= battery[i+1]:
            battery.pop(i)
        else:
            i += 1
    
    assert len(battery) == 12, len(battery)

    print("DONE: ", battery)
    return battery

def find_max2(battery, removing=1):
    if len(battery) == 12:
        return to_digit(battery)
    
    # i = 0
    # while removing == 1 and len(battery) > 12 and battery[0] < battery[1]:
    #     battery.pop(0)

    i = 0
    next_battery = None
    maxv = 0
    while removing not in battery:
        removing += 1
    
    for x in range(0, len(battery)):
        if battery[x] == removing:
            test_batteries = battery[0:x]+battery[x+1:]
            #print(battery, test_batteries)
            val = to_digit(test_batteries)
            if val > maxv:
                next_battery = test_batteries
                maxv = val
    #print("selected: ", next_battery)
    return find_max2(next_battery, removing)

def find_max3(battery, removing=1):
    i = 0
    j = 1
    res = []
    while len(res) < 12 and j < len(battery):
        if battery[i] > battery[j]:
            res.append(battery[i])
            i = j
            j+=1
        else:
            j+=1
    while len(res) < 12:
        res.append(battery[i])
        i += 1
    return to_digit(res)
    
    # i = 0
    # next_battery = None
    # maxv = 0
    # while removing not in battery:
    #     removing += 1
    
    # for x in range(0, len(battery)):
    #     if battery[x] == removing:
    #         test_batteries = battery[0:x]+battery[x+1:]
    #         #print(battery, test_batteries)
    #         val = to_digit(test_batteries)
    #         if val > maxv:
    #             next_battery = test_batteries
    #             maxv = val
    # #print("selected: ", next_battery)
    # return find_max2(next_battery, removing)

def get_val(on_off, battery):
    result = []
    for i in range(len(battery)):
        if on_off[i]:
            result.append(battery[i])
    return to_digit(result)

from collections import Counter
def find_max5(battery):
    start = 0
    digit = 9
    on_off = [0] * len(battery)
    
    turned_on = set()
    while sum(on_off) < 12:
        
        for i in range(start, len(battery)):
            if battery[i] == digit:
                on_off[i] = True                
                turned_on.add(i)
                if sum(on_off) >= 12:
                    break        
        # update start
        possibles = 0
        for i in range(len(battery)-1, 0, -1):
            if not on_off[i]:
                possibles += 1
            else:
                if possibles >= 12 - sum(on_off) and i in turned_on:
                    start = i
                    break
        digit -= 1

    return get_val(on_off, battery)

def find_max4(battery):
    counts = Counter(battery)    
    on_off = [0] * len(battery)
    digit = 9
    start = 0
    while sum(on_off) < 12:
        tracker = []
        if counts[digit] + sum(on_off) <= 12:
            # turn them all on
            for i in range(start, len(battery)):
                if battery[i] == digit:
                    on_off[i] = True
                    tracker.append((i,))
            digit -= 1
        else:
            # try them all
            max_val = get_val(on_off, battery)
            idx = 0
            for i in range(start, len(battery)):
                if not on_off[i] and battery[i] == digit:
                    on_off[i] = True
                    print("CANDIDATE:", get_val(on_off, battery))
                    if get_val(on_off, battery) >= max_val:
                        idx = i
                    on_off[i] = False
            on_off[idx] = True

        # if True in on_off:
        #     first = on_off.index(True)
        #     possibles = 0
        #     for i in range(first, len(on_off)):
        #         if not on_off[i]:
        #             possibles += 1
        #             if possibles >= 12:
        #                 start = i
        
    #     found = False
    #     i = 0
    #     while i < len(battery):
    #         is_on = on_off[i]
    #         if not is_on and battery[i] == digit:
    #             on_off[i] = True
    #             found = True
    #             break
    #         i+=1
    #     if not found:
    #         digit -= 1

    # result = []
    # for i in range(len(battery)):
    #     if on_off[i]:
    #         result.append(battery[i])

    assert sum(on_off) == 12
    return get_val(on_off, battery)

for l in lines:
    battery = [int(x) for x in list(l)]
    maxv = 0
    for x in range(0, len(battery)):
        for y in range(x+1, len(battery)):
            if battery[x] * 10 + battery[y] > maxv:                        
                maxv = battery[x] * 10 + battery[y]
    p1 += maxv

    maxv = find_max(battery)
    maxv4 = find_max5(battery)
    if maxv != maxv4:
        print(f"DIFF: {maxv} {maxv4}", "WAHT!?!?!!?!?!?!?!" if maxv4 < maxv else "")
    #maxv2 = find_max2(prep(battery))
    #assert maxv >= maxv2, f"{maxv} {maxv2}"
#    p2a.append(maxv)
    #print("p2:", maxv4)
    p2 += max(maxv, maxv4)

answer(p1)
answer(p2)


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

# 170418192256808 
# 144224743240223 too low
# 144255794526102
# 142397911862395                                                                                                                               
# 142723471892448
# 170398698434252