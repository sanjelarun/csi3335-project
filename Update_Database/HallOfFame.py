# Updates the Batting table
import pandas as pd;

def updateHallOfFame(cursor):
    print("Adding new Hall Of Fame data...")

    data=pd.read_csv("csvFiles/HallOfFame.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    hallOfFameAdded = 0

    for row in data.iloc:
        if(row["yearid"]<2023): 
            continue

        newHallOfFame= [
            row["playerID"],
            row["yearid"],
            row["votedBy"],
            row["ballots"],
            row["needed"],
            row["votes"] if pd.notnull(row['votes']) else None,
            row["inducted"],
            row["category"],
            row["needed_note"],
        ]
        
        sql = '''INSERT INTO halloffame (playerID,yearID,votedBy,ballots,needed,votes,inducted,category,note)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newHallOfFame)
        hallOfFameAdded += exe
    
    print("Complete: {} new rows of Hall Of Fame data!".format(hallOfFameAdded))