#!/usr/bin/env python3
# 2023 Day 22: Sand Slabs

import copy

def process_input(filename):
    """Acquire input data"""
    with open(filename) as file:
        input = file.read().splitlines()

    bricks = []

    for line in input:
        token = line.split('~')
        ends = []
        for t in range(2):
            end = [int(e) for e in token[t].split(',')]
            ends.append(end)
        brick = ['F',ends, [], []]
        bricks.append(brick)
            
    return bricks


def find_supported_by_ground():
    for brick in bricks:
        state, ends, supports, supported_by = brick
        if ends[0][2] == 1 or ends[1][2] == 1:
            brick[0] = 'S'
            brick[3].append('ground')
    return


def all_fall_down():
    while True:
        bn = lowest_unsupported()
        if bn == -1:
            break       # no more unsupported bricks
        drop_brick(bn)
    return


def lowest_unsupported():
    low_brick = -1
    lowest_z = 99999999
    for b, brick in enumerate(bricks):
        status, ends, supports, supported_by = brick
        if status == 'S':
            continue
        z = min_end(brick,'z')
        if z > lowest_z:
            continue    # already found a lower unsupported
        sbn = brick_supported_by(b)
        if sbn == -1:
            lowest_z = z
            low_brick = b
        else:
            brick[0] = bricks[sbn][0]  # update status
    return low_brick


def brick_supported_by(b):
    """Determine if brick b is resting on any other brick"""
    brick = bricks[b]
    bz = min_end(brick,'z')
    for tb, test_brick in enumerate(bricks):
        if tb == b:
            continue        # skip same brick
        if max_end(test_brick, 'z') != (bz - 1):
            continue        # bottom isn't one level above candidate
        if intersects(brick, test_brick):
            return tb
    return -1


def intersects(brick, test_brick):
    """Return if brick intersects with test_brick"""
    if (max_end(brick,'x') < min_end(test_brick,'x') or
        min_end(brick,'x') > max_end(test_brick,'x')):
        return False        # doesn't intersect in x dimension
    if (max_end(brick,'y') < min_end(test_brick,'y') or
        min_end(brick,'y') > max_end(test_brick,'y')):
        return False        # doesn't intersect in x dimension
    return True

def drop_brick(bn):
    brick = bricks[bn]
    hb = highest_intersecting_brick_below(bn)
    if hb == 'ground':
        drop_to_z(bn,1)
        brick[0] = 'S'      # brick is supported by the ground
        brick[3].append('ground')
    else:
        high_brick = bricks[hb]
        hbz = max_end(high_brick,'z')
        drop_to_z(bn,hbz+1)
        brick[0] = high_brick[0] # brick is supported if on a supported brick
    return


def highest_intersecting_brick_below(bn):
    """Find highest intersecting brick that is below brick bn"""
    brick = bricks[bn]
    brick_bottom = min_end(brick,'z')
    highest_z = 0
    highest = 'ground'
    for tb, test_brick in enumerate(bricks):
        if tb == bn:
            continue        # skip same brick
        tbz = max_end(test_brick,'z')
        if tbz >= brick_bottom:
            continue        # brick is too high
        if tbz <= highest_z:
            continue        # better brick already found
        if not intersects(brick, test_brick):
            continue        # doesn't intersect
        highest_z = tbz
        highest = tb
    return highest


def drop_to_z(bn, nz):
    brick = bricks[bn]
    drop = min_end(brick, 'z') - nz
    brick[1][0][2] -= drop
    brick[1][1][2] -= drop
    return
    
def what_supports_what():
    """Determine which bricks are supported and supported by other bricks"""
    for bn, brick in enumerate(bricks):
        top_z = max_end(brick,'z')
        for tn, test_brick in enumerate(bricks):
            if tn == bn:
                continue    # skip same brick
            if min_end(test_brick, 'z') != (top_z + 1):
                continue    # not on top of brick
            if not intersects(brick, test_brick):
                continue    # doens't intersect

            brick[2].append(tn)         # brick supports test brick
            test_brick[3].append(bn)    # test brick supported by brick
    return

def safe_to_disintegrate():
    safe = 0
    for bn, brick in enumerate(bricks):
        for s in brick[2]:
            supported_brick = bricks[s]
            if len(supported_brick[3]) <= 1:
                break       # supporting a brick with no other supports
        else:
            safe += 1
    return safe


def chain_reaction():
    chain_total = 0
    for bn in range(len(bricks)):
        cr_bricks = disintegrate(bn)
        chain = unsupported_bricks(cr_bricks)
        chain_total += chain
    return chain_total


def disintegrate(d):
    cr_bricks = copy.deepcopy(bricks)
    queue = [d]
    while len(queue) > 0:
        bn = queue.pop()
        for tbn, test_brick in enumerate(cr_bricks):
            if tbn == bn:
                continue    # skip same brick
            state, ends, supports, supported_by = test_brick
            if bn in supported_by:
                idx = supported_by.index(bn)
                del supported_by[idx]
                if len(supported_by) == 0:
                    queue.append(tbn)
    return cr_bricks

def unsupported_bricks(cr_bricks):
    unsupported = 0
    for state, ends, supports, supported_by in cr_bricks:
        if len(supported_by) == 0:
            unsupported += 1
    return unsupported

def min_end(brick, d):
    dimension = dict(x=0,y=1,z=2)
    dn = dimension[d]
    return min(brick[1][0][dn], brick[1][1][dn])

def max_end(brick, d):
    dimension = dict(x=0,y=1,z=2)
    dn = dimension[d]
    return max(brick[1][0][dn], brick[1][1][dn])

#-----------------------------------------------------------------------------------------

filename = r'C:\Users\raikoug\SyncThing\shared_code_tests\adventOfCode\2023\day_22\input.txt'
#filename = 'sample.txt'

print()
print('Acquiring bricks...')
bricks = process_input(filename)

print("What's supported by the ground?")
find_supported_by_ground()

print('Bricks are falling...')
all_fall_down()

print("What supports what?")
what_supports_what()

print('Which are safe to disintegrate?')
safe = safe_to_disintegrate()

print("Considering chain reactions...")
chain_total = chain_reaction()

print()
print('Safe to disintegrate:  ',safe)
print('Sum of chain reactions:',chain_total)