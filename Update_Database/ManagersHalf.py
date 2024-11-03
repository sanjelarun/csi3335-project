# Updates the Managers (half) table
import pandas as pd;

def updateManagersHalf(cursor):
    print("Updating Managers Half data...")

    data = pd.read_csv("csvFiles/ManagersHalf.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    managersHalfAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023):
            continue
        newManagerHalf = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['inseason'],
            row['G'] if pd.notnull(row['G']) else None,
            row['W'] if pd.notnull(row['W']) else None,
            row['L'] if pd.notnull(row['L']) else None,
            row['rank'] if pd.notnull(row['rank']) else None,
            row['half'] if pd.notnull(row['half']) else None,
        ]
        sql = '''UPDATE managers
                SET playerID=%s, yearID=%s, teamID=%s, inSeason=%s, manager_G=%s, manager_W=%s, manager_L=%s, teamRank=%s, half=%s
                WHERE playerID=VALUES(playerID) AND yearID=VALUES(yearID) AND teamID=VALUES(teamID)'''
        exe = cursor.execute(sql, newManagerHalf)
        managersHalfAdded += exe

    print("{} rows of managers have been updated!".format(managersHalfAdded))
