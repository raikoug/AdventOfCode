from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import Self, List, Dict

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

class Output():
    number: int
    values = List[int]
    
    def __init__(self, number):
        self.number = number
        self.values: List[int] = list()
        
    def __str__(self) -> str:
        return f"Output: {self.number}, Current values: {self.values}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

class Bot():
    number: int
    lower: Self | Output
    higher: Self | Output
    stack: List[int]
    
    def __init__(self, number):
        self.number = number
        self.stack = list()

    def __str__(self) -> str:
        lower = higher = ""
        if hasattr(self, "lower"):
            lower = f", Lower bot: {self.lower.number}"
        if hasattr(self, "higher"):
            higher = f", Higher bot: {self.higher.number}"
        return f"Bot: {self.number}, Current stack: {self.stack}{lower}{higher}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    bots: Dict[int, Bot] = dict()
    outputs: Dict[int, Output] = dict()
    
    for line in inputs_1.splitlines():
        if line.startswith("bot"):
            _, bot_n, _, _, _, low_dest, bot_low_n, _, _, _, high_dest, bot_high_n = line.split(" ")
            bot_n = int(bot_n)
            bot_low_n = int(bot_low_n)
            bot_high_n = int(bot_high_n)
            if bot_n not in bots:
                bots[bot_n] = Bot(bot_n)
            
            if low_dest == "bot":
                if bot_low_n not in bots:
                    bots[bot_low_n] = Bot(bot_low_n)
                bots[bot_n].lower = bots[bot_low_n]
            
            elif low_dest == "output":
                if bot_low_n not in outputs:
                    outputs[bot_low_n] = Output(bot_low_n)
                bots[bot_n].lower = outputs[bot_low_n]
            
            if high_dest == "bot":
                if bot_high_n not in bots:
                    bots[bot_high_n] = Bot(bot_high_n)
                bots[bot_n].higher = bots[bot_high_n]
            
            elif high_dest == "output":
                if bot_high_n not in outputs:
                    outputs[bot_high_n] = Output(bot_high_n)
                bots[bot_n].higher = outputs[bot_high_n]

        if line.startswith("value"):
            _, value, _, _, _, bot_n = line.split(" ")
            value = int(value)
            bot_n = int(bot_n)
            if bot_n not in bots:
                bots[bot_n] = Bot(bot_n)
            
            bots[bot_n].stack.append(value)
            bots[bot_n].stack.sort()
    #print(bots[88])
    #bot: Bot
    target = [17,61] # in ordine!
    while True:
        for n,bot in bots.items():
            if len(bot.stack) == 2:
                print(f"Bot {n} has 2 value in his stack!")
                if bot.stack == target:
                    return n
                if isinstance(bot.lower, Bot):
                    bot.lower.stack.append(bot.stack.pop(0))
                    print(f"    Bot {n} gave to bot {bot.lower.number} the value {bot.lower.stack[-1]}")
                    bot.lower.stack.sort()
                else:
                    bot.lower.values.append(bot.stack.pop(0))
                    print(f"    Bot {n} gave to output {bot.lower.number} the value {bot.lower.values[-1]}")
                
                if isinstance(bot.higher, Bot):
                    bot.higher.stack.append(bot.stack.pop(0))
                    print(f"    Bot {n} gave to bot {bot.higher.number} the value {bot.higher.stack[-1]}")
                    bot.higher.stack.sort()
                else:
                    bot.higher.values.append(bot.stack.pop(0))
                    print(f"    Bot {n} gave to output {bot.higher.number} the value {bot.higher.values[-1]}")
                    

def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    bots: Dict[int, Bot] = dict()
    outputs: Dict[int, Output] = dict()
    
    for line in inputs_1.splitlines():
        if line.startswith("bot"):
            _, bot_n, _, _, _, low_dest, bot_low_n, _, _, _, high_dest, bot_high_n = line.split(" ")
            bot_n = int(bot_n)
            bot_low_n = int(bot_low_n)
            bot_high_n = int(bot_high_n)
            if bot_n not in bots:
                bots[bot_n] = Bot(bot_n)
            
            if low_dest == "bot":
                if bot_low_n not in bots:
                    bots[bot_low_n] = Bot(bot_low_n)
                bots[bot_n].lower = bots[bot_low_n]
            
            elif low_dest == "output":
                if bot_low_n not in outputs:
                    outputs[bot_low_n] = Output(bot_low_n)
                bots[bot_n].lower = outputs[bot_low_n]
            
            if high_dest == "bot":
                if bot_high_n not in bots:
                    bots[bot_high_n] = Bot(bot_high_n)
                bots[bot_n].higher = bots[bot_high_n]
            
            elif high_dest == "output":
                if bot_high_n not in outputs:
                    outputs[bot_high_n] = Output(bot_high_n)
                bots[bot_n].higher = outputs[bot_high_n]

        if line.startswith("value"):
            _, value, _, _, _, bot_n = line.split(" ")
            value = int(value)
            bot_n = int(bot_n)
            if bot_n not in bots:
                bots[bot_n] = Bot(bot_n)
            
            bots[bot_n].stack.append(value)
            bots[bot_n].stack.sort()
    #print(bots[88])
    #bot: Bot
     # in ordine!
    while True:
        for n,bot in bots.items():
            if len(bot.stack) == 2:
                print(f"Bot {n} has 2 value in his stack!")
                if isinstance(bot.lower, Bot):
                    bot.lower.stack.append(bot.stack.pop(0))
                    print(f"    Bot {n} gave to bot {bot.lower.number} the value {bot.lower.stack[-1]}")
                    bot.lower.stack.sort()
                else:
                    bot.lower.values.append(bot.stack.pop(0))
                    print(f"    Bot {n} gave to output {bot.lower.number} the value {bot.lower.values[-1]}")
                
                if isinstance(bot.higher, Bot):
                    bot.higher.stack.append(bot.stack.pop(0))
                    print(f"    Bot {n} gave to bot {bot.higher.number} the value {bot.higher.stack[-1]}")
                    bot.higher.stack.sort()
                else:
                    bot.higher.values.append(bot.stack.pop(0))
                    print(f"    Bot {n} gave to output {bot.higher.number} the value {bot.higher.values[-1]}")
        if all([len(outputs[0].values) == 1,
                len(outputs[1].values) == 1,
                len(outputs[2].values) == 1
                ]):
            return outputs[0].values[0] * outputs[1].values[0] * outputs[2].values[0]
                    



if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")