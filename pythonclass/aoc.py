from pathlib import Path

class AOC:
    def __init__(self, year):
        self.year = year
        self.base_year_path = Path(__file__).parent.parent / Path(str(year))
    
    def get_input(self, day: int, input: int) -> str:
        # return the file in a unic string with`\n` as separator
        file_path = self.base_year_path / Path(f"inputs/day_{day:0>2}/input_{input}.txt")
        if file_path.exists():
            return file_path.read_text()
        else:
            from aocd import get_data
            data = get_data(day=day, year=self.year)
            file_path.write_text(data)
            return data
    
    def get_day_folder_path(self, day: int) -> Path:
        day_path = self.base_year_path / Path(f"inputs/day_{day:0>2}/")
        return day_path
        


if __name__ == "__main__":
    #test with year 2015
    aoc = AOC(2015)
    print(aoc.get_input(1, 1))
    