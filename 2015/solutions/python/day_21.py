from starter import AOC, CURRENT_YEAR
from pathlib import Path
from queue import PriorityQueue
from typing import List, Self
from itertools import combinations, product

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

class Item:
    Cost: int
    Damage: int
    Armor: int
    name: str
    id: int
    
    def __init__(self, name, Cost, Damage, Armor, id):
        self.Cost = Cost
        self.Damage = Damage
        self.Armor = Armor
        self.name = name
        self.id = id
        
    def __le__(self, other):
        return self.id <= other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __hash__(self):
        return self.id
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()
    
    def __format__(self):
        return self.__str__()

class Character:
    dmg: int
    arm: int
    hp:  int
    build_cost: int
    items: list
    
    def __init__(self, dmg: int = 0, arm: int = 0, hp: int = 100, clone: Self = False):

        self.dmg = dmg if not clone else clone.dmg
        self.arm = arm if not clone else clone.arm
        self.hp  = hp if not clone else clone.hp
        self.build_cost = 0
        self.items = list()
    
    def equip(self, items: List[Item]):
        for item in items:
            self.dmg += item.Damage
            self.arm += item.Armor
            self.build_cost += item.Cost
            self.items.append(item)

    def __str__(self):
        return f"dmg: {self.dmg:> 3} arm: {self.arm:> 3} hp: {self.hp} build_cost: {self.build_cost}"
    
    def __repr__(self):
        return self.__str__()
    
    def __format__(self):
        return self.__str__()
    
    def __le__(self, other : Self):
        return self.build_cost <= other.build_cost
    
    def __lt__(self, other : Self):
        return self.build_cost < other.build_cost
    
    def __eq__(self, other : Self):
        return self.build_cost == other.build_cost

    def __ne__(self, other : Self):
        return self.build_cost != other.build_cost

    def __gt__(self, other : Self):
        return self.build_cost > other.build_cost

    def __ge__(self, other : Self):
        return self.build_cost >= other.build_cost

    def __hash__(self):
        return self.build_cost
    
            
class Boss:
    dmg: int
    arm: int
    hp:  int
    
    def __init__(self, dmg: int, arm: int, hp: int):
        self.dmg = dmg
        self.arm = arm
        self.hp  = hp
    
    def __str__(self):
        return f"dmg: {self.dmg:> 3} arm: {self.arm:> 3} hp: {self.hp}"
    
    def __repr__(self):
        return self.__str__()
    
    def __format__(self):
        return self.__str__()

class Game:
    character: Character
    boss: Boss
    step: int
    
    def __init__(self, character: Character, boss: Boss):
        self.character = character
        self.boss = boss
        self.step = 0
    
    def next_step(self):
        self.step += 1
        if self.step % 2 == 1:
            # character turn!
            self.boss.hp -= max(1, self.character.dmg - self.boss.arm)
        else:
            self.character.hp -= max(1, self.boss.dmg - self.character.arm)
    
    def play(self):
        while True:
            self.next_step()
            if self.character.hp <= 0: 
                return 0
            if self.boss.hp <= 0: 
                return 1
            
WEAPONS = [
    Item("Dagger", 8,4,0,1),
    Item("Shortsword", 10,5,0,2),
    Item("Warhammer", 25,6,0,3),
    Item("Longsword", 40,7,0,4),
    Item("Greataxe", 74,8,0,5)
    ]
ARMORS = [
    Item("Leather",13,0,1,6),
    Item("Chainmail",31,0,2,7),
    Item("Splintmail",53,0,3,8),
    Item("Bandedmail",75,0,4,9),
    Item("Platemail",102,0,5,10)
]
RINGS = [
    Item("Damage +1",25,1,0,11),
    Item("Damage +2",50,2,0,12),
    Item("Damage +3",100,3,0,13),
    Item("Defense +1",20,0,1,14),
    Item("Defense +2",40,0,2,15),
    Item("Defense +3",80,0,3,16)
]

def all_combinations() -> list:

    # Genera combinazioni da A (1 elemento)
    combinations_A = [[elem] for elem in WEAPONS]

    # Genera combinazioni da B (0 o 1 elemento)
    combinations_B = [[], *[[elem] for elem in ARMORS]]

    # Genera combinazioni da C (0, 1 o 2 elementi, senza ripetizioni)
    combinations_C = [[]]
    combinations_C += [[elem] for elem in RINGS]
    combinations_C += [list(pair) for pair in combinations(RINGS, 2)]

    # Insieme per memorizzare le combinazioni uniche
    unique_combinations = set()

    # Genera tutte le combinazioni possibili rispettando le condizioni
    for a, b, c in product(combinations_A, combinations_B, combinations_C):
        # Combina gli elementi di A, B e C
        combined = a + b + c
        if combined:
            # Ordina la combinazione per evitare duplicati come [1,4] e [4,1]
            sorted_combined = tuple(sorted(combined))
            unique_combinations.add(sorted_combined)

    # Stampa le combinazioni uniche
    return unique_combinations


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string

    boss_hp     = int(inputs_1.splitlines()[0].replace("Hit Points: ", ""))
    boss_damage = int(inputs_1.splitlines()[1].replace("Damage: ", ""))
    boss_armor  = int(inputs_1.splitlines()[2].replace("Armor: ", ""))
    base_char = Character(0,0,100)
    characters=PriorityQueue()
    for purchase in all_combinations():
        new_char = Character(clone = base_char)
        new_char.equip(purchase)
        characters.put([new_char.build_cost, new_char])
    # each character in characters is :
    # [cost, character] tuple

    while True:
        boss = Boss(boss_damage, boss_armor, boss_hp)
        cost,character = characters.get()
        game = Game(character, boss)
        result = game.play()
        if result == 1:
            break
    
    print(character)
    return cost
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string

    boss_hp     = int(inputs_1.splitlines()[0].replace("Hit Points: ", ""))
    boss_damage = int(inputs_1.splitlines()[1].replace("Damage: ", ""))
    boss_armor  = int(inputs_1.splitlines()[2].replace("Armor: ", ""))
    base_char = Character(0,0,100)
    characters=PriorityQueue()
    for purchase in all_combinations():
        new_char = Character(clone = base_char)
        new_char.equip(purchase)
        characters.put([-new_char.build_cost, new_char])

    while True:
        boss = Boss(boss_damage, boss_armor, boss_hp)
        cost,character = characters.get()
        game = Game(character, boss)
        result = game.play()
        if result == 0:
            break
        
    print(character, character.items)
    return character.build_cost


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")