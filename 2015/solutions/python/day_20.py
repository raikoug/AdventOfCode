from starter import AOC, CURRENT_YEAR
from pathlib import Path
from collections import Counter
from itertools import product
from math import prod

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def is_prime(n, primes) -> bool:
    for prime in primes:
        if n % prime == 0:
            return False
    return True

extract_primes = lambda x: [el for el in x if el]

def useful_primes(massimo) -> list:
    primes = list()
    all_numbers = [i for i in range(0,massimo+1)]
    primes = [2,3,5,7,11,13]
    all_numbers[0] = False
    all_numbers[1] = False
    for prime in primes:
        lenght = len(all_numbers[prime*2::prime])
        all_numbers[prime*2::prime] = [False] * lenght
    
    i = 14
    while True:
        if all_numbers[i]:
            primes.append(i)
            lenght = len(all_numbers[i*2::i])
            all_numbers[i*2::i] = [False] * lenght
        i += 1
        if i > (massimo ** 0.5):
            break
    return extract_primes(all_numbers)

def fattorizzazione(x: int, primes: list):
    for p in primes:
        if p > x/2:
            #last check
            if x in primes:
                yield x
            break
        while x % p == 0:
            yield p
            x //= p

def divisori(lst):
    counts = Counter(lst)
    elements = list(counts.keys())
    max_counts = [counts[elem] for elem in elements]

    # Genera tutte le possibili combinazioni di conteggi per gli elementi
    count_combinations = [range(count + 1) for count in max_counts]

    # Genera tutte le combinazioni possibili rispettando i conteggi massimi
    all_combinations = list()
    for counts in product(*count_combinations):
        if any(counts):  # Esclude la combinazione con tutti zero
            combination = []
            for elem, count in zip(elements, counts):
                combination.extend([elem] * count)
            # Ordina la combinazione per evitare duplicati come [5, 2] e [2, 5]
            all_combinations.append(sorted(combination))

    # Rimuove eventuali duplicati
    unique_combinations = []
    [unique_combinations.append(x) for x in all_combinations if x not in unique_combinations]
    return unique_combinations


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    target = int(inputs_1)
    real_target = target//10
    print("Generating primes...")
    primes = useful_primes(real_target)
    print("Primes generated")
    i = 10000000
    while True:
        fattori_primi = list(fattorizzazione(i,primes))
        regali = sum([prod(lst) for lst in divisori(fattori_primi) + [[1]]])
        if regali == real_target:
            return i
        i += 1
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
        
    return 1


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")