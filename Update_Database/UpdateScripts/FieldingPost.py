# Updates the FieldingPost table
import pandas as pd;

def updateFieldingPost(cursor):
    print("Adding new FieldingPost data...")

    data=pd.read_csv("csvFiles/FieldingPost.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    fPostAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023): 
            continue

        newFPost = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['round'],
            row['POS'],
            row["G"],
            row["GS"],
            row["InnOuts"],
            row["PO"],
            row["A"],
            row["E"],
            row["DP"],
            row["TP"],
            row["PB"] if pd.notnull(row['PB']) else None,
        ]
        
        sql = '''INSERT INTO fieldingpost (playerID,yearId,teamID,round,position,f_G,f_GS,f_InnOuts,f_PO,f_A,f_E,f_DP,f_TP,f_PB)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        exe = cursor.execute(sql,newFPost)
        fPostAdded += exe
    
    print("Complete: {} new rows of FieldingPost data added!".format(fPostAdded))