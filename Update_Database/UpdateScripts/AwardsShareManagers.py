# Updates the Awards Share (managers) table
import pandas as pd;

def updateAwardsShareManagers(cursor):
    print("Updating AwardsShare managers data...")

    data = pd.read_csv("csvFiles/AwardsShareManagers.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    managerAwardsAdded = 0

    for row in data.iloc:
        if(row['yearID']<2023):
            continue
        newManagerHalf = [
            row['awardID'],
            row['yearID'],
            row['playerID'],
            row['lgID'],
            row['pointsWon'] if pd.notnull(row['pointsWon']) else None,
            row['pointsMax'] if pd.notnull(row['pointsMax']) else None,
            row['votesFirst'] if pd.notnull(row['votesFirst']) else None,
        ]
        sql = '''INSERT INTO awardsshare
                (awardID, yearID, playerID, lgID, pointsWon, pointsMax, votesFirst)
                VALUES(%s, %s, %s, %s, %s, %s, %s);'''
        exe = cursor.execute(sql, newManagerHalf)
        managerAwardsAdded += exe

    print("{} rows of AwardsShare managers have been updated!".format(managerAwardsAdded))
