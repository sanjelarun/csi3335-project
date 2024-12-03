# Updates the Teams table
import pandas as pd

def updateTeams(cursor):
    print("Adding new teams data...")

    data = pd.read_csv("Update_Assets/csvFiles/Teams.csv", na_values=['',' '])
    data = data.where(pd.notnull(data),None)

    teams_added = 0

    for row in data.iloc:
        if row["yearID"] < 2023:
            continue

        new_team = [
            row['yearID'],
            row['lgID'],
            row['teamID'],
            row['franchID'],
            row['divID'],
            row['Rank'],
            row['G'],
            row['Ghome'],
            row['W'],
            row['L'],
            row['DivWin'],
            row['WCWin'],
            row['LgWin'],
            row['WSWin'],
            row['R'],
            row['AB'],
            row['H'],
            row['2B'],
            row['3B'],
            row['HR'],
            row['BB'],
            row['SO'],
            row['SB'],
            row['CS'],
            row['HBP'],
            row['SF'],
            row['RA'],
            row['ER'],
            row['ERA'],
            row['CG'],
            row['SHO'],
            row['SV'],
            row['IPouts'],
            row['HA'],
            row['HRA'],
            row['BBA'],
            row['SOA'],
            row['E'],
            row['DP'],
            row['FP'],
            row['name'],
            row['park'],
            row['attendance'],
            row['BPF'],
            row['PPF'],
        ]

        sql = '''INSERT INTO teams (yearID,lgID,teamID,franchID,divID,team_rank,team_G,team_G_home,team_W,team_L,DivWin,WCWin,LgWin,WSWin,team_R,team_AB,team_H,team_2B,team_3B,team_HR,team_BB,team_SO,team_SB,team_CS,team_HBP,team_SF,team_RA,team_ER,team_ERA,team_CG,team_SHO,team_SV,team_IPouts,team_HA,team_HRA,team_BBA,team_SOA,team_E,team_DP,team_FP,team_name,park_name,team_attendance,team_BPF,team_PPF) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,new_team)
        teams_added += exe

    print("{} new Teams added.".format(teams_added))