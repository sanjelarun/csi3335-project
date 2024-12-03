from flask import render_template
from app import db
import sqlalchemy as sa
from app.models import Batting, People, Team, Season, Fielding
from sqlalchemy import and_, func, case
from immaculateGridCalculations.complexFormulas import get_war, get_grouped_fielding



def getBattingStats(teamId, year):
    grouped_fielding= get_grouped_fielding()
    war = get_war(grouped_fielding)

    subquery = (
        db.session.query(
            Batting.playerID.label("player_id"),
            func.sum(Batting.b_G).label("G"),
            (
                func.sum(Batting.b_AB)+
                func.sum(Batting.b_BB)+
                func.sum(Batting.b_HBP)+
                func.sum(Batting.b_SH)+
                func.sum(Batting.b_SF)
            ).label("PA"),
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
                ((Season.s_wBB * (func.sum(Batting.b_BB) - func.sum(Batting.b_IBB))) +
                (Season.s_wHBP * func.sum(Batting.b_HBP)) +
                (Season.s_w1B  * ((func.sum(Batting.b_H) - (func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(Batting.b_HR))))) +
                (Season.s_w2B  * func.sum(Batting.b_2B)) +
                (Season.s_w3B  * func.sum(Batting.b_3B)) +
                (Season.s_wHR  * func.sum(Batting.b_HR)))/
                (func.sum(Batting.b_AB) +
                func.sum(Batting.b_BB) -
                func.sum(Batting.b_IBB) +
                func.sum(Batting.b_SF) +
                func.sum(Batting.b_HBP))
            ).label("wOBA"),
            ( #BsR = wSB=((SB*runSB)+(CS*runCS))-(lgwSB*(1B+BB+HBP-IBB))
                (
                    (func.sum(Batting.b_SB) * Season.s_runSB)
                    + 
                    (func.sum(Batting.b_CS) * Season.s_runCS)
                ) 
                -
                (
                    (# lgwSB=((lgSB*runSB)+(lgCS*runCS))/(lg1B+lgBB+lgHBP+lgIBB)
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
                        (func.sum(Batting.b_H) - (func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(Batting.b_HR))) #1B
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
        .join(grouped_fielding,and_(
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
    team = getTeam(teamId,year)

    return render_template('roster.html', title="Roster - {} {}".format(year, team.team_name), teamId=teamId, team=team, year=year, batting_data=battingData)