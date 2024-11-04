# Update the CollegePlaying table
import pandas as pd

def update_college_playing(cursor):
    print("Adding new collegeplaying data...")

    data = pd.read_csv("csvFiles/CollegePlaying.csv",na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    college_playing_added = 0

    for row in data.iloc:
        if row["yearID"] < 2023:
            continue

        new_college_play = [
            row['playerID'],
            row['schoolID'],
            row['yearID'],
        ]

        sql = '''INSERT INTO collegeplaying (playerID,schoolID,yearID) VALUES (%s,%s,%s);'''
        exe = cursor.execute(sql,new_college_play)
        college_playing_added += exe
    print("{} new CollegePlaying data added.".format(college_playing_added))