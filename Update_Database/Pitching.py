# Updates the Pitching table
import Pandas as pd;

def updatePitching:
    print("Adding new pitching data...")
	
    data = pd.read_csv("csvFiles/Pitching.csv",na_values=['',' '])
    data = data.where(pd.notnull(data), None)

    pitchingAdded = 0

    for row in data.iloc:
        if(row["yearID"] < 2023):
            continue

        newPit = [
            row['pitching_ID'],
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['stint'],
            row['p_W'],
            row['p_L],
            row['p_G'],
            row['p_GS'],
            row['p_CG'],
            row['p_SHO'],
            row['p_SV'],
            row['p_IPOuts'],
            row['p_H'],
            row['p_ER'],
            row[p_HR'],
            row[p_BB'],
            row[p_SO'],
            row['p_BAOpp'],
            row['p_ERA'],
            row['p_IBB'],
            row['p_WP'],
            row['p_HBP'],
            row['p_BK'],
            row['p_BFP'],
            row['p_GF'],
            row['p_R'],
            row['p_SH'],
            row['p_SF'],
            row['p_GIDP'],
        ]

        sql = '''INSERT INTO pitching (pitchingID,playerID,yearID,teamID,stint,p_W,p_L,p_G,p_GS,p_CG,p_SHO,p_SV,p_IPOuts,p_H,p_ER,p_HR,p_BB,p_SO,p_BAOpp,p_ERA,p_IBB,p_WP,p_HBP,p_BK,p_BFP,p_GF,p_R,p_SH,p_SF,p_GIDP) VALUES(%s,%s,%s,,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        exe = cursor.execute(sql,newPit)
        pitchingAdded += exe
