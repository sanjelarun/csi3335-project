import sqlalchemy
from sqlalchemy.sql import text
from app import csi3335





def getPlayerBattingInfo(playerID: str) -> list[dict[str,str]]:
    output : list[dict[str,str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)
    with engine.connect() as con:
        sqlQuery = text("SELECT nameFirst, nameLast,yearID, b_G, b_AB, b_R, b_H, b_HR, b_RBI, teamID"
                        " FROM batting join PEOPLE USING(playerID) WHERE playerID = :player_ID ORDER BY yearID DESC, stint DESC")
        rs = con.execute(sqlQuery, {"player_ID" : playerID})

        for row in rs:
            line :dict[str,str] = {}
            line["name"] = row[0] + ' ' + row[1]
            line["yearId"] = row[2]
            line["b_G"] = row[3]
            line["b_AB"] = row[4]
            line["b_R"] = row[5]
            line["b_H"] = row[6]
            line["b_HR"] = row[7]
            line["b_RBI"] = row[8]
            line["teamId"] = row[9]
            output.append(line)

        return output

def getPlayerPitchingInfo(playerID: str) -> list[dict[str,str]]:
    output: list[dict[str,str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)

    with engine.connect() as con:
        sqlQuery = text("SELECT nameFirst, nameLast,yearID, teamID, p_W, p_L, p_G, p_GS, p_H, p_HR, p_SV, p_SO"
                        " FROM pitching join PEOPLE USING(playerID) WHERE playerID = :player_ID ORDER BY yearID DESC, stint DESC")
        rs = con.execute(sqlQuery, {"player_ID" : playerID})

        for row in rs:
            line :dict[str,str] = {}
            line["name"] = row[0] + ' ' + row[1]
            line["yearID"] = row[2]
            line["teamID"] = row[3]
            line["p_W"] = row[4]
            line["p_L"] = row[5]
            line["p_G"] = row[6]
            line["p_GS"] = row[7]
            line["p_H"] = row[8]
            line["p_HR"] = row[9]
            line["p_SV"] = row[10]
            line["p_SO"] = row[11]
            output.append(line)
        return output


def getPlayerFieldingInfo(playerID: str) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (
    csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)

    with engine.connect() as con:
        sqlQuery = text("SELECT nameFirst, nameLast,yearID, teamID, position, f_G, f_GS, f_InnOuts, f_PO, f_A, f_E, f_DP"
                        " FROM fielding join PEOPLE USING(playerID) WHERE playerID = :player_ID ORDER BY yearID DESC, stint DESC")
        rs = con.execute(sqlQuery, {"player_ID": playerID})

        for row in rs:
            line: dict[str, str] = {}
            line["name"] = row[0] + ' ' + row[1]
            line["yearID"] = row[2]
            line["teamID"] = row[3]
            line["position"] = row[4]
            line["f_G"] = row[5]
            line["f_Gs"] = row[6]
            line["f_InnOuts"] = row[7]
            line["f_PO"] = row[8]
            line["f_A"] = row[9]
            line["f_E"] = row[10]
            line["f_DP"] = row[11]

            output.append(line)
        return output


