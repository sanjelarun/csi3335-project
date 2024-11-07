# Updates the Appearances table
import pandas as pd;

def updateAppearances(cursor):
    print("Adding new appearances data...")

    data = pd.read_csv("csvFiles/Appearances.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    appearancesAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023):
            continue
        newAppearance = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['G_all'] if pd.notnull(row['G_all']) else None,
            row['GS'] if pd.notnull(row['GS']) else None,
            row['G_batting'] if pd.notnull(row['G_batting']) else None,
            row['G_defense'] if pd.notnull(row['G_defense']) else None,
            row['G_p'] if pd.notnull(row['G_p']) else None,
            row['G_c'] if pd.notnull(row['G_c']) else None,
            row['G_1b'] if pd.notnull(row['G_1b']) else None,
            row['G_2b'] if pd.notnull(row['G_2b']) else None,
            row['G_3b'] if pd.notnull(row['G_3b']) else None,
            row['G_ss'] if pd.notnull(row['G_ss']) else None,
            row['G_lf'] if pd.notnull(row['G_lf']) else None,
            row['G_cf'] if pd.notnull(row['G_cf']) else None,
            row['G_rf'] if pd.notnull(row['G_rf']) else None,
            row['G_of'] if pd.notnull(row['G_of']) else None,
            row['G_dh'] if pd.notnull(row['G_dh']) else None,
            row['G_ph'] if pd.notnull(row['G_ph']) else None,
            row['G_pr'] if pd.notnull(row['G_pr']) else None,
        ]
        sql = '''INSERT INTO appearances 
                (playerID,yearID,teamID,G_all,GS,G_batting,G_defense,G_p,G_c,G_1b,G_2b,G_3b,G_ss,G_lf,G_cf,G_rf,G_of,G_dh,G_ph,G_pr)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        exe = cursor.execute(sql, newAppearance)
        appearancesAdded += exe

    print("{} rows of appearances data added!".format(appearancesAdded))
