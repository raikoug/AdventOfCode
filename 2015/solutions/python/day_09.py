from starter import AOC, CURRENT_YEAR
from pathlib import Path
import json
import itertools

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

class Distances(dict):
    places: set
    
    def __init__(self):
        self.places = set()

    def add(self, riga: str):
        city1, _, city2, _, distance = riga.split(" ")
        self.places.add(city1)
        self.places.add(city2)
        key1 = f"{city1} {city2}"
        key2 = f"{city2} {city1}"
        value = int(distance)
        self[key1] = value
        self[key2] = value
        
    def print(self):
        print(json.dumps(self, indent=4))
        print(self.places)
        

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    d = Distances()
    for riga in inputs_1.splitlines():
        d.add(riga)
    
    print("Calculating possible paths...")
    possible_paths = list(itertools.permutations(d.places, len(d.places)))
    print("possible_paths: ", len(possible_paths))
    min = 129831290831289039
    for p in possible_paths:
        steps = [f"{p[i]} {p[i+1]}" for i in range(len(p)-1)]
        distance = sum([d[step] for step in steps])
        if distance < min:
            min = distance
            print(min, p)
    
    return min
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    d = Distances()
    for riga in inputs_1.splitlines():
        d.add(riga)
    
    print("Calculating possible paths...")
    possible_paths = list(itertools.permutations(d.places, len(d.places)))
    print("possible_paths: ", len(possible_paths))
    maximum = 0
    for p in possible_paths:
        steps = [f"{p[i]} {p[i+1]}" for i in range(len(p)-1)]
        distance = sum([d[step] for step in steps])
        if distance > maximum:
            maximum = distance
            print(maximum, p)
    
    return maximum

if __name__ == "__main__":
    print(solve_2())