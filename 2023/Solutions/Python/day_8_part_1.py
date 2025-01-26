import re
from icecream import ic

class steps():
    def add_step(self, step: str):
        # step will have the format:
        #  ABC = (LLL, RRR)
        # set self.abc = {"L": LLL, "R": RRR}
        # Will use the regex that will capture the 3 grousp:
        #  (^[A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)
        regex = r'(^[A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)'
        abc, lll, rrr = re.findall(regex, step)[0]
        setattr(self, abc, {"L": lll, "R": rrr})

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    
    directions = tf[0]
    total = 0
    S = steps()
    _ = [ S.add_step(line) for line in tf[2:] ]
    current_step = getattr(S, "AAA")
    #ic(current_step["L"])
    found = False
    while True:
        for d in directions:
            total += 1
            next_step = current_step[d]
            if next_step == "ZZZ":
                found = True
                break
            current_step = getattr(S, next_step)
            #ic(d, current_step, total)
        if found:
            break

    print (f"Total steps: {total}")
