from starter import AOC, CURRENT_YEAR
from pathlib import Path
import json

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)


def parse(d):
    if isinstance(d, dict):
        for k,v in d.items():
            if isinstance(v, dict):
                yield from parse(v)
            elif isinstance(v, list):
                yield from parse(v)
            elif isinstance(v, int):
                yield v
            else:
                #we pass, but maybe he will ask to make "2" -> 2
                pass
    if isinstance(d,list):
        for v in d:
            if isinstance(v, dict):
                yield from parse(v)
            elif isinstance(v, list):
                yield from parse(v)
            elif isinstance(v, int):
                yield v
            else:
                #we pass, but maybe he will ask to make "2" -> 2
                pass


def red_parse(d):
    if isinstance(d, dict):
        if "red" not in d.values():
            for k,v in d.items():
                if isinstance(v, dict):
                    if "red" not in v.values():
                        yield from red_parse(v)
                elif isinstance(v, list):
                    yield from red_parse(v)
                elif isinstance(v, int):
                    yield v
                else:
                    #we pass, but maybe he will ask to make "2" -> 2
                    pass
    
    elif isinstance(d,list):
        for v in d:
            if isinstance(v, dict):
                if "red" not in v.values():
                    yield from red_parse(v)
            elif isinstance(v, list):
                yield from red_parse(v)
            elif isinstance(v, int):
                yield v
            else:
                #we pass, but maybe he will ask to make "2" -> 2
                pass

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    j = json.loads(inputs_1)
    nums = list(parse(j))
    return sum(nums)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    j = json.loads(inputs_1)
    nums = list(red_parse(j))
    return sum(nums)


if __name__ == "__main__":
    s=""""""
    print("solve_1", solve_1(s))
    print("solve_2", solve_2(s))
