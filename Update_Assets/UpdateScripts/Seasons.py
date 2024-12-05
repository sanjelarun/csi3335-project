# Create a "seasons" table that stores stats about the season as a whole
import pandas as pd;

def createSeasons(cursor):
    print("Creating Season table...")

    sql="DROP TABLE IF EXISTS season"
    cursor.execute(sql)

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
            s_cFIP DOUBLE,
            s_Tms INT(12),
            s_NumBat INT(12),
            s_BatAge DOUBLE,
            s_R_G DOUBLE,
            s_G INT(12),
            s_PA INT(12),
            s_AB INT(12),
            s_R INT(12),
            s_H INT(12),
            s_1B INT(12),
            s_2B INT(12),
            s_3B INT(12),
            s_HR INT(12),
            s_RBI INT(12),
            s_SB INT(12),
            s_CS INT(12),
            s_BB INT(12),
            s_SO INT(12),
            s_BA DOUBLE,
            s_OBP DOUBLE,
            s_SLG DOUBLE,
            s_OPS DOUBLE,
            s_TB INT(12),
            s_GDP INT(12),
            s_HBP INT(12),
            s_SH INT(12),
            s_SF INT(12),
            s_IBB INT(12),
            s_BIP INT(12)
        );
        '''
    cursor.execute(sql)


    data = pd.read_csv("Update_Assets/csvFiles/Seasons.csv", na_values=['', ' ', 'nan', '--'])
    #data = data.where(pd.notnull(data), None)
    data = data.fillna(0)

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
            row["Tms"],
            row["#Bat"],
            row["BatAge"],
            row["R/G"],
            row["G"],
            row["PA"],
            row["AB"],
            row["R"],
            row["H"],
            row["1B"],
            row["2B"],
            row["3B"],
            row["HR"],
            row["RBI"],
            row["SB"],
            row["CS"],
            row["BB"],
            row["SO"],
            row["BA"],
            row["OBP"],
            row["SLG"],
            row["OPS"],
            row["TB"],
            row["GDP"],
            row["HBP"],
            row["SH"],
            row["SF"] or 0,
            row["IBB"],
            row["BIP"],
        ]
        sql = '''INSERT INTO season (yearID, s_wOBA, s_wOBAScale, s_wBB, s_wHBP, s_w1B, s_w2B, s_w3B, s_wHR, s_runSB, s_runCS, s_R_PA, s_R_W, s_cFIP,s_Tms, s_NumBat, s_BatAge, s_R_G, s_G, s_PA, s_AB, s_R, s_H, s_1B, s_2B, s_3B, s_HR, s_RBI, s_SB, s_CS, s_BB, s_SO, s_BA, s_OBP, s_SLG, s_OPS, s_TB, s_GDP, s_HBP, s_SH, s_SF, s_IBB, s_BIP)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        exe = cursor.execute(sql, newSeason)
        seasonsAdded += exe

    print("{} rows of seasons have been added!".format(seasonsAdded))
