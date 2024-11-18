from icecream import ic


class Lens:
    id: str
    focal: int
    def __init__(self, id: str, focal: int = 0):
        self.focal = focal
        self.id = id

class Box:
    label: str
    lens: list
    def __init__(self, label: str, lens: list):
        self.label = label
        self.lens = lens

    def action(self, lens: Lens, action: str):
        """
        If the operation character is a dash (-), go to the relevant box and remove the lens 
        with the given label if it is present in the box. Then, move any remaining lenses as 
        far forward in the box as they can go without changing their order, filling any space 
        made by removing the indicated lens. (If no lens in that box has the given label, 
        nothing happens.)

        If the operation character is an equals sign (=), it will be followed by a number 
        indicating the focal length of the lens that needs to go into the relevant box; be 
        sure to use the label maker to mark the lens with the label given in the beginning 
        of the step so you can find it later. There are two possible situations:
            - If there is already a lens in the box with the same label, replace the old lens 
            with the new lens: remove the old lens and put the new lens in its place, not moving 
            any other lenses in the box.
            -If there is not already a lens in the box with the same label, add the lens to 
            the box immediately behind any lenses already in the box. Don't move any of the 
            other lenses when you do this. If there aren't any lenses in the box, the new lens 
            goes all the way to the front of the box.
        """
        # and here come the astonishing lens _lens idea...
        if action == '-':
            for _lens in self.lens:
                if _lens.id == lens.id:
                    self.lens.remove(_lens)
                    break
            return

        # if we are here action is = 
        for _lens in self.lens:
            if _lens.id == lens.id:
                # substitute lens with the new focal
                _lens.focal = lens.focal
                return
        
        # if we are here, the lens is not in the box, we add it!
        self.lens.append(lens)

    def __str__(self):
        ### Box 3: [pc 4] [ot 9] [ab 5]
        res = f'Box {self.label}: '
        for _lens in self.lens:
            res += f'[{_lens.id} {_lens.focal}] '
        return res
    
    def __repr__(self):
        return self.__str__()

def hashing(line: str, mod: int = 256) -> int:
    ic.configureOutput(prefix=f'{line} -> ')
    current_value = 0
    for char in line:
        # pahse 1: Determine the ASCII code for the current character of the string
        ascii_code = ord(char)
        # phase 2: Add the ASCII code to the total
        current_value += ascii_code
        # phase 3: Multiply the current value by 17
        current_value *= 17
        # phase 4: Module
        current_value %= mod
    
    return current_value

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)[0]

    
    values = tf.split(",")
    actions = list()
    for value in values:
        """
            values can be '[BoxID]=y' or '[BoxId]-'
            BoxId is the lens id too.
            = or - are the possible actions.
        """
        if '=' in value:
            box, focal = value.split('=')
            actions.append([box, focal, '='])
        else:
            box = value[:-1]
            actions.append([box, '-', '-'])
    
    boxes = dict()
    for action in actions:
        ic.configureOutput(prefix=f'{action} -> ')
        id = action[0]
        focal = int(action[1]) if action[1] not in ['-', '='] else 0
        operation = action[2]
        # box label is converted to numbers
        box_n = hashing(id)
        if box_n not in boxes:
            boxes[box_n] = Box(box_n, list())
            # lens id is kept as string not hashed
        
        lens = Lens(id, focal)
        boxes[box_n].action(lens, operation)
    ic.configureOutput(prefix=f'boxes -> ')
    totals = 0
    for k,box in boxes.items():
        for i,lens in enumerate(box.lens):
            #ic(k+1, i+1, lens.focal, (k+1)*(i+1)*lens.focal)
            totals += (k+1)*(i+1)*lens.focal
    ic.configureOutput(prefix=f'total -> ')
    ic(totals)

    
