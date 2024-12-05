from typing import Any
from icecream import ic
import copy

class Part:
    x: int
    m: int
    a: int
    s: int
    value: int
    acceppted: bool
    def __init__(self, x: int,m: int,a: int,s: int):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.value = self.calc_value()
        self.acceppted = False

    def __str__(self) -> str:
        return f'x={self.x},m={self.m},a={self.a},s={self.s}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def calc_value(self):
        return self.x + self.m + self.a + self.s

class Condition:
    what: str
    sign: str
    value: int
    result: str
    def __init__(self, what: str, sign: str, value: str, result: str):
        self.what = what       # can be None
        self.sign = sign       # can be None
        self.value = value     # can be None
        self.result = result   
    
    def __str__(self):
        return f'{self.what if self.what else ''}{self.sign if self.sign else ''}{self.value if self.value else ''}{":" if self.value else '' }{self.result}'

    def __repr__(self) -> str:
        return self.__str__()

    def evalueate_part(self, part: Part):
        if self.what == None:
            return self.result
        
        if self.sign == '<':
            if getattr(part, self.what) < self.value:
                return self.result
        
        if self.sign == '>':
            if getattr(part, self.what) > self.value:
                return self.result
        
        return False

class Wflows:
    label: str
    conditions: list
    def __init__(self, label):
        self.label = label
        self.conditions = list()
    
    def __str__(self):
        return f'{self.label}: {self.conditions}'
    
    def __repr__(self) -> str:
        return f'{self.label}: {self.conditions}'

    def add_condition(self, condition: str):
        # condition is something like 
        # a<2006:A
        # m>2090:saq
        # A
        # rfg
        if any(['<' in condition, '>' in condition]):
            # this is a comparison, 
            # before the ':' - > first char is always what, then sign, then value
            # after ':' -> result
            what = condition.split(':')[0][0]
            sign = condition.split(':')[0][1]
            value = int(condition.split(':')[0][2:])
            result = condition.split(':')[1]
        else:
            # this is not a condition, what, sign, value are None
            # only result is present, it is like a default behavior
            what = sign = value = None
            result = condition
        
        self.conditions.append(Condition(what, sign, value, result))

def accept_part(part: Part):
    part.acceppted = True
    return part.value

def calc_range_value(ranges: dict)-> int:
    xs = ranges['x']['max'] - ranges['x']['min'] + 1
    ms = ranges['m']['max'] - ranges['m']['min'] + 1
    as_ = ranges['a']['max'] - ranges['a']['min'] + 1
    ss = ranges['s']['max'] - ranges['s']['min'] + 1
    return xs * ms * as_ * ss


def part_2(wfs: dict) -> int:
    accepts = 0
    # each wf can be accessed by only one other wf, then, 
    #  once evaulated, remove it from wfs
    # intial ranges are:
    start_ranges = {
        "x" : {"min": 1, "max": 4000},
        "m" : {"min": 1, "max": 4000},
        "a" : {"min": 1, "max": 4000},
        "s" : {"min": 1, "max": 4000}
    }
    # evaluating each wf in order from [in] split the ranges for the WF that accept
    # those values or reject them or redirect them to other wfs
    wfs_to_evaluate = list()
    wfs_to_evaluate.append([wfs['in'], start_ranges])
    while wfs_to_evaluate:
        wf, ranges = wfs_to_evaluate.pop(0)
        for condition in wf.conditions:
            #ic(ranges)
            if condition.what == None:
                if condition.result == 'A':
                    accepts += calc_range_value(ranges)
                elif condition.result == 'R':
                    pass
                else:
                    wfs_to_evaluate.append([wfs[condition.result], ranges])
            else:

                what, sign, value, result = condition.what, condition.sign, condition.value, condition.result
                # TODO check if there is really a range split, for now assume yes
                if sign == '<':
                    # example x<2006:A   with x 999 to 3900
                    #ic(what, sign, value, result, ranges[what])
                    result_ranges = copy.deepcopy(ranges)
                    result_ranges[what]['max'] = value - 1 # this goes to the result x 999 to 2005
                    #ic(result_ranges)
                    #ic(ranges)
                    ranges[what]['min'] = value # this goes to the next condition x 2007 to 3900
                    #ic(ranges)
                else:
                    # example x>2006:A   with x 999 to 3900
                    result_ranges = copy.deepcopy(ranges)
                    result_ranges[what]['min'] = value + 1 # x 2007 to 3900
                    ranges[what]['max'] = value # x 999 to 2006
                
                if result == 'A':
                    accepts += calc_range_value(result_ranges)
                    
                elif result == 'R':
                    del result_ranges
                else:
                    wfs_to_evaluate.append([wfs[result], result_ranges])

    return accepts

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    wf_loop = True
    workflows = dict()
    parts = list()
    part_1_res = 0
    part_2_res = 0
    for line in tf:
        if line == '':
            #ic(workflows)
            wf_loop = False
            #for wf in workflows.values():
            #    for condition in wf.conditions:
            #        ic(wf.label, condition)
            part_2_res = part_2(workflows)
            continue
        if wf_loop:
            # we are parsing worklows, the structure is:
            # px{a<2006:qkq,m>2090:A,rfg}
            # px is the label, can be any characters leght, untile '{'
            # the rest are the conditions
            label = line.split('{')[0]
            workflows[label] = Wflows(label)

            # conditions are inside the curly brackets
            # are like 'x=148,m=595,a=439,s=483'
            for condition in line[line.find('{')+1:line.find('}')].split(','):
                #ic(label, condition)
                workflows[label].add_condition(condition)
        else:
            # we are parsing parts, the structure is:
            # {x=349,m=1359,a=353,s=1425}
            tmps = {'s': None, 'x': None, 'm': None, 'a': None}
            for part in line[line.find('{')+1:line.find('}')].split(','):
                # using regex
                # ^x=(\d+),m=(\d+),a=(\d+),s=(\d+)
                # to capure the 4 values
                what = part.split('=')[0]
                value = int(part.split('=')[1])
                tmps[what] = value
            parts.append(Part(tmps['x'], tmps['m'], tmps['a'], tmps['s']))
            # we already have all the workflow, we don't need to loop through parts,
            #   we can evaulate them now!
            part = parts[-1]
            #ic(part)
            # entry wf is always the same, 'in' workflow
            first_label = 'in'
            wf = workflows[first_label]
            while True:
                #ic(part, wf.label)
                kill_it = False
                for condition in wf.conditions:
                    #ic(part, wf.label, condition)
                    result = condition.evalueate_part(part)
                    if result:
                        #ic(part, wf.label, condition, result)
                        # cases:
                        # result is a number --> accept part --> break
                        if isinstance(result, int):
                            part_1_res += accept_part(part)
                            kill_it = True
                            break
                        # result is either A or R --> accept/reject part --> break
                        if result == 'A':
                            part_1_res += accept_part(part)
                            kill_it = True
                            break
                        if result == 'R':
                            kill_it = True
                            break
                        # result 
                        # is another workflow --> evaulate that workflow
                        wf = workflows[result]
                        break
                if kill_it:
                    break
    ic(part_1_res)
    ic(part_2_res)