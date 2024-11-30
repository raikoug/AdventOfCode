from starter import AOC, CURRENT_YEAR
from pathlib import Path
import collections

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    elves = int(inputs_1)
    best_power = 2
    while True:
        new_power = best_power * 2
        if new_power > elves:
            break
        best_power = new_power
    
    magic_number = elves - best_power
    lucky_elf = (2 * magic_number) + 1
    return lucky_elf
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # i dont like this. I didn do this neither I understood it entirely.... :/
    # source: https://www.reddit.com/user/aceshades/ :
    #   https://www.reddit.com/r/adventofcode/comments/5j4lp1/comment/dbdf9mn/
    #   
    elves = int(inputs_1)
    left = collections.deque()
    right = collections.deque()
    for i in range(1, elves+1):
        if i < (elves // 2) + 1:
            left.append(i)
        else:
            right.appendleft(i)

    while left and right:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        # rotate
        right.appendleft(left.popleft())
        left.append(right.pop())
    return left[0] or right[0]



if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")