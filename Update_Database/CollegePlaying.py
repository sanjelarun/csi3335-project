# Update the CollegePlaying table
import pandas as pd;

def updateCollegePlaying(cursor):
    print("Adding new collegeplaying data...")

    data = pd.read_csv("csvFiles/CollegePlaying.csv",na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    collegePlayingAdded = 0

    for row in data.iloc:
        if(row["yearID"] < 2023):
            continue

        newCollegePlay = [
            row['playerID'],
            row['schoolID'],
            row['yearID'],
        ]

        sql = '''INSERT INTO collegeplaying (playerID,schoolID,yearID) VALUES (%s,%s,%s);'''
        exe = cursor.execute(sql,newCollegePlay)
        collegePlayingAdded += exe
