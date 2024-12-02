# Updates the Salaries table
import pandas as pd;

# NOTE: This data has not been updated since 2016
# I made this script in the off chance we need it later

def updateSalaries(cursor):
    print("Adding new Salaries data...")

    data = pd.read_csv("Update_Assets/csvFiles/Salaries.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    salariesAdded = 0

    for row in data.iloc:
        if (row["yearID"] < 2023):
            continue

        newBat = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['salary'] if pd.notnull(row['salary']) else None,
        ]

        sql = '''INSERT INTO salaries (playerID, yearId, teamID, salary)
                VALUES(%s,%s,%s,%s);'''
        exe = cursor.execute(sql, newBat)
        salariesAdded += exe

    print("{} new rows of Salaries data added!".format(salariesAdded))