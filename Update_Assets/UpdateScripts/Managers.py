# Updates the Managers table
import pandas as pd;

def updateManagers(cursor):
    print("Adding new managers...")

    data=pd.read_csv("Update_Assets/csvFiles/Managers.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    managersAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023): 
            continue

        newManager = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['inseason'],
            row['G'],
            row['W'],
            row['L'],
            row['rank'],
            row['plyrMgr']
        ]
        
        sql = '''INSERT INTO managers (playerID, yearID, teamID, inSeason, manager_G, manager_W, manager_L, teamRank, plyrMgr)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        #execute html and extract needed info from result set
        exe = cursor.execute(sql,newManager)
        managersAdded += exe
    
    print("Complete: {} new Managers added!".format(managersAdded))