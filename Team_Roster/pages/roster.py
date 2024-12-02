from flask import render_template
from app import db
import sqlalchemy as sa
from app.models import Batting, People, Team, Season, Fielding
from sqlalchemy import and_, func


def getBattingStats(teamId, year):
    subquery = (
        db.session.query(
            Batting.playerID.label("player_id"),
            func.sum(Batting.b_G).label("G"),
            (
                (Batting.b_AB)+
                (Batting.b_BB)+
                (Batting.b_HBP)+
                (Batting.b_SH)+
                (Batting.b_SF)
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
            (# WAR = RaR/season R_W   
                (# RAR=wRAA + BsR + Fielding Runs + Positional Adjustment + Replacement Runs
                ( #wRAA = (wOBA - leagueWOBA) / wOBAScale * AB+BB+HBP+SF+SH
                    (
                    (#wOBA (took logan's equation)
                        ((0.69 * (func.sum(Batting.b_BB) - func.sum(Batting.b_IBB))) +
                        (0.72 * func.sum(Batting.b_HBP)) +
                        (0.888 * ((func.sum(Batting.b_H) - (func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(Batting.b_HR))))) +
                        (1.271 * func.sum(Batting.b_2B)) +
                        (1.616 * func.sum(Batting.b_3B)) +
                        (2.101 * func.sum(Batting.b_HR)))
                        /
                        (func.sum(Batting.b_AB) +
                        func.sum(Batting.b_BB) -
                        func.sum(Batting.b_IBB) +
                        func.sum(Batting.b_SF) +
                        func.sum(Batting.b_HBP))
                    )
                    - Season.s_wOBA
                    )
                    / Season.s_wOBAScale
                    * ( #PA = AB+BB+HBP+SF+SH
                        (func.sum(Batting.b_AB) +
                        func.sum(Batting.b_BB) +
                        func.sum(Batting.b_HBP) +
                        func.sum(Batting.b_SF) +
                        func.sum(Batting.b_SH))
                    )
                )
                + 
                ( #BsR=(SB×runSB)−(CS×runCS) -(lgwSB*(1B+BB+HBP)) 
                    (func.sum(Batting.b_SB) * Season.s_runSB)
                    +
                    (func.sum(Batting.b_CS) * Season.s_runCS)
                )
                +
                ( # Fielding Runs= Range Runs+Error Runs + Double Play Runs
                    0
                    #func.sum(Fielding.f_ZR)
                    # + Error runs
                    # + Double play controbutions

                )
                # + Positional Adjustment
                +
                ( # Replacement Runs = 20/600 * PA
                    (20/600)
                    * ( #PA = AB+BB+HBP+SF+SH
                        (func.sum(Batting.b_AB) +
                        func.sum(Batting.b_BB) +
                        func.sum(Batting.b_HBP) +
                        func.sum(Batting.b_SF) +
                        func.sum(Batting.b_SH))
                    )
                )
                )
                /Season.s_R_W
            ).label("WAR")  

        )
        .filter(Batting.yearID == year, Batting.teamID == teamId, Season.yearID == year, Fielding.yearID==year)
        .join(Fielding, Batting.playerID == Fielding.playerID)
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
            subquery.c["WAR"]
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