import sqlalchemy
from sqlalchemy.sql import text
from app import csi3335

def getTeamInfo(teamID: str, yearID: int) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)
    with engine.connect() as con:
        print(teamID)
        print(yearID)
        sqlQuery = text("SELECT teamID, team_name, team_rank, team_W, team_L, team_R, team_H, team_HR, team_BB, team_SO FROM teams WHERE teamID = :team_ID AND yearID = :year_ID")
        rs = con.execute(sqlQuery, {"team_ID": teamID, "year_ID": yearID})
        for row in rs:
            line: dict[str, str] = {}
            line["teamID"] = row[0]
            line["team_name"] = row[1]
            line["team_rank"] = str(row[2])
            line["team_W"] = str(row[3])
            line["team_L"] = str(row[4])
            line["team_R"] = str(row[5])
            line["team_H"] = str(row[6])
            line["team_HR"] = str(row[7])
            line["team_BB"] = str(row[8])
            line["team_SO"] = str(row[9])
            output.append(line)
    return output


def getBattingInfoByTeamIDandYearID(teamID: str, yearID: int) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)
    with engine.connect() as con:
        sqlQuery = text("SELECT playerid, nameFirst, nameLast,yearID, b_G, b_AB, b_R, b_H, b_HR, b_RBI, teamID, position FROM batting JOIN people USING(playerid) NATURAL JOIN fielding WHERE teamID = :team_ID AND yearID = :year_ID ORDER BY nameLast DESC, stint DESC")
        rs = con.execute(sqlQuery, {"team_ID": teamID, "year_ID": yearID})

        for row in rs:
            line: dict[str, str] = {}
            line["playerid"] = row[0]
            line["nameFirst"] = str(row[1])
            line["nameLast"] = str(row[2])
            line["b_G"] = str(row[3])
            line["b_AB"] = row[5]
            line["b_R"] = row[6]
            line["b_H"] = row[7]
            line["b_HR"] = row[8]
            line["b_RBI"] = row[9]
            line["teamID"] = row[10]
            line["position"] = str(row[11])
            output.append(line)

    return output

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
            line["yearID"] = row[2]
            line["b_G"] = row[3]
            line["b_AB"] = row[4]
            line["b_R"] = row[5]
            line["b_H"] = row[6]
            line["b_HR"] = row[7]
            line["b_RBI"] = row[8]
            line["teamID"] = row[9]
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


