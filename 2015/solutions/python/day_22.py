from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import Self, Dict, Set, List
from queue import PriorityQueue

DEBUG = 0

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

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

class Spell:
    name: str
    cost: int
    damage: int
    heal: int
    armor: int
    duration: int
    manaboost: int
    
    def __init__(self, name: str,     cost: int,      damage: int = 0, 
                       heal: int = 0, armor: int = 0, duration: int = 0, 
                       manaboost: int = 0):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.heal = heal
        self.armor = armor
        self.duration = duration
        self.manaboost = manaboost
    
    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return self.__repr__()
    
    def __format__(self):
        return self.__repr__()
    
    def __hahs__(self):
        return self.cost
    
    def __le__(self, other : Self):
        return self.cost <= other.cost
    
    def __lt__(self, other : Self):
        return self.cost < other.cost
    
    def __eq__(self, other : Self):
        return self.cost == other.cost

    def __ne__(self, other : Self):
        return self.cost != other.cost

    def __gt__(self, other : Self):
        return self.cost > other.cost

    def __ge__(self, other : Self):
        return self.cost >= other.cost

class Spells(list[Spell]):
    pass

class Character:
    dmg: int
    arm: int
    hp:  int
    mana: int
    mana_used: int
    spells: Spells
    
    def __init__(self, dmg:   int = 0,   arm:  int = 0, 
                       hp:    int = 50,  mana: int = 500, 
                       clone: Self = False):

        self.dmg = dmg if not clone else clone.dmg
        self.arm = arm if not clone else clone.arm
        self.hp  = hp if not clone else clone.hp
        self.mana = mana if not clone else clone.mana
        self.mana_used = 0
        self.spells = Spells()

    def action(self):
        # return armor, damage, heal, manaboost, spell
        
        spell = self.spells.pop(0) if self.spells else False
        armor = spell.armor  if spell else 0
        damage = spell.damage if spell else 0
        heal = spell.heal if spell else 0
        manaboost = spell.manaboost if spell else 0
        self.mana_used += spell.cost if spell else 0
        self.mana -= spell.cost if spell else 0
        
        return armor, damage, heal, manaboost, spell
           
    def __str__(self):
        return f"dmg: {self.dmg:> 3} arm: {self.arm:> 3} hp: {self.hp} mana: {self.mana}"
    
    def __repr__(self):
        return self.__str__()
    
    def __format__(self):
        return self.__str__()
    
    def __le__(self, other : Self):
        return self.mana <= other.mana
    
    def __lt__(self, other : Self):
        return self.mana < other.mana
    
    def __eq__(self, other : Self):
        return self.mana == other.mana

    def __ne__(self, other : Self):
        return self.mana != other.mana

    def __gt__(self, other : Self):
        return self.mana > other.mana

    def __ge__(self, other : Self):
        return self.mana >= other.mana

    def __hash__(self):
        return self.mana

class Effect:
    spell: Spell
    remain: int
    
    def __init__(self, spell: Spell):
        self.spell = spell
        self.remain = spell.duration
        
    def play_effect(self):
        self.remain -=1 
        return self.spell.armor, self.spell.damage, self.spell.heal, self.spell.manaboost

class Effects(list[Effect]):
    pass

class Game:
    character: Character
    boss: Boss
    step: int
    active_effects = Effects
    v2: bool
    
    def __init__(self, character: Character, boss: Boss, v2: bool = False):
        self.character = character
        self.boss = boss
        self.step = 0
        self.active_effects = Effects()
        self.v2 = v2
    
    def next_step(self):
        self.step += 1
        # before, effects apply
        spacing = "-"* (self.step % 2)*50
        if self.v2: 
            self.character.hp -= 1
            if self.character.hp <= 0:
                return

        if DEBUG: print(f"{spacing}New Turn")
        if DEBUG: print(f"{spacing}Character:",self.character)
        if DEBUG: print(f"{spacing}Boss:",self.boss)
        if DEBUG: print(f"{spacing} Effects")
        for effect in self.active_effects:
            if DEBUG: print(f"{spacing}  Spell: {effect.spell.name:>.9} - Remains: {effect.remain} Turns")
            armor, damage, heal, manaboost = effect.play_effect()
            if armor:
                pass
            if damage:
                if DEBUG: print(f"{spacing}      Damaging boss for: {effect.spell.damage}")
                self.boss.hp -= damage
                if DEBUG: print(f"{spacing}          Boss HP: {self.boss.hp}")
            
            if heal:
                if DEBUG: print(f"{spacing}      Healing Character for: {effect.spell.heal}")
                self.character.hp += heal
                if DEBUG: print(f"{spacing}          Character HP: {self.character.hp}")
            
            if manaboost:
                if DEBUG: print(f"{spacing}      Recovering Character Mana for: {effect.spell.manaboost}")
                self.character.mana += manaboost
                if DEBUG: print(f"{spacing}          Character mana: {self.character.mana}")
        
        # check if remove effect:
        for effect in self.active_effects:
            armor, damage, heal, manaboost = 0,0,0,0
            if effect.remain == 0:
                if DEBUG: print(f"{spacing}  Spell: {effect.spell.name:>9} - exhausted")
                if armor:
                    if DEBUG: print(f"{spacing}      Removing {effect.spell.armor} armor from player")
                    self.character.arm -= armor
                
                self.active_effects.remove(effect)
        
        
        if self.boss.hp <= 0:
            return
        
        if self.step % 2 == 1:
            if DEBUG: print(f"{spacing}  Character Turn")
            # character turn!
            armor, damage, heal, manaboost, spell = self.character.action()
            if not spell:
                print(f"{spacing}   Caracter out of actions, lose!")
                self.character.hp = -1
                return
            if DEBUG: print(f"{spacing}      Character cast {spell.name}")
            if armor:
                if DEBUG: print(f"{spacing}        Character increas armor of {armor}")
                self.character.arm += armor
                self.active_effects.append(Effect(spell))
                if DEBUG: print(f"{spacing}          Character armor: {self.character.arm}")
            
            if damage and spell.duration == 0:
                if DEBUG: print(f"{spacing}        Character damage boss for {damage}")
                self.boss.hp -= damage
                if DEBUG: print(f"{spacing}          Boss HP: {self.boss.hp}")
                

            elif (damage and spell.duration > 0) or manaboost:
                if DEBUG: print(f"{spacing}        Character does not damage boss, effect apply nect turn...")
                self.active_effects.append(Effect(spell))
            
            if heal:
                if DEBUG: print(f"{spacing}        Character heals for {heal} hp")
                self.character.hp += heal
                if DEBUG: print(f"{spacing}          Character HP: {self.character.hp}")
            
                
            
        else:
            # boss turn
            if DEBUG: print(f"{spacing}  Boss Turn")
            if DEBUG: print(f"{spacing}      Boss attack player for {self.boss.dmg} - {self.character.arm} armor: {max(1, self.boss.dmg - self.character.arm)}")
            self.character.hp -= max(1, self.boss.dmg - self.character.arm)
            if DEBUG: print(f"{spacing}          Character HP: {self.character.hp}")
    
    def play(self):
        while True:
            self.next_step()
            if self.character.hp <= 0: 
                if DEBUG: print(f"  Boss WIN")
                return 0
            if self.boss.hp <= 0: 
                if DEBUG: print(f"  Character WIN")
                return 1


SPELLS = {
    "Magic Missile" : Spell("Magic Missile", 53, damage = 4, heal = 0, armor = 0, 
                                                 duration = 0, manaboost = 0),
    "Drain" :         Spell("Drain",         73, damage = 2, heal = 2, armor = 0, 
                                                 duration = 0, manaboost = 0),
    "Shield" :        Spell("Shield",       113, damage = 0, heal = 0, armor = 7, 
                                                 duration = 6, manaboost = 0),
    "Poison" :        Spell("Poison",       173, damage = 3, heal = 0, armor = 0, 
                                                 duration = 6, manaboost = 0),
    "Recharge" :      Spell("Recharge",     229, damage = 0, heal = 0, armor = 0, 
                                                 duration = 5, manaboost = 101)
}

def generate_sequences(N: int, boss_hp_initial: int, mana: int = 500) -> PriorityQueue:
    sequences = PriorityQueue()

    def can_cast(spell: Spell, active_effects: Dict[str, int]) -> bool:
        # Non si può lanciare uno spell se l'effetto è ancora attivo
        if spell.duration > 0 and spell.name in active_effects:
            return False
        return True

    def apply_effects(active_effects: Dict[str, int], mana: int, boss_hp: int):
        new_effects = active_effects.copy()
        # Applica gli effetti attivi
        for effect in list(active_effects.keys()):
            spell = SPELLS[effect]
            # Applica effetti
            if spell.name == "Recharge":
                mana += spell.manaboost
            elif spell.name == "Poison":
                boss_hp -= 3  # "Poison" infligge 3 danni per applicazione
            # Decrementa il timer
            new_effects[effect] -= 1
            if new_effects[effect] == 0:
                del new_effects[effect]
        return new_effects, mana, boss_hp

    def backtrack(turn: int, sequence: List[Spell], mana: int, active_effects: Dict[str, int],
                  boss_hp: int, player_turn: bool):
        # Applica gli effetti all'inizio di ogni turno
        active_effects, mana, boss_hp = apply_effects(active_effects, mana, boss_hp)

        # Verifica se il boss è stato sconfitto
        if boss_hp <= 0:
            total_cost = sum(spell.cost for spell in sequence)
            sequences.put((total_cost, sequence.copy()))
            return

        # PRUNING: Se il mana è negativo, interrompi l'esplorazione
        if mana < 0:
            return

        # Se abbiamo raggiunto il numero massimo di turni, interrompi
        if turn == N:
            return

        if player_turn:
            # Turno del giocatore
            # Genera la lista degli incantesimi che si possono lanciare
            available_spells = []
            for spell in SPELLS.values():
                if spell.cost <= mana and can_cast(spell, active_effects):
                    available_spells.append(spell)

            # Se non ci sono incantesimi disponibili, termina la sequenza
            if not available_spells:
                return

            # Prova a lanciare ogni incantesimo disponibile
            for spell in available_spells:
                # Aggiorna lo stato per il prossimo turno
                new_sequence = sequence.copy()
                new_sequence.append(spell)
                new_mana = mana - spell.cost

                # PRUNING: Se il mana diventa negativo dopo aver lanciato lo spell, interrompi
                if new_mana < 0:
                    continue

                new_active_effects = active_effects.copy()
                new_boss_hp = boss_hp

                # Applica gli effetti dello spell lanciato
                # Danno immediato
                if spell.damage > 0 and spell.duration == 0:
                    new_boss_hp -= spell.damage
                # Effetti di durata
                if spell.duration > 0:
                    new_active_effects[spell.name] = spell.duration

                # Verifica se il boss è stato sconfitto dopo il lancio dello spell
                if new_boss_hp <= 0:
                    total_cost = sum(spell.cost for spell in new_sequence)
                    sequences.put((total_cost, new_sequence.copy()))
                    return

                # Avanza al turno successivo (turno del boss)
                backtrack(turn + 1, new_sequence, new_mana, new_active_effects, new_boss_hp, player_turn=False)
        else:
            # Turno del boss
            # Il boss attacca (puoi implementare la logica dell'attacco se necessario)
            # In questo esempio, ignoriamo l'attacco del boss per focalizzarci sulla sconfitta del boss
            # Avanza al prossimo turno (turno del giocatore)
            backtrack(turn, sequence, mana, active_effects, boss_hp, player_turn=True)

    # Inizia il backtracking dal turno 0, turno del giocatore
    backtrack(0, [], mana, {}, boss_hp_initial, player_turn=True)
    return sequences

def solve_1(test_string = None, char_string: str = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    boss_hp = int(inputs_1.splitlines()[0].replace("Hit Points: ", ""))
    boss_dmg = int(inputs_1.splitlines()[1].replace("Damage: ", ""))
    if char_string:
        char_hp = int(char_string.splitlines()[0].replace("Hit Points: ", ""))
        char_mana = int(char_string.splitlines()[1].replace("Mana: ", ""))
    else:
        char_hp = 50
        char_mana = 500
    N = 10
    print(f"Generating sequences")
    all_sequences = generate_sequences(N, boss_hp, char_mana)
    print(f"Sequences generates")

    while True:
        if all_sequences.empty():
            print(f"No valid sequence for {N} spells")
            cost = 0
            break
        boss = Boss(boss_dmg, 0, boss_hp)
        char = Character(hp=char_hp, mana=char_mana)
        
        cost, spells = all_sequences.get()
        char.spells = list(spells)
    
        game = Game(char, boss)
        res = game.play()
        if res == 1:
            print(f"Player Wins!")
            print(spells)
            print(char.mana_used)
            break
        else:
            pass
            #print(f"Boss Wins")
    
    #boss = Boss(boss_dmg, 0, boss_hp)
    #char = Character(hp=char_hp, mana=char_mana)
    #char.spells = list(spells)
    #global DEBUG
    #DEBUG = 1
    #game = Game(char, boss)
    #res = game.play()
    
    
    return cost
    
def solve_2(test_string = None, char_string: str = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    boss_hp = int(inputs_1.splitlines()[0].replace("Hit Points: ", ""))
    boss_dmg = int(inputs_1.splitlines()[1].replace("Damage: ", ""))
    if char_string:
        char_hp = int(char_string.splitlines()[0].replace("Hit Points: ", ""))
        char_mana = int(char_string.splitlines()[1].replace("Mana: ", ""))
    else:
        char_hp = 50
        char_mana = 500
    N = 10
    print(f"Generating sequences")
    all_sequences = generate_sequences(N, boss_hp, char_mana)
    print(f"Sequences generates")

    while True:
        if all_sequences.empty():
            print(f"No valid sequence for {N} spells")
            cost = 0
            break
        boss = Boss(boss_dmg, 0, boss_hp)
        char = Character(hp=char_hp, mana=char_mana)
        
        cost, spells = all_sequences.get()
        char.spells = list(spells)
    
        game = Game(char, boss, True)
        res = game.play()
        if res == 1:
            print(f"Player Wins!")
            print(spells)
            print(char.mana_used)
            break
        else:
            pass
            #print(f"Boss Wins")
    
    #boss = Boss(boss_dmg, 0, boss_hp)
    #char = Character(hp=char_hp, mana=char_mana)
    #char.spells = list(spells)
    #global DEBUG
    #DEBUG = 1
    #game = Game(char, boss)
    #res = game.play()
    
    
    return cost


if __name__ == "__main__":
    fake_game_1 = """Hit Points: 13
Damage: 8
"""
    fake_char_1 = """Hit Points: 10
Mana: 250
"""
    fake_game_2 = """Hit Points: 14
Damage: 8
"""
    fake_char_2 = """Hit Points: 10
Mana: 250
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")