from app import db
import sqlalchemy as sa
from app.models import Batting, People, Team, Pitching, Season, Fielding
from sqlalchemy import func, and_

def getBattingStats(teamId, year):
    subquery = (
        db.session.query(
            Batting.playerID.label("player_id"),
            func.sum(Batting.b_G).label("G"),
            func.sum(Batting.b_AB).label("PA"),
            func.sum(Batting.b_HR).label("HR"),
            func.sum(Batting.b_SB).label("SB"),
            (func.sum(Batting.b_BB)/ func.sum(Batting.b_AB)).label("BB"),
            (func.sum(Batting.b_SO)/ func.sum(Batting.b_AB)).label("K"),
            ((func.sum(Batting.b_2B) + (2 * func.sum(Batting.b_3B)) + (3 * func.sum(Batting.b_HR)))/
                func.sum(Batting.b_AB)).label("ISO"),
            ((func.sum(Batting.b_H) - func.sum(Batting.b_HR))/
             (func.sum(Batting.b_AB) - func.sum(Batting.b_SO) - func.sum(Batting.b_HR) + func.sum(Batting.b_SF))
                     ).label("BABIP"),
            (func.sum(Batting.b_H)/
                func.sum(Batting.b_AB)).label("AVG"),
            ((func.sum(Batting.b_H) + func.sum(Batting.b_BB) + func.sum(Batting.b_HBP))/
             (func.sum(Batting.b_AB) + func.sum(Batting.b_BB) + func.sum(Batting.b_HBP) + func.sum(Batting.b_SF))
            ).label("OBP"),
            ((((func.sum(Batting.b_H) - (func.sum(Batting.b_HR) + func.sum(Batting.b_3B) + func.sum(Batting.b_2B))) +
               (2 * func.sum(Batting.b_2B)) + (3 * func.sum(Batting.b_3B))) + (4*func.sum(Batting.b_HR)))/
                func.sum(Batting.b_AB)
            ).label("SLG"),
            (
                ((0.69 * (func.sum(Batting.b_BB) - func.sum(Batting.b_IBB))) +
                (0.72 * func.sum(Batting.b_HBP)) +
                (0.888 * ((func.sum(Batting.b_H) - (func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(Batting.b_HR))))) +
                (1.271 * func.sum(Batting.b_2B)) +
                (1.616 * func.sum(Batting.b_3B)) +
                (2.101 * func.sum(Batting.b_HR)))/
                (func.sum(Batting.b_AB) +
                func.sum(Batting.b_BB) -
                func.sum(Batting.b_IBB) +
                func.sum(Batting.b_SF) +
                func.sum(Batting.b_HBP))
            ).label("wOBA"),
            # func.sum().label("wRC+"),  # Unsure
            # func.sum().label("BsR"),  # Unsure
            # func.sum().label("Off"),  # Unsure
            # func.sum().label("Def"),  # Unsure
            # func.sum().label("WAR")  # Unsure

        )
        .filter(Batting.yearID == year, Batting.teamID == teamId)
        .group_by(Batting.playerID)
        .subquery()
    )

    results = (
        db.session.query(
            func.concat(People.nameFirst, ' ', People.nameLast).label("full_name"),
            subquery.c.player_id,
            subquery.c["G"],
            subquery.c.PA,
            subquery.c.HR,
            subquery.c.SB,
            subquery.c["BB"],
            subquery.c["K"],
            subquery.c["ISO"],
            subquery.c["BABIP"],
            subquery.c["AVG"],
            subquery.c["OBP"],
            subquery.c["SLG"],
            subquery.c["wOBA"],
            # subquery.c["wRC+"],
            # subquery.c["BsR"],
            # subquery.c["Off"],
            # subquery.c["Def"],
            # subquery.c["WAR"]
        )
        .join(People, People.playerID == subquery.c.player_id)
        .order_by(subquery.c.PA.desc())
        .all()
    )

    batting_data = {}
    for result in results:
        player_data = {
            "full_name": result.full_name,
            "player_id": result.player_id,
            "G": result.G,
            "PA": result.PA or 0,
            "HR": result.HR or 0,
            "SB": result.SB or 0,
            "BB%": result.BB or 0,
            "K%": result.K or 0,
            "ISO": result.ISO or 0,
            "BABIP": result.BABIP or 0,
            "AVG": result.AVG or 0,
            "OBP": result.OBP or 0,
            "SLG": result.SLG or 0,
            "wOBA": result.wOBA or 0,
            # "wRC+": result["wRC+"],
            # "BsR": result["BsR"],
            # "Off": result["Off"],
            # "Def": result["Def"],
            # "WAR": result["WAR"],
        }
        batting_data[result.player_id] = player_data

    return batting_data

def getPitchingStats(teamId, year):
    subquery = (
        db.session.query(
            Pitching.playerID.label("player_id"),

            (
                    func.sum(Pitching.p_IPOuts) / 3
            ).label("IP"),
            (  # k/9 = Strikeout Total / Innings Pitched * 9
                    func.sum(Pitching.p_SO)
                    / (func.sum(Pitching.p_IPOuts) / 3)
                    * 9
            ).label("K9"),
            (  # BB/9 = walks total / Innings Pitched * 9
                    func.sum(Pitching.p_BB)
                    / (func.sum(Pitching.p_IPOuts) / 3)
                    * 9
            ).label("BB9"),
            (  # HR/9 = Home Runs Total / Innings Pitched * 9
                    func.sum(Pitching.p_HR)
                    / (func.sum(Pitching.p_IPOuts) / 3)
                    * 9
            ).label("HR9"),
            (  # BABIP (Patting average on balls in play) = (H - HR)/(AB - SO - HR + SF)
                    (func.sum(Pitching.p_H) - func.sum(Pitching.p_HR))
                    /
                    (
                            (  # AB: At-bats (calculated as BFP−BB−HBP−SF)
                                    func.sum(Pitching.p_BFP)
                                    - func.sum(Pitching.p_BB)
                                    - func.sum(Pitching.p_HBP)
                                    - func.sum(Pitching.p_SF)
                            )
                            - func.sum(Pitching.p_SO)
                            - func.sum(Pitching.p_HR)
                            + func.sum(Pitching.p_SF)
                    )
            ).label("BABIP"),
            (  # LOB% = (H+BB+HBP-R)/(H+BB+HBP-(1.4*HR))
                    (
                            func.sum(Pitching.p_H)
                            + func.sum(Pitching.p_BB)
                            + func.sum(Pitching.p_HBP)
                            - func.sum(Pitching.p_R)
                    )
                    /
                    (
                            func.sum(Pitching.p_H)
                            + func.sum(Pitching.p_BB)
                            + func.sum(Pitching.p_HBP)
                            - (1.4 * func.sum(Pitching.p_HR))
                    )
            ).label("LOB"),
            (  # ERA exists!
                func.sum(Pitching.p_ERA)
            ).label("ERA"),
            (  # FIP = ((HR * 13)+ (3 * (BB+HBP)) - (2 * SO)) / IP + FIPconstant
                    (
                            (func.sum(Pitching.p_HR) * 13)
                            +
                            (3 *
                             (
                                     func.sum(Pitching.p_BB)
                                     + func.sum(Pitching.p_HBP)
                             )
                             )
                            -
                            (func.sum(Pitching.p_SO) * 2)
                    )
                    /
                    (func.sum(Pitching.p_IPOuts) / 3)
                    +
                    (Season.s_cFIP)
            ).label("FIP")
        )
        .filter(Pitching.yearID == year, Pitching.teamID == teamId, Season.yearID == year)
        .group_by(Pitching.playerID)
        .subquery()
    )

    results = (
        db.session.query(
            func.concat(People.nameFirst, ' ', People.nameLast).label("full_name"),
            subquery.c.player_id,
            subquery.c["IP"],
            subquery.c["K9"],
            subquery.c["BB9"],
            subquery.c["HR9"],
            subquery.c["BABIP"],
            subquery.c["LOB"],
            subquery.c["ERA"],
            subquery.c["FIP"],
        )
        .join(People, People.playerID == subquery.c.player_id)
        .order_by(subquery.c["IP"].desc())
        .all()
    )

    pitching_data = {}
    for result in results:
        player_data = {
            "full_name": result.full_name,
            "player_id": result.player_id,
            "IP": result.IP or 0,
            "K9": result.K9 or 0,
            "BB9": result.BB9 or 0,
            "HR9": result.HR9 or 0,
            "BABIP": result.BABIP or 0,
            "LOB": result.LOB or 0,
            "ERA": result.ERA or 0,
            "FIP": result.FIP or 0,

        }
        pitching_data[result.player_id] = player_data

    return pitching_data

def getTeam(teamId,year):
    team = db.session.scalar(
        sa.select(Team).where(and_(Team.teamID==teamId, Team.yearID == year))
    )
    return team

def getSelectedStats(teamId, year, stat):
    positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C', 'P', 'OF']
    all_stats = {'percentage': {}, 'PA': {}, 'wOBA': {}}
    for position in positions:
        percentage_query = (
            db.session.query(
                People.nameFirst,
                People.nameLast,
                Fielding.position,
                (func.sum(Fielding.f_InnOuts) /
                 func.sum(Fielding.f_InnOuts).over(partition_by=Fielding.position) * 100).label('stat_value')
            )
            .join(Fielding, People.playerID == Fielding.playerID)
            .filter(
                Fielding.teamID == teamId,
                Fielding.yearID == year,
                Fielding.position == position
            )
            .group_by(People.playerID, Fielding.position)
            .order_by(func.sum(Fielding.f_InnOuts).desc())
            .limit(6)
        )
        all_stats['percentage'][position] = percentage_query.all()

        # Query for Plate Appearances (PA)
        pa_query = (
            db.session.query(
                People.nameFirst,
                People.nameLast,
                Fielding.position,
                func.sum(Batting.b_AB + Batting.b_BB + Batting.b_HBP + Batting.b_SF + Batting.b_SH).label('stat_value')
            )
            .join(Fielding, People.playerID == Fielding.playerID)
            .join(Batting, Batting.playerID == Fielding.playerID)
            .filter(
                Fielding.teamID == teamId,
                Fielding.yearID == year,
                Fielding.position == position
            )
            .group_by(Fielding.playerID, Fielding.position)
            .order_by(func.sum(Batting.b_AB + Batting.b_BB + Batting.b_HBP + Batting.b_SF + Batting.b_SH).desc())
            .limit(6)
        )
        all_stats['PA'][position] = pa_query.all()

        woba_query = (
            db.session.query(
                People.nameFirst,
                People.nameLast,
                Fielding.position,
                (
                        ((0.69 * func.sum(Batting.b_BB)) +
                         (0.72 * func.sum(Batting.b_HBP)) +
                         (0.888 * func.sum(Batting.b_H)) +
                         (1.271 * func.sum(Batting.b_2B)) +
                         (1.616 * func.sum(Batting.b_3B)) +
                         (2.101 * func.sum(Batting.b_HR))) /
                        func.sum(Batting.b_AB + Batting.b_BB + Batting.b_HBP + Batting.b_SF + Batting.b_SH)
                ).label("stat_value")
            )
            .join(Fielding, People.playerID == Fielding.playerID)
            .join(Batting, Batting.playerID == Fielding.playerID)
            .filter(
                Fielding.teamID == teamId,
                Fielding.yearID == year,
                Fielding.position == position
            )
            .group_by(Fielding.playerID, Fielding.position)
            .order_by((
                              (0.69 * func.sum(Batting.b_BB)) +
                              (0.72 * func.sum(Batting.b_HBP)) +
                              (0.888 * func.sum(Batting.b_H)) +
                              (1.271 * func.sum(Batting.b_2B)) +
                              (1.616 * func.sum(Batting.b_3B)) +
                              (2.101 * func.sum(Batting.b_HR)) /
                              func.sum(Batting.b_AB) +
                              func.sum(Batting.b_BB) -
                              func.sum(Batting.b_IBB) +
                              func.sum(Batting.b_SF) +
                              func.sum(Batting.b_HBP)
                      ).desc())
            .limit(6)
        )
        all_stats['wOBA'][position] = woba_query.all()

    return all_stats.get(stat, {})
