
from sqlalchemy import case, func
from app.models import Batting, Fielding, Season
from app import db


def get_grouped_fielding():
    return(
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





def get_war(grouped_fielding):
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

    return(
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
            )
    )