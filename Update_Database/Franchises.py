# Updates the Franchises table
import pandas as pd;


def updateFranchises(cursor):
    print("Adding new franchise data...")

    data = pd.read_csv("csvFiles/TeamsFranchises.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    franchAdded = 0

    for row in data.iloc:
        newFranch = [
            row['franchID'],
            row['franchName'],
            row['active'],
            row['NAassoc'] if pd.notnull(row['NAassoc']) else None,
        ]
        # Since year isn't tracked and duplicates aren't allowed,
        # Insert on new entries, update on existing ones.
        sql = '''INSERT IGNORE INTO franchises 
                    (franchID,franchName,active,NAassoc)
                VALUES(%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    franchName  = VALUES(franchName),
                    active      = VALUES(active),
                    NAassoc     = VALUES(NAassoc);
                '''
        exe = cursor.execute(sql, newFranch)
        franchAdded += exe

    print("{} rows of franchises data updated (0 is expected)!".format(franchAdded))
