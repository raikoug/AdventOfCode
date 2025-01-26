from icecream import ic
import functools

class Hand:
    str: str
    bid: int
    rank: int
    place: int
    type: int

    def __init__(self, hand: str, bid: int):
        self.hand = hand
        self.bid = bid
        self.rank = 0
        self.place = 0
        self.type = self.calc_type()

    def calc_type(self):
        """
        7. Five of a kind, where all five cards have the same label: AAAAA
        6. Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        5. Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        4. Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        3. Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        2. One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        1. High card, where all cards' labels are distinct: 23456
        """
        # just for this part I order the self.str
        hand = "".join(sorted(self.hand))
        scores = []
        # count istance of the first char and store it in a list, then remove the char from the hand
        Js = 0
        while len(hand) > 0:
            char = hand[0]
            count = hand.count(char)
            if char == "J":
                Js = count
            else:  
                scores.append(count)
            
            hand = hand.replace(char, "")

        scores.sort()
        # add Js value to highest
        if scores: scores[-1] += Js
        else: scores.append(Js)
        if scores == [1, 1, 1, 1, 1]:
            return 1
        elif scores == [1, 1, 1, 2]:
            return 2
        elif scores == [1, 2, 2]:
            return 3
        elif scores == [1, 1 , 3]:
            return 4
        elif scores == [2, 3]:
            return 5
        elif scores == [1, 4]:
            return 6
        elif scores == [5]:
            return 7

CM = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

def compare_2_hands(left, right):
    if left.type > right.type:
        return -1
    elif left.type < right.type:
        return 1
    else:
        # from left ro right of hand.hand string, win the one with the highest char where char order is:
        # A > K > Q > J > T > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2 (using CM)
        for i in range(len(left.hand)):
            if CM[left.hand[i]] > CM[right.hand[i]]:
                return -1
            elif CM[left.hand[i]] < CM[right.hand[i]]:
                return 1
    

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    
    hands = list()
    for line in tf:
        hand, bid = line.split(" ")
        H = Hand(hand, int(bid))
        hands.append(H)
    #import sys; sys.exit(0)
    # sort the hands by type
    hands.sort(key=functools.cmp_to_key(compare_2_hands), reverse=True)
    place = 1
    total = 0
    for h in hands:
        h.place = place
        place += 1
        total += h.bid*h.place
    print(total)