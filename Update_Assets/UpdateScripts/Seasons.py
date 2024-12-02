# Create a "seasons" table that stores stats about the season as a whole
import pandas as pd;

def createSeasons(cursor):
    print("Creating Seasons table...")

    sql = '''
        CREATE TABLE IF NOT EXISTS season (
            season_ID INT(12) AUTO_INCREMENT PRIMARY KEY,
            yearID INT(6) NOT NULL,
            s_wOBA DOUBLE,
            s_wOBAScale DOUBLE,
            s_wBB DOUBLE,
            s_wHBP DOUBLE,
            s_w1B DOUBLE,
            s_w2B DOUBLE,
            s_w3B DOUBLE,
            s_wHR DOUBLE,
            s_runSB DOUBLE,
            s_runCS DOUBLE,
            s_R_PA DOUBLE,
            s_R_W DOUBLE,
            s_cFIP DOUBLE 
        );
        '''
    cursor.execute(sql)


    data = pd.read_csv("Update_Assets/csvFiles/Seasons.csv", na_values=['', ' '])
    data = data.where(pd.notnull(data), None)

    seasonsAdded = 0

    for row in data.iloc:
        newSeason = [
           row["Season"],
           row["wOBA"],
           row["wOBAScale"],
           row["wBB"],
           row["wHBP"],
           row["w1B"],
           row["w2B"],
           row["w3B"],
           row["wHR"],
           row["runSB"],
           row["runCS"],
           row["R/PA"],
           row["R/W"],
           row["cFIP"],
        ]
        sql = '''INSERT INTO season (yearID, s_wOBA, s_wOBAScale, s_wBB, s_wHBP, s_w1B, s_w2B, s_w3B, s_wHR, s_runSB, s_runCS, s_R_PA, s_R_W, s_cFIP)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        exe = cursor.execute(sql, newSeason)
        seasonsAdded += exe

    print("{} rows of seasons have been added!".format(seasonsAdded))
