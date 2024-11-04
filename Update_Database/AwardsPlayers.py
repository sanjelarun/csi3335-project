# Updates the Awards table from AwardsPlayers
import pandas as pd

def update_awards(cursor):
    print("Adding new awards data...")

    data = pd.read_csv("csvFiles/AwardsPlayers.csv",na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    awards_added = 0

    for row in data.iloc:
        if row["yearID"] < 2023:
            continue

        new_award = [
            row['awardID'],
            row['yearID'],
            row['playerID'],
            row['lgID'],
            row['tie'],
            row['notes'],
        ]

        sql = '''INSERT INTO awards (awardID,yearID,playerID,lgID,tie,notes) VALUES (%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,new_award)
        awards_added += exe

    print("{} new awards added".format(awards_added))
