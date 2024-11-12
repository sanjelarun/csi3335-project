from flask import render_template
from app import db
from app.models import Batting, People
from sqlalchemy import func


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
            (func.sum(Batting.b_2B) + (2 * func.sum(Batting.b_3B)) + (3 * func.sum(Batting.b_HR))/
                func.sum(Batting.b_AB)).label("ISO"),
            (func.sum(Batting.b_H) - func.sum(Batting.b_HR)/
                func.sum(Batting.b_AB) - (func.sum(Batting.b_SO)/func.sum(Batting.b_AB)) - func.sum(Batting.b_HR) + func.sum(Batting.b_SF)
                     ).label("BABIP"),
            (func.sum(Batting.b_H)/
                func.sum(Batting.b_AB)).label("AVG"),
            (func.sum(Batting.b_H) + func.sum(Batting.b_BB) + func.sum(Batting.b_HBP)/
                func.sum(Batting.b_AB) + func.sum(Batting.b_HBP) + func.sum(Batting.b_SF)
            ).label("OBP"),
            (func.sum(Batting.b_H) + (2 * func.sum(Batting.b_2B)) + (3 * func.sum(Batting.b_3B)) + (
                    func.sum(Batting.b_HR))/
                func.sum(Batting.b_AB)
            ).label("SLG"),
            (
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
        .order_by(subquery.c["G"])
        .all()
    )

    batting_data = {}
    for result in results:
        player_data = {
            "full_name": result.full_name,
            "player_id": result.player_id,
            "PA": result.PA,
            "HR": result.HR,
            "SB": result.SB,
            "BB%": result.BB,
            "K%": result.K,
            "ISO": result.ISO,
            "BABIP": result.BABIP,
            "AVG": result.AVG,
            "OBP": result.OBP,
            "SLG": result.SLG,
            "wOBA": result.wOBA,
            # "wRC+": result["wRC+"],
            # "BsR": result["BsR"],
            # "Off": result["Off"],
            # "Def": result["Def"],
            # "WAR": result["WAR"],
        }
        batting_data[result.player_id] = player_data

    return batting_data
def ShowRoster(teamId, year):
    return render_template('roster.html', title="{}'s Roster".format(teamId), teamId=teamId, year=year, batting_data=getBattingStats(teamId, year))