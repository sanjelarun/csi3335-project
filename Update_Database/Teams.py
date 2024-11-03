# Updates the Teams table
import pandas as pd;

def updateTeams:
    print("Adding new teams data...")

    data = pd.read_csv("csvFiles/Teams.csv", na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    teamsAdded = 0

    for row in data.iloc:
        if(row["yearID"] < 2023):
            continue
        
        newTeam = [
            row['teamID'],
            row['yearID'],
            row['lgID'],
            row['divID'],
            row['franchID'],
            row['team_name'],
            row['team_G'],
            row['team_G_home'],
            row['team_W'],
            row['team_L'],
            row['DivWin'],
            row['WCWin'],
            row['LgWin'],
            row['WSWin'],
            row['team_R'],
            row['team_AB'],
            row['team_H'],
            row['team_2B'],
            row['team_3B'],
            row['team_HR'],
            row['team_BB'],
            row['team_SO'],
            row['team_SB'],
            row['team_CS'],
            row['team_HBP'],
            row['team_SF'],
            row['team_RA'],
            row['team_ER'],
            row['team_ERA'],
            row['team_CG'],
            row['team_SHO'],
            row['team_SV'],
            row['team_IPouts'],
            row['team_HA'],
            row['team_HRA'],
            row['team_BBA'],
            row['team_SOA'],
            row['team_E'],
            row['team_DP'],
            row['team_FP'],
            row['park_name'],
            row['team_attendance'],
            row['team_BPF'],
            row['team_PPF'],
            row['team_projW'],
            row['team_projL'],
        ]

        sql = '''INSERT INTO teams (teamID,yearID,lgID,divID,franchID,team_name,team_G,team_G_home,team_W,team_L,DivWin,WCWin,LgWin,WSWin,team_R,team_AB,team_H,team_2B,team_3B,team_HR,team_BB,team_SO,team_SB,team_CS,team_HBP,team_SF,team_RA,team_ER,team_ERA,team_CG,team_SHO,team_SV,team_IPouts,team_HA,team_HRA,team_BBA,team_SOA,team_E,team_DP,team_FP,park_name,team_attendance,team_BPF,team_PPF,team_projW,team_projL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newTeam)
        teamsAdded += exe
