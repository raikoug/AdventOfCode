from icecream import ic

class Reading:
    def __init__(self, data: str):
        # data will be like this:
        # "0 3 6 9 12 15"
        numbers = [int(el) for el in data.split(" ")]
        self.numbers = list()
        self.numbers.append(numbers)

    def next(self):
        # The next array will be evaluated as follows:
        #   0   3   6   9   12   15   (making diffs from actual numbers):
        #     3    3  3   3    3               (diffs)
        tmp = list()
        for i in range(1, len(self.numbers[-1])):
            tmp.append(self.numbers[-1][i] - self.numbers[-1][i-1])
        self.numbers.append(tmp)

    def recursive_add_new_value(self):
        # add a 0 to the end of self.numebers[-1]
        # and then add the new value to the end of self.numbers[-2] (the one before)
        #     this new number will be X that X - self.numbers[-2][-1] = self.numbers[-1][-1]
        #  go on with self.numbers[-3] with a value X that X - self.numbers[-3][-1] = self.numbers[-2][-1]
        self.numbers[-1].append(0)
        for i in reversed(range(len(self.numbers)-1)):
            self.numbers[i].append(self.numbers[i+1][-1] + self.numbers[i][-1])

    def all_zeroes(self) -> bool:
        for el in self.numbers[-1]:
            if el != 0:
                return False
        return True

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    
    R = [Reading(line) for line in tf]
    max = len(R)
    max_s = len(str(max))
    i = 0
    print(f"{i:>{max_s}}/{max}", end="\r")
    all_zeroes = False
    for r in R:
        while not all_zeroes:
            r.next()
            all_zeroes = r.all_zeroes()
            i += 1
            print(f"{i:>{max_s}}/{max}", end="\r")

        all_zeroes = False

    totals = 0 
    for r in R:
        r.recursive_add_new_value()
        totals += r.numbers[0][-1]
    
    ic(totals)
