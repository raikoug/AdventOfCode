from numpy import prod

races = \
[
    {  
        "time": 62,       
        "distance": 553
    },
    {
        "time": 64,
        "distance": 1010
    },
    {
        "time": 91,
        "distance": 1473
    },
    {
        "time": 90,
        "distance": 1074
    }]

solutions: list = []
for race in races:
    tmp: list = []
    time = race["time"]
    distance = race["distance"]
    for x in range(1, time+1):
        if (time-x)*x > distance:
            tmp.append(x)
    solutions.append(tmp)

print(prod([len(s) for s in solutions]))

## NO... done in excel XD