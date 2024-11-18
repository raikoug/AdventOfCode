from collections import defaultdict

target = 29000000

def part1(upperBound):
    houses = defaultdict(int)

    for elf in range(1, target):
        for house in range(elf, upperBound, elf):
            houses[house] += elf*10
            
        if houses[elf] >= target:
            return elf

def part2(upperBound):
    houses = defaultdict(int)

    for elf in range(1, target):
        for house in range(elf, min(elf*50+1, upperBound), elf):
            houses[house] += elf*11
            
        if houses[elf] >= target:
            return elf

            
print( part1(1000000))
print( part2(1000000))