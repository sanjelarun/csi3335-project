# Updates the batting post table
import pandas as pd

def update_batting_post(cursor):
    print("Adding new batting post data...")

    data = pd.read_csv("csvFiles/BattingPost.csv",na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    batting_post_added = 0

    for row in data.iloc:
        if row["yearID"] < 2023:
            continue

        new_bat_post = [
            row['yearID'],
            row['round'],
            row['playerID'],
            row['teamID'],
            row['G'],
            row['AB'],
            row['R'],
            row['H'],
            row['2B'],
            row['3B'],
            row['HR'],
            row['RBI'],
            row['SB'],
            row['CS'],
            row['BB'],
            row['SO'],
            row['IBB'],
            row['HBP'],
            row['SH'],
            row['SF'],
            row['GIDP'],
        ]

        sql = '''INSERT INTO battingpost (yearID,round,playerID,teamID,b_G,b_AB,b_R,b_H,b_2B,b_3B,b_HR,b_RBI,b_SB,b_CS,b_BB,b_SO,b_IBB,b_HBP,b_SH,b_SF,b_GIDP) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''

        exe = cursor.execute(sql,new_bat_post)
        batting_post_added += exe
