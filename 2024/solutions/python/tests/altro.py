import sys
import functools

input = open(r'/home/raikoug/SyncThing/SharedCodeTest/adventOfCode/2024/inputs/day_22/input_1.txt').readlines()

def mix(n1, n2):
    return n1 ^ n2

def prune(n):
    return n % 16777216

def next_secret(num):
    num = prune(mix(num, num*64))
    num = prune(mix(num, num//32))
    num = prune(mix(num, num*2048))
    return num

def n_secrets(num, n):
    result = [num]
    for _ in range(n):
        result.append(next_secret(result[-1]))
    return result


buyer_secrets = [n_secrets(int(n), 2000) for n in input]

print("1:", sum(map(lambda l: l[-1], buyer_secrets)))

## part 2 

def prices_per_buyer(bs):
    bs = list(map(lambda x: x % 10, bs))
    b_res = {}
    for i in range(4, 2001):
        price_deltas = (bs[i-3] - bs[i-4], bs[i-2] - bs[i-3], bs[i-1] - bs[i-2], bs[i] - bs[i-1]) 
        if price_deltas not in b_res:
            b_res[price_deltas] = bs[i]

    return b_res

res_map = {}
for bs in buyer_secrets:
    for pd, val in prices_per_buyer(bs).items():
        res_map[pd] = res_map.get(pd, 0) + val

print("2:", max(res_map.values()))
