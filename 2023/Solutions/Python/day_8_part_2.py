import re
from icecream import ic
from numpy import prod, lcm

class steps():
    def add_step(self, step: str):
        # step will have the format:
        #  ABC = (LLL, RRR)
        # set self.abc = {"L": LLL, "R": RRR}
        # Will use the regex that will capture the 3 grousp:
        #  (^[A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)
        regex = r'(^[A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)'
        #ic(step)
        abc, lll, rrr = re.findall(regex, step)[0]
        setattr(self, abc, {"L": lll, "R": rrr})
        # if abc ends with letter "A" return it
        if abc[-1] == "A":
            return getattr(self, abc)

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    
    directions = tf[0]
    total = 0
    S = steps()
    current_steps = [el for el in [ S.add_step(line) for line in tf[2:] ] if el]
    #ic(current_steps)
    totals = list()

    found = False
    while True:
        for d in directions:
            total += 1
            next_steps = list()
            for step in current_steps:
                next_steps.append(step[d])
            #ic(total, d, next_steps)

            for step in next_steps:
                if step[-1] == "Z":
                    #ic("Found ONE!", step, total, totals)
                    totals.append(total)
                
                    next_steps.remove(step)
                    if not next_steps:
                        found = True
                        break

            current_steps = [getattr(S, step) for step in next_steps]
        if found:
            break
    result = 1

    print (f"Totals: {totals} - make LCM of these :D")
    # calculated LCM with wolfram alpha, since making it in python is just... meh.
    ## btw all of them are dibvisible by 281... LoL
    # 12083 = 43×281 (2 distinct prime factors)
    # 13207 = 47×281 (2 distinct prime factors)
    # 14893 = 53×281 (2 distinct prime factors)
    # 19951 = 71×281 (2 distinct prime factors)
    # 20513 = 73×281 (2 distinct prime factors)
    # 22199 = 79×281 (2 distinct prime factors)