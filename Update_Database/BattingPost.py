# Updates the battingpost table
import pandas as pd

def update_batting_post(cursor):
    print("Adding new battingpost data...")

    data = pd.read_csv("csvFiles/BattingPost.csv",na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    batting_post_added = 0

    for row in data.iloc:
        if row["yearID"] < 2023:
            continue

        new_bat_post = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['round'],
            row['b_G'],
            row['b_AB'],
            row['b_R'],
            row['b_H'],
            row['b_2B'],
            row['b_3B'],
            row['b_HR'],
            row['b_RBI'],
            row['b_SB'],
            row['b_CS'],
            row['b_BB'],
            row['b_SO'],
            row['b_IBB'],
            row['b_HBP'],
            row['b_SH'],
            row['b_SF'],
            row['b_GIDP'],
        ]

        sql = '''INSERT INTO battingpost (playerID,yearID,teamID,round,b_G,b_AB,b_R,b_H,b_2B,b_3B,b_HR,b_RBI,b_SB,b_CS,b_BB,b_SO,b_IBB,b_HBP,b_SH,b_SF,b_GIDP) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''

        exe = cursor.execute(sql,new_bat_post)
        batting_post_added += exe
