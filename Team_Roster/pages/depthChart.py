from flask import jsonify, render_template, request
from app import db
import sqlalchemy as sa
from app.models import People, Fielding, Batting, Team, Pitching, Season
from sqlalchemy import func, and_
from pages.stats import *

def getTeam(teamId,year):
    team = db.session.scalar(
        sa.select(Team).where(and_(Team.teamID==teamId, Team.yearID == year))
    )
    return team

def getSelectedStats(teamId,year,stat):
    positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C', 'P']
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
        all_stats['percentage'][position] = [row._asdict() for row in percentage_query.all()]

            # Query for Plate Appearances (PA) -- Every player is in batting but not necessarily in pitching. Use to determine PA better?
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
        all_stats['PA'][position] = [row._asdict() for row in pa_query.all()]

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
                    (2.101 * func.sum(Batting.b_HR)))/
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
                    (2.101 * func.sum(Batting.b_HR))/
                    func.sum(Batting.b_AB) +
                    func.sum(Batting.b_BB) -
                    func.sum(Batting.b_IBB) +
                    func.sum(Batting.b_SF) +
                    func.sum(Batting.b_HBP)
                ).desc())
            .limit(6)
        )
        all_stats['wOBA'][position] = [row._asdict() for row in woba_query.all()]

        
    return all_stats.get(stat, {})

def getPitchingStats(teamId,year):
    subquery = (
        db.session.query(
            Pitching.playerID.label("player_id"),

            (
                func.sum(Pitching.p_IPOuts)/3
            ).label("IP"),
            ( #k/9 = Strikeout Total / Innings Pitched * 9
                func.sum(Pitching.p_SO)
                /(func.sum(Pitching.p_IPOuts)/3)
                *9
             ).label("K9"),
            ( #BB/9 = walks total / Innings Pitched * 9
                func.sum(Pitching.p_BB)
                /(func.sum(Pitching.p_IPOuts)/3)
                *9
             ).label("BB9"),
            ( #HR/9 = Home Runs Total / Innings Pitched * 9
                func.sum(Pitching.p_HR)
                /(func.sum(Pitching.p_IPOuts)/3)
                *9
             ).label("HR9"),
             ( #BABIP (Patting average on balls in play) = (H - HR)/(AB - SO - HR + SF)
                (func.sum(Pitching.p_H) - func.sum(Pitching.p_HR))
                /
                (
                    (#AB: At-bats (calculated as BFP−BB−HBP−SF)
                        func.sum(Pitching.p_BFP)
                        -func.sum(Pitching.p_BB)
                        -func.sum(Pitching.p_HBP)
                        -func.sum(Pitching.p_SF)
                    )
                    - func.sum(Pitching.p_SO)
                    - func.sum(Pitching.p_HR)
                    + func.sum(Pitching.p_SF)
                )
             ).label("BABIP"),
            ( # LOB% = (H+BB+HBP-R)/(H+BB+HBP-(1.4*HR))
                (
                    func.sum(Pitching.p_H)
                    +func.sum(Pitching.p_BB)
                    +func.sum(Pitching.p_HBP)
                    -func.sum(Pitching.p_R)
                )
                /
                (
                    func.sum(Pitching.p_H)
                    +func.sum(Pitching.p_BB)
                    +func.sum(Pitching.p_HBP)
                    -( 1.4* func.sum(Pitching.p_HR))
                )
            ).label("LOB"),
            ( #ERA exists!
                func.sum(Pitching.p_ERA) 
            ).label("ERA"),
            ( #FIP = ((HR * 13)+ (3 * (BB+HBP)) - (2 * SO)) / IP + FIPconstant
                (
                    (func.sum(Pitching.p_HR) * 13)
                    +
                    ( 3 *
                      (
                          func.sum(Pitching.p_BB)
                          +func.sum(Pitching.p_HBP)
                      )
                    )
                    -
                    (func.sum(Pitching.p_SO) * 2)
                )
                /
                ( func.sum(Pitching.p_IPOuts)/3)
                +
                (Season.s_cFIP)
            ).label("FIP")
        )
        .filter(Pitching.yearID == year, Pitching.teamID == teamId,Season.yearID == year)
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

    batting_data = {}
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
        batting_data[result.player_id] = player_data

    return batting_data

def getBattingStats(teamId,year):
    subquery=(
        db.session.query(
            Batting.playerID.label("player_id"),
            (
                (Batting.b_AB)+
                (Batting.b_BB)+
                (Batting.b_HBP)+
                (Batting.b_SH)+
                (Batting.b_SF)
            ).label("PA"),
            (
                func.sum(Batting.b_H) /
                func.sum(Batting.b_AB)
            ).label("AVG"),
            (
                (func.sum(Batting.b_H) + func.sum(Batting.b_BB) + func.sum(Batting.b_HBP)) /
                (func.sum(Batting.b_AB) + func.sum(Batting.b_BB) + func.sum(Batting.b_HBP) + func.sum(Batting.b_SF))
             ).label("OBP"),
            (
                (((func.sum(Batting.b_H) - (func.sum(Batting.b_HR) + func.sum(Batting.b_3B) + func.sum(Batting.b_2B))) +
                (2 * func.sum(Batting.b_2B)) + (3 * func.sum(Batting.b_3B))) + (4 * func.sum(Batting.b_HR))) / func.sum(Batting.b_AB)
             ).label("SLG"),
            (
                ((0.69 * (func.sum(Batting.b_BB) - func.sum(Batting.b_IBB))) +
                (0.72 * func.sum(Batting.b_HBP)) +
                (0.888 * ((func.sum(Batting.b_H) - (
                        func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(Batting.b_HR))))) +
                (1.271 * func.sum(Batting.b_2B)) +
                (1.616 * func.sum(Batting.b_3B)) +
                (2.101 * func.sum(Batting.b_HR))) /
                (func.sum(Batting.b_AB) +
                func.sum(Batting.b_BB) -
                func.sum(Batting.b_IBB) +
                func.sum(Batting.b_SF) +
                func.sum(Batting.b_HBP))
            ).label("wOBA"),
            (
                # Seriously stumped on how to calculate this value
                (
                    (Batting.b_R) +
                    #Base Running-Runs
                    ((Batting.b_SB*Season.s_runSB+
                     Batting.b_CS*Season.s_runCS-
                      (Season.s_runSB * (Batting.b_BB +Batting.b_HBP + Batting.b_IBB)))+
                     (Batting.b_GIDP))+
                    func.sum(Batting.b_2B)+ # Helps get close to target value
                    func.sum(Batting.b_3B)+ # Helps get close to target value
                    (Batting.b_BB)
                )
                /(9*Season.s_R_W*1.5+3) # Generic formula for RPW
            ).label("WAR")
        ).filter(Batting.yearID == year, Batting.teamID == teamId, Season.yearID ==year)
        .group_by(Batting.playerID)
        .subquery()
    )
    results = (
        db.session.query(
            func.concat(People.nameFirst, ' ', People.nameLast).label("full_name"),
            subquery.c.player_id,
            subquery.c["PA"],
            subquery.c["AVG"],
            subquery.c["OBP"],
            subquery.c["SLG"],
            subquery.c["wOBA"],
            # subquery.c["Bat"],
            # subquery.c["Fld"],
            # subquery.c["BsR"],
            subquery.c["WAR"]
        )
        .join(People, People.playerID == subquery.c.player_id)
        .order_by(subquery.c["PA"].desc())
        .all()
    )
    batting_data = {}
    for result in results:
        player_data = {
            "full_name": result.full_name,
            "player_id": result.player_id,
            "PA": result.PA or 0,
            "AVG": result.AVG or 0,
            "OBP": result.OBP or 0,
            "SLG": result.SLG or 0,
            "wOBA": result.wOBA or 0,
            # "Bat": result.Bat or 0,
            # "Fld": result.Fld or 0,
            # "BsR": result.BsR or 0,
            "WAR": result.WAR or 0,
        }
        batting_data[result.player_id] = player_data
    return batting_data


def ShowDepthChart(teamId, year):
    
    stat = request.args.get('stat', 'percentage')  # Default to 'percentage' if no stat is specified

    selected_stats = getSelectedStats(teamId,year,stat)
    
    pitching_stats = getPitchingStats(teamId,year)

    batting_stats = getBattingStats(teamId, year)

    team=getTeam(teamId,year)

    return render_template('depthChart.html',title="Depth Chart - {} {}".format(year, team.team_name), positions_stats=selected_stats, pitching_stats = pitching_stats, batting_stats=batting_stats, stat=stat, team=team, teamId=teamId, year=year)
