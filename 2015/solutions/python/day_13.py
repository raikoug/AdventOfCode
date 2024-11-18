from starter import AOC, CURRENT_YEAR
from pathlib import Path
import json
from IPython import embed
import itertools


CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

class Person(dict):
    name: str
    
    def __init__(self, person_lines: list):
        # Alice would gain 2 happiness units by sitting next to Bob.
        # Alice would lose 82 happiness units by sitting next to David.
        # ...
        self.name = person_lines[0].split(" ")[0]
        for line in person_lines:
            mult = 1 if "gain" in line else -1
            name, _, _, value, _, _, _, _, _, _, target = line.split(" ")
            value = int(value) * mult
            self[target] = value
    
    def __dict__(self):
        result = dict(self)
        result["name"] = self.name
        return result

class Table:
    persons: dict
    seats: list
    count: int
    peoples: set
    v2: bool
    
    def __init__(self, s: str, v2 = False):
        self.v2 = v2
        self.persons = dict()
        self.seats = list()
        self.peoples = set([line.split(" ")[0] for line in s.splitlines()])
        if v2:
            for person in self.peoples:
                # add line with
                #  Me would gain 0 happiness units by sitting next to {person}
                # for each person
                # and for each person a line
                #  {person} would gain 0 happiness units by sitting next to Me
                
                s += f"Me would gain 0 happiness units by sitting next to {person}\n"
                s += f"{person} would gain 0 happiness units by sitting next to Me\n"
            
            self.peoples.add("Me")
            
        self.count = len(self.peoples)
        for person in self.peoples:
            person_list = [line for line in s.splitlines() if line.startswith(person)]
            self.persons[person] = Person(person_list)
    
    def calc_happiness(self) -> int:
        happiness = 0
        for i,person in enumerate(self.seats):
            #print(f"{person} is near {self.seats[i-1]} and {self.seats[(i+1)%self.count]}")
            happiness += self.persons[person][self.seats[i-1]]
            happiness += self.persons[person][self.seats[(i+1)%self.count]]
        return happiness
            

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    inputs_1 = inputs_1.replace(".", "")
    t = Table(inputs_1)
    # t.peoples contains the list of person, now the hard part, all the combinations
    all_combinations = itertools.permutations(t.peoples, t.count)
    usefull_combinations = list()
    for combination in all_combinations:
        if (not combination in usefull_combinations) and (not combination[::-1] in usefull_combinations):
            usefull_combinations.append(combination)
    print(len(usefull_combinations))
    happiness = -10000000
    for combination in usefull_combinations:
        t.seats = combination
        new = t.calc_happiness()
        if new > happiness:
            happiness = new
    return happiness

def print_progress(total, current, perc):
    lenght = 100
    half_symbol = "▄"
    full_symbol = "█"
    unde_symbol = "▁"
    half = perc % 2
    full = perc- half
    unde = lenght - half - full
    
    print(f"{full_symbol*full}{half_symbol*half}{unde_symbol*unde} {perc:> 3}%", end="\r")
    

def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    inputs_1 = inputs_1.replace(".", "")
    t = Table(inputs_1, True)
    print("Table done, calculating all combinations...")
    # t.peoples contains the list of person, now the hard part, all the combinations
    all_combinations = list(itertools.permutations(t.peoples, t.count))
    
    print(f"Combinations done: {len(all_combinations)}, calculating happiness..")
    
    # progress barr (a kink...)
    total = len(all_combinations)
    current = 0
    perc = int(current/total*100)
    print_progress(total, current, perc)
    
    happiness = -10000000
    for combination in all_combinations:
        current +=1 
        if int((current/total)*100) > perc:
            perc = int((current/total)*100)
            print_progress(total, current, perc)
        t.seats = combination
        new = t.calc_happiness()
        if new > happiness:
            happiness = new
    print()
    return happiness


if __name__ == "__main__":
    print(solve_2())