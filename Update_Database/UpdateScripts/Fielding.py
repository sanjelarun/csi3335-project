# Updates the Fielding table
import pandas as pd;


def updateFielding(cursor):
    print("Adding new fielding data...")

    data = pd.read_csv("csvFiles/Fielding.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    fieldingAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023):
            continue
        newField = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['stint'],
            row['POS'] if pd.notnull(row['POS']) else None,
            row['G'] if pd.notnull(row['G']) else None,
            row['GS'] if pd.notnull(row['GS']) else None,
            row['InnOuts'] if pd.notnull(row['InnOuts']) else None,
            row['PO'] if pd.notnull(row['PO']) else None,
            row['A'] if pd.notnull(row['A']) else None,
            row['E'] if pd.notnull(row['E']) else None,
            row['DP'] if pd.notnull(row['DP']) else None,
            row['PB'] if pd.notnull(row['PB']) else None,
            row['WP'] if pd.notnull(row['WP']) else None,
            row['SB'] if pd.notnull(row['SB']) else None,
            row['CS'] if pd.notnull(row['CS']) else None,
            row['ZR'] if pd.notnull(row['ZR']) else None,
        ]
        sql = '''INSERT INTO fielding 
                (playerID,yearID,teamID,stint,position,f_G,f_GS,f_InnOuts,f_PO,f_A,f_E,f_DP,f_PB,f_WP,f_SB,f_CS,f_ZR)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        exe = cursor.execute(sql, newField)
        fieldingAdded += exe

    print("{} rows of fielding data updated!".format(fieldingAdded))
