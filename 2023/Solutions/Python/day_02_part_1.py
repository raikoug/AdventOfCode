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

def is_game_feasible(game: dict) -> bool:
    # game is feasible if the sum of the records is less than 15
    for color,value in C.items():
        if color not in game:
            pass
        else:
            if game[color] > value:
                return False
    return True


res = 0
for line in input_list:
    game_id = line.split(":")[0].replace("Game ", "")
    games = line.split(": ")[1].split(";")
    print(game_id)
    feaseble_game_id = True
    for game in games:
        # sanitize game
        # sometimes can start with a space
        if game[0] == " ":
            game = game[1:]
        dGame = getC(game)
        if not is_game_feasible(dGame):
            feaseble_game_id = False
            break
    if feaseble_game_id:
        res += int(game_id)

print(res)
    