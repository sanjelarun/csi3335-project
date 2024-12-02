# Updates the PitchingPost table
import pandas as pd;

def updatePitchingPost(cursor):
    print("Adding new pitching post data...")

    data = pd.read_csv("Update_Assets/csvFiles/PitchingPost.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    pitchingPostsAdded = 0

    for row in data.iloc:
        if(row["yearID"]<2023):
            continue
        newPitchPost = [
            row['playerID'],
            row['yearID'],
            row['teamID'],
            row['round'],
            row['W'] if pd.notnull(row['W']) else None,
            row['L'] if pd.notnull(row['L']) else None,
            row['G'] if pd.notnull(row['G']) else None,
            row['GS'] if pd.notnull(row['GS']) else None,
            row['CG'] if pd.notnull(row['CG']) else None,
            row['SHO'] if pd.notnull(row['SHO']) else None,
            row['SV'] if pd.notnull(row['SV']) else None,
            row['IPouts'] if pd.notnull(row['IPouts']) else None,
            row['H'] if pd.notnull(row['H']) else None,
            row['ER'] if pd.notnull(row['ER']) else None,
            row['HR'] if pd.notnull(row['HR']) else None,
            row['BB'] if pd.notnull(row['BB']) else None,
            row['SO'] if pd.notnull(row['SO']) else None,
            row['BAOpp'] if pd.notnull(row['BAOpp']) else None,
            row['ERA'] if pd.notnull(row['ERA']) else None,
            row['IBB'] if pd.notnull(row['IBB']) else None,
            row['WP'] if pd.notnull(row['WP']) else None,
            row['HBP'] if pd.notnull(row['HBP']) else None,
            row['BK'] if pd.notnull(row['BK']) else None,
            row['BFP'] if pd.notnull(row['BFP']) else None,
            row['GF'] if pd.notnull(row['GF']) else None,
            row['R'] if pd.notnull(row['R']) else None,
            row['SH'] if pd.notnull(row['SH']) else None,
            row['SF'] if pd.notnull(row['SF']) else None,
            row['GIDP'] if pd.notnull(row['GIDP']) else None,
        ]
        sql = '''INSERT INTO pitchingpost 
                (playerID,yearID,teamID,round,p_W,p_L,p_G,p_GS,p_CG,p_SHO,p_SV,p_IPouts,p_H,p_ER,p_HR,p_BB,p_SO,p_BAOpp,p_ERA,p_IBB,p_WP,p_HBP,p_BK,p_BFP,p_GF,p_R,p_SH,p_SF,p_GIDP)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        exe = cursor.execute(sql, newPitchPost)
        pitchingPostsAdded += exe

    print("{} rows of pitchingpost data added!".format(pitchingPostsAdded))
