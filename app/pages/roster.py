from flask import render_template
from app import db
import sqlalchemy as sa
from app.models import Batting, People, Team, Season, Pitching, Queries, Users
from sqlalchemy import and_, func
from immaculateGridCalculations.complexFormulas import get_war, get_grouped_fielding
from flask_login import current_user

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

def getBattingStats(teamId, year):
    grouped_fielding = get_grouped_fielding()
    war = get_war(grouped_fielding)

    subquery = (
        db.session.query(
            Batting.playerID.label("player_id"),
            func.sum(Batting.b_G).label("G"),
            (
                    func.sum(Batting.b_AB) +
                    func.sum(Batting.b_BB) +
                    func.sum(Batting.b_HBP) +
                    func.sum(Batting.b_SH) +
                    func.sum(Batting.b_SF)
            ).label("PA"),
            func.sum(Batting.b_HR).label("HR"),
            func.sum(Batting.b_SB).label("SB"),
            (func.sum(Batting.b_BB) / func.sum(Batting.b_AB)).label("BB"),
            (func.sum(Batting.b_SO) / func.sum(Batting.b_AB)).label("K"),
            ((func.sum(Batting.b_2B) + (2 * func.sum(Batting.b_3B)) + (3 * func.sum(Batting.b_HR))) /
             func.sum(Batting.b_AB)).label("ISO"),
            ((func.sum(Batting.b_H) - func.sum(Batting.b_HR)) /
             (func.sum(Batting.b_AB) - func.sum(Batting.b_SO) - func.sum(Batting.b_HR) + func.sum(Batting.b_SF))
             ).label("BABIP"),
            (func.sum(Batting.b_H) /
             func.sum(Batting.b_AB)).label("AVG"),
            ((func.sum(Batting.b_H) + func.sum(Batting.b_BB) + func.sum(Batting.b_HBP)) /
             (func.sum(Batting.b_AB) + func.sum(Batting.b_BB) + func.sum(Batting.b_HBP) + func.sum(Batting.b_SF))
             ).label("OBP"),
            ((((func.sum(Batting.b_H) - (func.sum(Batting.b_HR) + func.sum(Batting.b_3B) + func.sum(Batting.b_2B))) +
               (2 * func.sum(Batting.b_2B)) + (3 * func.sum(Batting.b_3B))) + (4 * func.sum(Batting.b_HR))) /
             func.sum(Batting.b_AB)
             ).label("SLG"),
            (
                    ((Season.s_wBB * (func.sum(Batting.b_BB) - func.sum(Batting.b_IBB))) +
                     (Season.s_wHBP * func.sum(Batting.b_HBP)) +
                     (Season.s_w1B * ((func.sum(Batting.b_H) - (
                                 func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(Batting.b_HR))))) +
                     (Season.s_w2B * func.sum(Batting.b_2B)) +
                     (Season.s_w3B * func.sum(Batting.b_3B)) +
                     (Season.s_wHR * func.sum(Batting.b_HR))) /
                    (func.sum(Batting.b_AB) +
                     func.sum(Batting.b_BB) -
                     func.sum(Batting.b_IBB) +
                     func.sum(Batting.b_SF) +
                     func.sum(Batting.b_HBP))
            ).label("wOBA"),
            (  # BsR = wSB=((SB*runSB)+(CS*runCS))-(lgwSB*(1B+BB+HBP-IBB))
                    (
                            (func.sum(Batting.b_SB) * Season.s_runSB)
                            +
                            (func.sum(Batting.b_CS) * Season.s_runCS)
                    )
                    -
                    (
                            (  # lgwSB=((lgSB*runSB)+(lgCS*runCS))/(lg1B+lgBB+lgHBP+lgIBB)
                                    (
                                            (Season.s_SB * Season.s_runSB) +
                                            (Season.s_CS * Season.s_runCS)
                                    )
                                    /
                                    (
                                            Season.s_1B + Season.s_BB + Season.s_HBP - Season.s_IBB
                                    )
                            )
                            *
                            (
                                    (func.sum(Batting.b_H) - (
                                                func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(
                                            Batting.b_HR)))  # 1B
                                    +
                                    func.sum(Batting.b_BB)
                                    +
                                    func.sum(Batting.b_HBP)
                                    -
                                    func.sum(Batting.b_IBB)
                            )
                    )
            ).label("BsR"),
            war.label("WAR"),

        )
        .join(grouped_fielding, and_(
            Batting.playerID == grouped_fielding.c.playerID,
            Batting.yearID == grouped_fielding.c.yearID,
            Batting.teamID == grouped_fielding.c.teamID,
            Batting.stint == grouped_fielding.c.stint

        ))
        .filter(
            Batting.yearID == year,
            Batting.teamID == teamId,
            Season.yearID == year
        )
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
            subquery.c["BsR"],
            subquery.c["WAR"],
        )
        .join(People, People.playerID == subquery.c.player_id)
        .order_by(subquery.c.WAR.desc())
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
            "BsR": result.BsR or 0,
            "WAR": result.WAR,
        }
        batting_data[result.player_id] = player_data

    return batting_data

def getTeam(teamId,year):
    team = db.session.scalar(
        sa.select(Team).where(and_(Team.teamID==teamId, Team.yearID == year))
    )
    return team

def ShowRoster(teamId, year):

    battingData = getBattingStats(teamId,year)
    pitchingData = getPitchingStats(teamId,year)
    team = getTeam(teamId,year)

    query = Queries(user_ID=current_user.get_id(), q_TEAM=team.team_name, q_YEAR=year)
    db.session.add(query)
    db.session.commit()

    return render_template('roster.html', title="Roster - {} {}".format(year, team.team_name), teamId=teamId, team=team, year=year, batting_data=battingData, pitching_data=pitchingData)