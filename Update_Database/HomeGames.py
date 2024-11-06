# Update the HomeGames table
import pandas as pd;

def updatingHomeGames(cursor):
    print("Adding new homegames data...")

    data = pd.read_cdv("csvFiles/HomeGames.csv",na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    homeGameAdded = 0

    for row in data.iloc:
        if(row["yearID"] < 2023):
            continue:

        newHomeGame = [
            row['teamID'],
            row['parkID'],
            row['yearID'],
            row['firstGame'],
            row['lastGame'],
            row['games'],
            row['openings'],
            row['attendance'],
        ]

        sql = '''INSERT INTO homegames (teamID,parkID,yearID,firstGame,lastGame,games,openings,attendance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newHomeGame)
        homeGameAdded += exe
