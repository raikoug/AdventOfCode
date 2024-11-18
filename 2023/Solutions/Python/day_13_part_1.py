from icecream import ic

def get_column_as_string(m: list, col: int):
    """
        Get a column as a string
    """
    return "".join([row[col] for row in m])

def find_orizontal_mirror(F: list)-> int:
    """
        Find the orizontal mirror is any.
            return index of the row or 0 if not found
    """
    def is_mirror(r: int) -> bool:
        """
            Check if a mirror has been found, 
              this is triggered when a row (x) is equal to the preivous one (x-1)
              need to check if next row (x+1) is equal to the pre-previous (x-2) one and so on
              if this persist until the end of the matrix, then we have a mirror
              for example row 'r' triggered this, o we know that
                r == r-1
              we need to chek this couples:
                r+1 == r-2 (r[x+1] == r[x-2])
                r+2 == r-3 (r[x+2] == r[x-3])
                ...
                until either r-x == 0 or r+x == len(F)
        """
        for i in range(1, len(F)):
            if (r-i-1 < 0) or (r+i >= len(F)):
                return True
            
            if F[r+i] != F[r-i-1]:
                return False
        return True

    for i,row in enumerate(F):
        if (i == 0):
            continue
        if row == F[i-1]:
            ic(i, row)
            if is_mirror(i):
                return i
    return 0

def find_vertical_mirror(tf):
    pass

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    
    original_blocks = list()
    rotated_blocks = list()
    tmp_block = list()
    
    for line in tf:
        if line == '':
            # If I wanto to check horizontal, it's easy enough, this is a list of rows.
            #  to check columns, this is different, I should generate the columns each time I need them and crea
            #  a new funciton just for columns... I transpose the matrix 90 degree right and I can use the same
            #  function for horizontal and vertical
            rotated_block = [''.join(el) for el in (zip(*tmp_block[::-1]))]
            original_blocks.append(tmp_block)
            rotated_blocks.append(rotated_block)
            tmp_block = list()
            continue
        
        tmp_block.append(line)
    
    rotated_block = [''.join(el) for el in (zip(*tmp_block[::-1]))]
    original_blocks.append(tmp_block)
    rotated_blocks.append(rotated_block)
    #ic(len(original_blocks), len(rotated_blocks))
    #ic(original_blocks, rotated_blocks)

    mirrors_found = list()

    total = 0
    for i,block in enumerate(original_blocks):
        value = find_orizontal_mirror(block)*100
        if value:
            mirrors_found.append(i)
            total += value
    
    for i,block in enumerate(rotated_blocks):
        value = find_orizontal_mirror(block)
        if value:
            mirrors_found.append(i)
            total += value
    
    mirrors_found = list(set(mirrors_found))
    ic(len(mirrors_found))
    #ic(mirrors_found)
    ic(total)