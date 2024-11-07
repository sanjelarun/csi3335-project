# Updates the Awards table from AwardsPlayers
import pandas as pd

def updateAwardsPlayers(cursor):
    print("Adding new awards data...")

    data = pd.read_csv("csvFiles/AwardsPlayers.csv",na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    awards_added = 0

    for row in data.iloc:
        if row["yearID"] < 2023:
            continue

        new_award = [
            row['playerID'],
            row['awardID'],
            row['yearID'],
            row['lgID'],
            row['tie'],
            row['notes'],
        ]

        sql = '''INSERT INTO awards (playerID,awardID,yearID,lgID,tie,notes) VALUES (%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,new_award)
        awards_added += exe

    print("{} new awards added".format(awards_added))
