from pathlib import Path
import requests 
from bs4 import BeautifulSoup
from markdownify import markdownify as md

class AOC:
    def __init__(self, year):
        self.year = year
        self.base_year_path = Path(__file__).parent.parent / Path(str(year))
        
    def get_prose(self, day: int):
        url: str = f"https://adventofcode.com/{self.year}/day/{day}"
        file_path = self.base_year_path / Path(f"inputs/day_{day:0>2}/instructions.md")
        if file_path.exists():
            return
        response = requests.get(url)
        if response.ok:
            html_content = response.text
        else:
            print("Requests fallita")
            return
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find('article', class_='day-desc')

        if article:
            # Estrae il testo all'interno dell'articolo
            content = md(article.decode_contents())
            file_path.write_text(content)
        else:
            print("Non è stato trovato un articolo con classe 'day-desc'.")

        
    
    def get_input(self, day: int, input: int) -> str:
        # return the file in a unic string with`\n` as separator
        self.get_prose(day)
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
    