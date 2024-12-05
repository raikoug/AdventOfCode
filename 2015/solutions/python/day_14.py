from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

TIME = 2503


def calc_distance(speed, sprint, sleep, time = TIME):
    # speed is km per second
    # sprint is for how may seconds he can run without stopping
    # sleep is seconds he need to rest
    seconds = 0
    can_sprint = True
    distance = 0
    
    while seconds < time:
        if can_sprint:
            time_sprint = min(sprint, time-seconds)
            distance += time_sprint * speed
            seconds += time_sprint
            can_sprint = False
        else:
            time_sleep = min(sleep, time-seconds)
            seconds += time_sleep
            can_sprint = True
    
    return distance

class Deer:
    name: str
    speed: int
    sprint: int
    sleep: int
    points: int
    distance: int
    
    def __init__(self, s: str):
        splitting = s.split(" ")
        self.name, self.speed, self.sprint, self.sleep = splitting[0], int(splitting[3]), int(splitting[6]), int(splitting[13])
        self.points = 0
        self.distance = 0
        self.s = s
    
    def __str__(self):
        return f"Name: {self.name}, Points: {self.points}"
    
    def __repr__(self):
        return f"Name: {self.name}, Points: {self.points}"
    
    
    def calc_distance(self, time: int) -> int:
        # speed is km per second
        # sprint is for how may seconds he can run without stopping
        # sleep is seconds he need to rest
        seconds = 0
        can_sprint = True
        distance = 0
        
        while seconds < time:
            if can_sprint:
                time_sprint = min(self.sprint, time-seconds)
                distance += time_sprint * self.speed
                seconds += time_sprint
                can_sprint = False
            else:
                time_sleep = min(self.sleep, time-seconds)
                seconds += time_sleep
                can_sprint = True
        
        return distance
            
    def award(self):
        self.points += 1
        

class Race:
    deers: dict
    second: int
    total: int
    
    def __init__(self, total = TIME):
        self.total = total
        self.deers = dict()
        self.second = 0
    
    def add_deer(self, s: str):
        new_deer = Deer(s)
        self.deers[new_deer.name] = new_deer
    
    def tick(self):
        self.second += 1
        results = dict()
        for name, deer in self.deers.items():
            d = deer.calc_distance(self.second)
            if d in results:
                results[d].append(name)
            else:
                results[d] = [name]
        for name in results[sorted(results)[-1]]:
            self.deers[name].award()
        
        #print(self.deers)
        


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    #  Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
    best = 0
    for line in inputs_1.splitlines():
        splitting = line.split(" ")
        distance = calc_distance(int(splitting[3]), int(splitting[6]), int(splitting[13]))
        if distance > best:
            best = distance
    return best
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    deers = list()
    race = Race()
    for line in inputs_1.splitlines():
        race.add_deer(line)
    for i in range(TIME):
        race.tick()
    
    best = None
    for deer in race.deers.values():
        if not best:
            best = deer
        else:
            if deer.points > best.points:
                best = deer
    return best


if __name__ == "__main__":
    print(solve_2())