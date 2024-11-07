# Updates the Batting table
import pandas as pd;

def updateAwardsManagers(cursor):
    print("Adding new manager awards data...")

    data=pd.read_csv("csvFiles/AwardsManagers.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    managerAwardsAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023): 
            continue

        newAward=[
            row["playerID"],
            row["awardID"],
            row["yearID"],
            row["lgID"],
            row["tie"],
            row["notes"],
        ]
        
        sql = '''INSERT INTO awards (playerID,awardID,yearID,lgID,tie,notes )
                VALUES(%s,%s,%s,%s,%s,%s );'''
        exe = cursor.execute(sql,newAward)
        managerAwardsAdded += exe
    
    print("Complete: {} new rows of manager awards added to awards!".format(managerAwardsAdded))