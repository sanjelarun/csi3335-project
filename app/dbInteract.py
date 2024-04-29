import sqlalchemy
from sqlalchemy.sql import text
from app import csi3335


def getTeamInfo(teamID: str, yearID: int) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (
    csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)
    with engine.connect() as con:
        print(teamID)
        print(yearID)
        sqlQuery = text(
            "SELECT teamID, team_name, team_rank, team_W, team_L, team_R, team_H, team_HR, team_BB, team_SO, team_G, park_name, team_attendance, WCWin, LgWin, WSWin, franchID FROM teams WHERE teamID = :team_ID AND yearID = :year_ID")
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
            line["team_G"] = str(row[10])
            line["park_name"] = str(row[11])
            line["team_attendance"] = str(row[12])
            line["WCWin"] = str(row[13])
            line["LgWin"] = str(row[14])
            line["WSWin"] = str(row[15])
            line["franchID"] = str(row[16])
            output.append(line)
    return output


def getName(playerID: int) -> str:
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (
    csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)
    with engine.connect() as con:
        sqlQuery = text("SELECT nameFirst, nameLast FROM people WHERE playerID = :player_ID")
        rs = con.execute(sqlQuery, {"player_ID": playerID})
        player_name: tuple = rs.fetchone()
        if player_name:
            return f"{player_name[0]} {player_name[1]}"
        else:
            return "Player not found"


def getBattingInfoByTeamIDandYearID(teamID: str, yearID: int) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (
    csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)
    with engine.connect() as con:
        sqlQuery = text(
            "SELECT playerid, nameFirst, nameLast, yearID, b_G, b_AB, b_R, b_H, b_HR, b_RBI, teamID, position, b_BB, b_HBP, b_SF, b_2B, b_3B FROM batting JOIN people USING(playerid) NATURAL JOIN fielding WHERE teamID = :team_ID AND yearID = :year_ID ORDER BY nameLast ASC, stint DESC")
        rs = con.execute(sqlQuery, {"team_ID": teamID, "year_ID": yearID})

        for row in rs:
            line: dict[str, str] = {}
            line["playerid"] = row[0]
            line["nameFirst"] = str(row[1])
            line["nameLast"] = str(row[2])
            line["yearID"] = str(row[3])
            line["b_G"] = row[4]
            line["b_AB"] = row[5]
            line["b_R"] = row[6]
            line["b_H"] = row[7]
            line["b_HR"] = row[8]
            line["b_RBI"] = row[9]
            line["teamID"] = row[10]
            line["position"] = str(row[11])
            line["b_BB"] = row[12]
            line["b_HBP"] = row[13]
            line["b_SF"] = row[14]
            line["b_2B"] = row[15]
            line["b_3B"] = row[16]

            output.append(line)

    return output


def getPitchingInfoByTeamIDandYearID(teamID: str, yearID: int) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (
    csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)
    with engine.connect() as con:
        sqlQuery = text(
            "SELECT playerid, nameFirst, nameLast, yearID, teamID, p_W, p_L, p_G, p_GS, p_H, p_HR, p_SV, p_SO, p_ERA, p_BB, p_IPOuts "
            "FROM pitching JOIN people USING(playerid) NATURAL JOIN fielding "
            "WHERE teamID = :team_ID AND yearID = :year_ID ORDER BY nameLast ASC, stint DESC")

        rs = con.execute(sqlQuery, {"team_ID": teamID, "year_ID": yearID})

        for row in rs:
            line: dict[str, str] = {}
            line["playerid"] = row[0]
            line["nameFirst"] = str(row[1])
            line["nameLast"] = str(row[2])
            line["yearID"] = str(row[3])
            line["teamID"] = row[4]
            line["p_W"] = row[5]
            line["p_L"] = row[6]
            line["p_G"] = row[7]
            line["p_GS"] = row[8]
            line["p_H"] = row[9]
            line["p_HR"] = row[10]
            line["p_SV"] = row[11]
            line["p_SO"] = row[12]
            line["p_ERA"] = row[13]
            line["p_BB"] = row[14]
            line["p_IPOuts"] = row[15]

            # Calculate additional stats
            innings_pitched = int(row[15]) / 3  # p_IPOuts / 3
            whip = (int(row[14]) + int(row[9])) / innings_pitched  # (p_BB + p_H) / innings_pitched
            strikeouts_per_9 = (int(row[12]) / innings_pitched) * 9  # (p_SO / innings_pitched) * 9

            line["p_IP"] = f"{innings_pitched:.1f}"  # Format innings_pitched to 1 decimal place
            line["p_WHIP"] = f"{whip:.3f}"  # Format WHIP to 3 decimal places
            line["p_SO_per_9"] = f"{strikeouts_per_9:.1f}"  # Format strikeouts_per_9 to 1 decimal place

            output.append(line)

    return output


def getPlayerBattingInfo(playerID: str) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (
    csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)
    with engine.connect() as con:
        sqlQuery = text("SELECT nameFirst, nameLast,yearID, b_G, b_AB, b_R, b_H, b_HR, b_RBI, teamID"
                        " FROM batting join PEOPLE USING(playerID) WHERE playerID = :player_ID ORDER BY yearID DESC, stint DESC")
        rs = con.execute(sqlQuery, {"player_ID": playerID})

        for row in rs:
            line: dict[str, str] = {}
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


def getPlayerPitchingInfo(playerID: str) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s" % (
    csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]), echo=False)

    with engine.connect() as con:
        sqlQuery = text("SELECT nameFirst, nameLast,yearID, teamID, p_W, p_L, p_G, p_GS, p_H, p_HR, p_SV, p_SO"
                        " FROM pitching join PEOPLE USING(playerID) WHERE playerID = :player_ID ORDER BY yearID DESC, stint DESC")
        rs = con.execute(sqlQuery, {"player_ID": playerID})

        for row in rs:
            line: dict[str, str] = {}
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
        csi3335.mysql["user"], csi3335.mysql["password"], csi3335.mysql["location"], csi3335.mysql["database"]),
                                      echo=False)

    with engine.connect() as con:
        sqlQuery = text(
            "SELECT nameFirst, nameLast,yearID, teamID, position, f_G, f_GS, f_InnOuts, f_PO, f_A, f_E, f_DP"
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
