from flask import render_template
from app import db
import sqlalchemy as sa
from app.models import Batting, People, Team, Season, Fielding
from sqlalchemy import and_, func, case




def getBattingStats(teamId, year):

    grouped_fielding = (
        db.session.query(
            Fielding.playerID.label("playerID"),
            Fielding.yearID.label("yearID"),
            Fielding.teamID.label("teamID"),
            Fielding.stint.label("stint"),
            Fielding.position.label("position"),
            Fielding.f_G.label("f_G"),
            Fielding.f_GS.label("f_GS"),
            Fielding.f_InnOuts.label("f_InnOuts"),
            Fielding.f_PO.label("f_PO"),
            Fielding.f_A.label("f_A"),
        )
        .group_by(Fielding.playerID, Fielding.yearID, Fielding.teamID, Fielding.stint)  # Ensure to group by all non-aggregated fields
        .subquery()
    )
    position_adjustments = { #used for war
    'C': 9,
    '1B': -9.5,
    '2B': 3,
    '3B': 2,
    'SS': 7,
    'LF': -7,
    'CF': 2.5,
    'RF': -7,
    }
    # Create a SQLAlchemy case expression

    adjustment_case = case(
        *[
            (grouped_fielding.c.position == position, adjustment * grouped_fielding.c.f_InnOuts/3)
            for position, adjustment in position_adjustments.items()
        ],
        else_=0  # Default adjustment if position doesn't match
    )

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
            # func.sum().label("wRC+"),  # Unsure
            # func.sum().label("BsR"),  # Unsure
            # func.sum().label("Off"),  # Unsure
            # func.sum().label("Def"),  # Unsure
            (# WAR = RaR/season R_W   
                (# RAR=wRAA + BsR + Rpos + RLR / RPW
                ( #wRAA = (wOBA - leagueWOBA) / wOBAScale * AB+BB+HBP+SF+SH
                    (
                    (#wOBA (took logan's equation)
                        ((Season.s_wBB * (func.sum(Batting.b_BB) - func.sum(Batting.b_IBB))) +
                        (Season.s_wHBP * func.sum(Batting.b_HBP)) +
                        (Season.s_w1B * ((func.sum(Batting.b_H) - (func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(Batting.b_HR))))) +
                        (Season.s_w2B * func.sum(Batting.b_2B)) +
                        (Season.s_w3B * func.sum(Batting.b_3B)) +
                        (Season.s_wHR * func.sum(Batting.b_HR)))
                        /
                        (func.sum(Batting.b_AB) +
                        (func.sum(Batting.b_BB) -
                        func.sum(Batting.b_IBB)) +
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
                )
                +
                ( # Positional Adjustment
                   func.sum(adjustment_case) / 1350
                )
                +
                ( # RLR = ((0.235 * G) * RPW * PA) / lgPA
                    (
                        (0.235 * Season.s_G/2)
                        * 
                        Season.s_R_W 
                        *
                        #PA = AB+BB+HBP+SF+SH
                        (func.sum(Batting.b_AB)+
                        func.sum(Batting.b_BB)+
                        func.sum(Batting.b_HBP)+
                        func.sum(Batting.b_SH)+
                        func.sum(Batting.b_SF))
                    )
                    /
                    Season.s_PA
                )
                )
                /Season.s_R_W
            ).label("WAR")  ,

            #####
            #####
            ( #wRAA = (wOBA - leagueWOBA) / wOBAScale * AB+BB+HBP+SF+SH
                    ((
                    (#wOBA (took logan's equation)
                        ((Season.s_wBB * (func.sum(Batting.b_BB) - func.sum(Batting.b_IBB))) +
                        (Season.s_wHBP * func.sum(Batting.b_HBP)) +
                        (Season.s_w1B * ((func.sum(Batting.b_H) - (func.sum(Batting.b_2B) + func.sum(Batting.b_3B) + func.sum(Batting.b_HR))))) +
                        (Season.s_w2B * func.sum(Batting.b_2B)) +
                        (Season.s_w3B * func.sum(Batting.b_3B)) +
                        (Season.s_wHR * func.sum(Batting.b_HR)))
                        /
                        (func.sum(Batting.b_AB) +
                        (func.sum(Batting.b_BB) -
                        func.sum(Batting.b_IBB)) +
                        func.sum(Batting.b_SF) +
                        func.sum(Batting.b_HBP))
                    )
                    - Season.s_wOBA
                    )
                    / Season.s_wOBAScale)
                    * ( #PA = AB+BB+HBP+SF+SH
                        func.sum(Batting.b_AB) +
                        func.sum(Batting.b_BB) +
                        func.sum(Batting.b_SF) +
                        func.sum(Batting.b_HBP) +
                        func.sum(Batting.b_SH)
                    )
            ).label("wRAA"),

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
                ( # Positional Adjustment
                   func.sum(adjustment_case) / 1350
                ).label("PositionalAdj"),
                ( # RLR = ((0.235 * G) * RPW * PA) / lgPA
                    (
                        (0.235 * Season.s_G)
                        * 
                        Season.s_R_W 
                        *
                        #PA = AB+BB+HBP+SF+SH
                        (func.sum(Batting.b_AB) +
                        func.sum(Batting.b_BB) +
                        func.sum(Batting.b_HBP) +
                        func.sum(Batting.b_SF) +
                        func.sum(Batting.b_SH))
                    )
                    /
                    Season.s_PA
                ).label("RLR")

        )       
        .join(grouped_fielding,and_(
            Batting.playerID == grouped_fielding.c.playerID,
            Batting.yearID == grouped_fielding.c.yearID,
            Batting.teamID == grouped_fielding.c.teamID,
            Batting.stint == grouped_fielding.c.stint
        
        ))
        .join(Season,Season.yearID == Batting.yearID)
        .filter(
            Batting.yearID == year,
            Batting.teamID == teamId,
            Season.yearID == year
        )
        .group_by(Batting.playerID)
        .subquery()
    )

    print(subquery)

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
            subquery.c["WAR"],
            subquery.c["wRAA"],
            subquery.c["BsR"],
            subquery.c["PositionalAdj"],
            subquery.c["RLR"],
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
            # "wRC+": result["wRC+"],
            # "BsR": result["BsR"],
            # "Off": result["Off"],
            # "Def": result["Def"],
            "WAR": result.WAR,
            "wRAA": result.wRAA,
            "BsR": result.BsR,
            "PositionalAdj": result.PositionalAdj,
            "RLR": result.RLR
        }
        batting_data[result.player_id] = player_data

        if result.full_name == "Josh Harrison":
            print(player_data)

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