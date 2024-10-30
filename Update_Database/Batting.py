# Updates the Batting table
import pandas as pd;

def updateBatting(cursor):
    print("Adding new batting data...")

    data=pd.read_csv("csvFiles/Batting.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    battingAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023): 
            continue

        newBat = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['stint'],
            row["G"],
            row["AB"],
            row["R"],
            row["H"],
            row["2B"],
            row["3B"],
            row["HR"],
            row["RBI"],
            row["SB"],
            row["CS"],
            row["BB"],
            row["SO"],
            row["IBB"],
            row["HBP"],
            row["SH"],
            row["SF"],
            row["GIDP"],
        ]
        
        sql = '''INSERT INTO batting (playerID,yearId,teamID,stint,b_G,b_AB,b_R,b_H,b_2B,b_3B,b_HR,b_RBI,b_SB,b_CS,b_BB,b_SO,b_IBB,b_HBP,b_SH,b_SF,b_GIDP)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newBat)
        battingAdded += exe
    
    print("{} new rows of batting data added!".format(battingAdded))