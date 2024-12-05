from starter import AOC, CURRENT_YEAR
from pathlib import Path
from icecream import ic
import json
from IPython import embed
from numpy import uint16

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

# il `NOT`, o `~u16` calcola il complementare di 65535, ~n = 65535-n
BITWISE=65535

class LineMap:
    EQ: bool
    PUT: bool
    val: uint16
    NOT: bool
    OR: bool
    R: bool
    AND: bool
    L: bool
    op1: str 
    op2: str
    dest: str
    
    def __init__(self):
        self.EQ = False
        self.PUT = False
        self.val = 0
        self.NOT = False
        self.R = False
        self.AND = False
        self.OR = False
        self.L = False
        self.op1 = None
        self.op2 = None
        self.dest = ""
    
    def __str__(self) -> str:
        return f"EQ: {self.EQ} PUT: {self.PUT} val: {self.val} NOT: {self.NOT} R: {self.R} AND: {self.AND} OR: {self.OR} L: {self.L} op1: {self.op1} op2: {self.op2} dest: {self.dest}"
    def __repr__(self) -> str:
        return self.__str__()
        

def map_line(line: str) -> list:
    # 44430 -> dest
    # op1 -> dest
    # NOT op1 -> dest
    # op1 OR op2 -> dest
    # op1 and op2 -> dest
    # op1 RSHIFT val -> dest
    # op1 LSHIFT val -> dest
    
    # reult will be of class `LineMap`
    res = LineMap()
    
    # Il bastardo non ha detto che può fare anche:
    # op1 -> op2
    
    operazione,res.dest = line.split(" -> ")
    
    if "RSHIFT" in operazione: res.R = True
    elif "LSHIFT" in operazione: res.L = True
    elif "NOT" in operazione: res.NOT = True
    elif "OR" in operazione: res.OR = True
    elif "AND" in operazione: res.AND = True
    else: 
        try:
            res.val = uint16(int(operazione))
            res.EQ = True
        except:
            res.PUT = True
            res.op1 = operazione
        return res

    if res.R or res.L:
        res.op1, _, res.val = operazione.split(" ")
        res.val = uint16(int(res.val))
    elif res.NOT:
        _, res.op1 = operazione.split(" ")
    elif res.OR or res.AND:
        res.op1, _, res.op2 = operazione.split(" ")
    else:
        print("ERROR!")
    
    return res

def evaluate_m(m: LineMap, values: dict):
    new_key = m.dest
    
    if m.EQ:
        # 44430 -> dest
        new_value = m.val
        return False, new_key, new_value
    
    if m.PUT:
        # op1 -> dest
        if m.op1 in values:
            new_value = values[m.op1]
            return False, new_key, new_value
    
    if m.R or m.L:
        # op1 RSHIFT val -> dest
        # op1 LSHIFT val -> dest
        
        if m.op1 in values:
            new_value = values[m.op1] >> m.val if m.R else values[m.op1] << m.val
            return False, new_key, new_value
    
    if m.AND:
        # case op1 is a number (only 1)
        if m.op1.isnumeric():
            if m.op2 in values:
                new_value = uint16(1) & values[m.op2]
                return False, new_key, new_value
        else:
            # op1 is a key
            if m.op1 in values and m.op2 in values:
                new_value = values[m.op1] & values[m.op2]
                return False, new_key, new_value
    
    if m.OR:
        # op1 OR op2 -> dest
        if m.op1 in values and m.op2 in values:
            new_value = values[m.op1] | values[m.op2]
            return False, new_key, new_value
    
    if m.NOT:
        # NOT op1 -> dest
        if m.op1 in values:
            #new_value = uint16(65535) - values[m.op1]
            new_value = ~values[m.op1]
            return False, new_key, new_value
            
    
    return m, False, False


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    todo = list()
    values = dict()
    for line in inputs_1.splitlines():
        m : LineMap = map_line(line)
        #ic(m)
        o, new_key, new_value = evaluate_m(m, values)

        if o:
            todo.append(o)
        else:
            values[new_key]= new_value
    
    max = 100000
    i = 0
    
    while todo:
        m = todo.pop(0)
        o, new_key, new_value = evaluate_m(m, values)
        if o:
            todo.append(o)
            pass
        else:
            values[new_key]= new_value
        i += 1
        if i == max:
            print("reach 100000 iteration, ffs...")
            break
    return values 
    
def solve_2(test_string = None) -> int:
    inputs_2 = aoc.get_input(CURRENT_DAY, 2) if not test_string else test_string
    
    new_values = solve_1(inputs_2)
        
    return new_values["a"]


if __name__ == "__main__":
    print(solve_2())