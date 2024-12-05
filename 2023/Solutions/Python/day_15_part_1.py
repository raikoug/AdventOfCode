from icecream import ic


def hasing(line: str, mod: int) -> int:
    ic.configureOutput(prefix=f'{line} -> ')
    current_value = 0
    for char in line:
        ic.configureOutput(prefix=f'{line} | {char} -> ')
        ic(current_value)
        # pahse 1: Determine the ASCII code for the current character of the string
        ascii_code = ord(char)
        ic(ascii_code)
        # phase 2: Add the ASCII code to the total
        current_value += ascii_code
        ic(current_value)
        # phase 3: Multiply the current value by 17
        current_value *= 17
        ic(current_value)
        # phase 4: Module
        current_value %= mod
        ic(current_value)
    
    return current_value


if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)[0]
    
    values = tf.split(",")
    module = 256
    total= 0
    ic.disable()
    for value in values:
        total += hasing(value, module)
    ic.configureOutput(prefix=f'total -> ')
    ic.enable()
    ic(total)
