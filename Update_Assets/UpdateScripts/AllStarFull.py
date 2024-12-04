# Updates the Batting table
import pandas as pd;

def updateAllStarFull(cursor):
    print("Adding new All Star Full data...")

    data=pd.read_csv("Update_Assets/csvFiles/AllstarFull.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    allStarAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2022): 
            continue

        newAllStar=[
            row["playerID"],
            row["lgID"],
            row["teamID"],
            row["yearID"],
            row["gameID"],
            row["GP"],
            row["startingPos"] if pd.notnull(row['startingPos']) else None,
        ]

        sql = '''INSERT INTO allstarfull (playerID,lgID,teamID,yearID,gameID,GP,startingPos)
                VALUES(%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newAllStar)
        allStarAdded += exe
    
    print("Complete: {} new rows of AllStarFull Data!".format(allStarAdded))