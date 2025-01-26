from numpy import prod
import aoc_utils
from pathlib import Path

day = int(Path(__file__).name.split('_')[1])
input_list = aoc_utils.get_day_input(day)



C = {
    "red": 12,
    "green": 13,
    "blue": 14
}

def getC(game: str) -> dict:
    # game format is "3 green, 8 red, 1 blue"
    # output is {"red": 8, "green": 3, "blue": 1}
    res = {}
    for color in game.split(", "):
        res[color.split(" ")[1]] = int(color.split(" ")[0])
    
    # if a color is not in the game, it has 0 records and is always possible
    return res

def fewer(games: list)-> dict:
    res = {
        "red" : 0,
        "green" :0,
        "blue" :0
    }
    for game in games:
        for color in C.keys():
            res[color] = max(game.get(color, 0), res[color])
    return res


total = 0
for line in input_list:
    game_id = line.split(":")[0].replace("Game ", "")
    games = line.split(": ")[1].split(";")
    feaseble_game_id = True
    gamed_id_games = list()
    for game in games:
        # sanitize game
        # sometimes can start with a space
        if game[0] == " ":
            game = game[1:]
        gamed_id_games.append(getC(game))
        
    Cf = fewer(gamed_id_games)
    
    value = prod([v for v in Cf.values() ])
    total += value

print(total)

