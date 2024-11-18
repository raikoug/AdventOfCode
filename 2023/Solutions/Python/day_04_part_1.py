import aoc_utils
from pathlib import Path

day = int(Path(__file__).name.split('_')[1])
tf = aoc_utils.get_day_input(day)



def count_left_right(left, right):
    # count how many numbers in the left are in the right
    count = 0
    for l in left:
        if l in right:
            count += 1
    return count

cards = list()
for line in tf:
    card, values = line.split(":") if line else (None, None)
    winnings, numbers = values.split("|")

    cards.append({'winnings': [int(el) for el in winnings.split(' ') if el],
                  'numbers': [int(el) for el in numbers.split(' ') if el]})

total = 0 
for card in cards:
    the_count = count_left_right(card['winnings'], card['numbers'])
    total += 2**(the_count -1 ) if the_count >= 1 else 0
    #print(f"card: {card['winnings']} {card['numbers']} -> {count_left_right(card['winnings'], card['numbers'])}, value: {2**(the_count -1 ) if the_count >= 1 else 0}")
    

print(total)
#print(cards)