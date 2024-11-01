# Updates the Batting table
import pandas as pd;

def updateFieldingOFSplit(cursor):
    print("Adding new fielding OF Split data...")

    data=pd.read_csv("csvFiles/FieldingOFsplit.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    fieldingSplitAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023): 
            continue

        newFielding=[
            row["playerID"],
            row["yearID"],
            row["teamID"],
            row["stint"],
            row["POS"],
            row["G"],
            row["GS"],
            row["InnOuts"],
            row["PO"],
            row["A"],
            row["E"],
            row["DP"],
        ]
        
        sql = '''INSERT INTO fielding (playerID, yearID, teamID, stint, position, f_G, f_GS, f_InnOuts, f_PO, f_A, f_E, f_DP)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newFielding)
        fieldingSplitAdded += exe
    
    print("Complete: {} new rows of fielding OF split data added to fielding!".format(fieldingSplitAdded))