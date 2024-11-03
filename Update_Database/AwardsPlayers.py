# Updates the Awards table from AwardsPlayers
import pandas as pd;

def updateAwards(cursor):
    print("Adding new awards data...")

    data = pd.read_csv("csvFiles/AwardsPlayers.csv",na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    awardsAdded = 0

    for row in data.iloc:
        if(row["yearID"] < 2023:
            continue

        newAward = [
            row['awardID'],
            row['yearID'],
            row['playerID'],
            row['lgID'],
            row['tie'],
            row['notes'],
        ]

        sql = '''INSERT INTO awards (awardID,yearID,playerID,lgID,tie,notes) VALUES (%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newAware)
        awardsAdded += exe
