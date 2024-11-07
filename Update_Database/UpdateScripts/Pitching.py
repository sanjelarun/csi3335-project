# Updates the Pitching table
import pandas as pd


def updatePitching(cursor):
    print("Adding new pitching data...")

    data = pd.read_csv("csvFiles/Pitching.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    pitching_added = 0

    for row in data.iloc:
        if row["yearID"] < 2023:
            continue

        new_pit = [
            row['playerID'],
            row['yearID'],
            row['stint'],
            row['teamID'],
            row['W'],
            row['L'],
            row['G'],
            row['GS'],
            row['CG'],
            row['SHO'],
            row['SV'],
            row['IPouts'],
            row['H'],
            row['ER'],
            row['HR'],
            row['BB'],
            row['SO'],
            row['BAOpp'],
            row['ERA'],
            row['IBB'],
            row['WP'],
            row['HBP'],
            row['BK'],
            row['BFP'],
            row['GF'],
            row['R'],
            row['SH'],
            row['SF'],
            row['GIDP'],
        ]

        sql = '''INSERT INTO pitching (playerID,yearID,stint,teamID,p_W,p_L,p_G,p_GS,p_CG,p_SHO,p_SV,p_IPOuts,p_H,p_ER,p_HR,p_BB,p_SO,p_BAOpp,p_ERA,p_IBB,p_WP,p_HBP,p_BK,p_BFP,p_GF,p_R,p_SH,p_SF,p_GIDP) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql, new_pit)
        pitching_added += exe
    print("{} new Pitching added!".format(pitching_added))
