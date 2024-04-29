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
            "SELECT team_name, team_W, team_L, team_R, team_HR, team_BB, "
            "team_SO, team_AB, team_H, team_2B, team_3B, team_HR, team_BB,"
            " team_SO, team_SB, team_CS, team_HBP, team_SF, team_RA,"
            " team_ER, team_ERA, team_CG, team_SHO, team_SV, team_IPouts, "
            "team_HA, team_HRA, team_BBA, team_SOA, team_E, team_DP, team_FP, "
            "team_attendance, team_BPF, team_PPF, team_projW, team_projL, team_rank, team_G, franchID,"
            "WSWin, Divwin, lgwin "
            "FROM teams WHERE teamID = :team_ID AND yearID = :year_ID")
        rs = con.execute(sqlQuery, {"team_ID": teamID, "year_ID": yearID})
        for row in rs:
            line: dict[str, str] = {}
            line["team_name"] = str(row[0])
            line["team_W"] = str(row[1])
            line["team_L"] = str(row[2])
            line["team_R"] = str(row[3])
            line["team_HR"] = str(row[4])
            line["team_BB"] = str(row[5])
            line["team_SO"] = str(row[6])
            line["team_AB"] = str(row[7])
            line["team_H"] = str(row[8])
            line["team_2B"] = str(row[9])
            line["team_3B"] = str(row[10])
            line["team_HR"] = str(row[11])
            line["team_BB"] = str(row[12])
            line["team_SO"] = str(row[13])
            line["team_SB"] = str(row[14])
            line["team_CS"] = str(row[15])
            line["team_HBP"] = str(row[16])
            line["team_SF"] = str(row[17])
            line["team_RA"] = str(row[18])
            line["team_ER"] = str(row[19])
            line["team_ERA"] = str(row[20])
            line["team_CG"] = str(row[21])
            line["team_SHO"] = str(row[22])
            line["team_SV"] = str(row[23])
            line["team_IPouts"] = str(row[24])
            line["team_HA"] = str(row[25])
            line["team_HRA"] = str(row[26])
            line["team_BBA"] = str(row[27])
            line["team_SOA"] = str(row[28])
            line["team_E"] = str(row[29])
            line["team_DP"] = str(row[30])
            line["team_FP"] = str(row[31])
            line["team_attendance"] = str(row[32])
            line["team_BPF"] = str(row[33])
            line["team_PPF"] = str(row[34])
            line["team_projW"] = str(row[35])
            line["team_projL"] = str(row[36])
            line["team_rank"] = row[37]
            line["team_G"] = str(row[38])
            line["franchID"] = str(row[39])
            line["WSWin"] = str(row[40])
            line["divWin"] = str(row[40])
            line["LGwin"] = str(row[40])


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
