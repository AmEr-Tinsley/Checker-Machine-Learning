import pandas as pd

mv = pd.read_csv('players.csv')

stats = {}
id=len(mv['ID'])
for i in range(id):
    M1 = mv['Black'][i]
    M2 = mv['White'][i]
    result = mv['Result'][i]
    if result == 1:
        if M1 in stats.keys():
            stats[M1][0] += 1
        else:
            stats[M1] = [1, 0, 0]
        if M2 in stats.keys():
            stats[M2][1] += 1
        else:
            stats[M2] = [0, 1, 0]
    elif result == 2:
        if M2 in stats.keys():
            stats[M2][0] += 1
        else:
            stats[M2] = [1, 0, 0]
        if M1 in stats.keys():
            stats[M1][1] += 1
        else:
            stats[M1] = [0, 1, 0]
    elif result == 0:
        if M1 in stats.keys():
            stats[M1][2] += 1
        else:
            stats[M1] = [0, 0, 1]
        if M2 in stats.keys():
            stats[M2][2] += 1
        else:
            stats[M2] = [0, 0, 1]
pd.DataFrame.from_dict(data=stats, orient='index').to_csv('stat_player.csv', header=False)
