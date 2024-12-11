import time

def part_one(raw_input: str) -> int:
    counts = get_start_map(raw_input)
    counts = run_steps(counts, 25)
    return sum(counts.values())


def part_two(raw_input: str) -> int:
    counts = get_start_map(raw_input)
    counts = run_steps(counts, 75)
    return sum(counts.values())


def get_start_map(raw_input: str) -> dict[int, int]:
    result = {}
    for num in raw_input.split():
        num = int(num)
        result[num] = result.get(num, 0) + 1
    return result



def run_steps(input_map: dict[int, int], steps: int) -> dict[int, int]:
    counts = input_map
    for _ in range(steps):
        counts = individual_step(counts)
    return counts


def individual_step(input_counts: dict[int, int]) -> dict[int, int]:
    new_counts = {}
    for num, count in input_counts.items():
        if num == 0:
            new_counts[1] = new_counts.get(1, 0) + count
        elif is_even_digits(num):
            new_nums: tuple[int, int] = split(num)
            for new_num in new_nums:
                new_counts[new_num] = new_counts.get(new_num, 0) + count
        else:
            new_num = num * 2024
            new_counts[new_num] = new_counts.get(new_num, 0) + count

    return new_counts


def is_even_digits(num: int) -> bool:
    return len(str(num)) % 2 == 0


def split(num:int) -> tuple[int, int]:
    str_num = str(num)
    new_length = len(str_num) // 2
    return int(str_num[:new_length]), int(str_num[new_length:])


def main():
    with open(r"C:\Temp\Code\AdventOfCode\2024\inputs\day_11\input_1.txt") as f:
        raw_input = f.read().strip()
    start_time = time.time()
    part_one_result = part_one(raw_input)
    mid_time = time.time()
    part_two_result = part_two(raw_input)
    end_time = time.time()
    print(f"Part One: {part_one_result} ("
          f"{(mid_time - start_time) * 1000:.2f}ms)")
    print(f"Part Two: {part_two_result} ("
          f"{(end_time - mid_time) * 1000:.1f}ms)")


if __name__ == "__main__":
    main()