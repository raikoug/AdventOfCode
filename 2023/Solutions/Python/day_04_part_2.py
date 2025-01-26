from icecream import ic

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

cards = dict()
winned_cards_from_before = dict()
# winned_cards_from_before will ahve the format
# { X: quantity,
#   Y: quantity,
#   Z: qantity,
#   ....
# }

total = 0
for line in tf:
    card, values = line.split(":") if line else (None, None)
    try:
        card_id = int(card.split(' ')[1])
    except:
        ic(line)
    winnings, numbers = values.split("|")

    cards[card_id] = {'winnings': [int(el) for el in winnings.split(' ') if el],
                      'numbers': [int(el) for el in numbers.split(' ') if el],
                      'quantity': 1}
    # check if winned cards from before has this card id, add it to wuantities
    if card_id in winned_cards_from_before:
        cards[card_id]['quantity'] += winned_cards_from_before[card_id]
    
    to_add = cards[card_id]['quantity']
    total += to_add

    # check winnings from this card and multiply for quantity
    winnings = count_left_right(cards[card_id]['winnings'], cards[card_id]['numbers'])

    # winned_cards_from_before add the winnings,
    #   if the winning is 5: 
    #           - winned_cards_from_before[card_id+1] += cards[card_id]['quantity']
    #           - winned_cards_from_before[card_id+2] += cards[card_id]['quantity']
    #           - winned_cards_from_before[card_id+3] += cards[card_id]['quantity']
    #           - winned_cards_from_before[card_id+4] += cards[card_id]['quantity']
    #           - winned_cards_from_before[card_id+5] += cards[card_id]['quantity']

    new_card_id = card_id
    while winnings > 0:
        new_card_id += 1
        if new_card_id in winned_cards_from_before:
            winned_cards_from_before[new_card_id] += to_add
        else:
            winned_cards_from_before[new_card_id] = to_add
        winnings -= 1
    

print(total)