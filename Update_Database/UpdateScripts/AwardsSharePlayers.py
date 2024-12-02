# Updates the AwardsShare table
import pandas as pd;

def updateAwardsSharePlayers(cursor):
    print("Adding new players awards data...")

    data=pd.read_csv("csvFiles/AwardsSharePlayers.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    playerAwardsAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023): 
            continue

        newAward=[
            row["playerID"],
            row["awardID"],
            row["yearID"],
            row["lgID"],
            row["pointsWon"],
            row["pointsMax"],
            row["votesFirst"]
        ]
        
        sql = '''INSERT INTO awardsshare (playerID,awardID,yearID,lgID,pointsWon,pointsMax,votesFirst )
                VALUES(%s,%s,%s,%s,%s,%s,%s );'''
        exe = cursor.execute(sql,newAward)
        playerAwardsAdded += exe
    
    print("Complete: {} new rows of player awards data added to awardsshare!".format(playerAwardsAdded))