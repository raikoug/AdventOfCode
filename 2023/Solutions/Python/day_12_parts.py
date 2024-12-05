from functools import cache
from icecream import ic



# old nonogram solution in my toolbox :D
@cache
def springs_finder(row, nums):
  next_part = nums[1:]
  springs = (f"{spr*'.'}{'#'*nums[0]}."
             for spr in range(len(row) - sum(nums) - len(next_part)))
  valid = (len(spr) for spr in springs
           if all(r in (c, '?') for r, c in zip(row, spr)))
  return sum(springs_finder(row[v:], next_part)
             for v in valid) if next_part else sum('#' not in row[v:]
                                                   for v in valid)

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    
    the_data = list()
    for line in tf:
        row, nums = line.split()
        nums = tuple(int(num) for num in nums.split(','))
        the_data.append((row, nums))
    #ic(the_data)
    #making data for part 2
    new_data = list()
    for data in the_data:
        #    ROW data[0] (str)
        # *5 to this part with '?' between
        # ".#" -> ".#?.#?.#?.#?.#"
        #    COLs data[1] (tuple)
        # *5 to this part with ',' between
        # (1) -> (1,1,1,1,1)
        new_data.append( ['?'.join([data[0]]*5),
                         data[1]*5] )

    #ic(new_data)
       

    total_1 = 0
    total_2 = 0
    for data1, data2 in zip(the_data, new_data):
        row = data1[0] + '.'
        sums = data1[1]
        total_1 += springs_finder(row, sums)
        row = data2[0] + '.'
        sums = data2[1]
        total_2 += springs_finder(row, sums)
       

    ic(total_1)
    ic(total_2)
