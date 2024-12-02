# Updates the Teams table
# Pretty sure this table is actually pointless all the info exists in the database lol
import pandas as pd;

def updateTeamsHalf(cursor):
    print("Adding new teams...")

    data=pd.read_csv("Update_Assets/csvFiles/TeamsHalf.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)
    
    teamsAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023): 
            continue

        newTeam = [
            row['yearID'],
            row['lgID'],
            row['teamID'],
            row['divID'],
            row['DivWin'],
            row['rank'],
            row['G'],
            row['W'],
            row['L']
        ]
        
        sql = '''INSERT INTO teams (yearID, lgID, teamID, DivWin, team_rank, team_G, team_W, team_L)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
        #execute html and extract needed info from result set
        exe = cursor.execute(sql,newTeam)
        teamsAdded += exe
    
    print("Complete: {} new Teams added!".format(teamsAdded))