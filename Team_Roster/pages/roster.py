from flask import render_template
from sqlalchemy import func
from Team_Roster.app import db
from Team_Roster.app.models import Pitching, People

def ShowRoster(teamId, year):
    league_fip = 4.20
    fip_constant = 10.5

    # Subquery for aggregated pitching data
    subquery = (
        db.session.query(
            Pitching.playerID.label("player_id"),
            func.sum(Pitching.p_G).label("G"),
            func.sum(Pitching.p_GS).label("GS"),
            func.div(func.sum(Pitching.p_IPOuts), 3).label("IP"),
            func.div(func.sum(Pitching.p_SO * 100.0), func.sum(Pitching.p_BFP)).label("K%"),
            func.div(func.sum(Pitching.p_BB) * 100.0, func.sum(Pitching.p_BFP)).label("BB%"),
            func.div(func.sum(Pitching.p_HR) * 9.0,
                     func.div(func.sum(Pitching.p_IPOuts), 3.0)).label("HR/9"),
            func.div(
                (func.sum(Pitching.p_H) - func.sum(Pitching.p_HR)),
                (func.sum(Pitching.p_BFP) - func.sum(Pitching.p_SO) -
                 func.sum(Pitching.p_BB) - func.sum(Pitching.p_HR) - func.sum(Pitching.p_HBP))
            ).label("BABIP"),
            func.div(
                (func.sum(Pitching.p_H) + func.sum(Pitching.p_BB) +
                 func.sum(Pitching.p_HBP) - func.sum(Pitching.p_ER)),
                (func.sum(Pitching.p_H) + func.sum(Pitching.p_BB) +
                 func.sum(Pitching.p_HBP) - (1.4 * func.sum(Pitching.p_HR)))
            ).label("LOB%"),
            func.div(func.sum(Pitching.p_ER) * 9.0,
                     (func.sum(Pitching.p_IPOuts) / 3.0)).label("ERA"),
            func.div(
                (13 * func.sum(Pitching.p_HR)) +
                (3 * func.sum(Pitching.p_BB)) -
                (2 * func.sum(Pitching.p_SO)) +
                (3 * func.sum(Pitching.p_HBP)),
                (func.sum(Pitching.p_IPOuts) / 3.0)
            ).label("FIP") + 3.1,
        )
        .filter(Pitching.yearID == year, Pitching.teamID == teamId)
        .group_by(Pitching.playerID)
        .subquery()
    )

    # Main query to fetch player names and stats
    results = (
        db.session.query(
            func.concat(People.nameFirst, ' ', People.nameLast).label("full_name"),
            subquery.c.player_id,
            subquery.c["G"],
            subquery.c["GS"],
            subquery.c["IP"],
            subquery.c["K%"],
            subquery.c["BB%"],
            subquery.c["HR/9"],
            subquery.c["BABIP"],
            subquery.c["LOB%"],
            subquery.c["ERA"],
            subquery.c["FIP"],
            ((league_fip - subquery.c.FIP) * subquery.c.IP / fip_constant).label("WAR"),
        )
        .join(People, People.playerID == subquery.c.player_id)
        .order_by(subquery.c["G"])
        .all()
    )

    # Prepare pitching data dictionary
    pitching_data = {}
    for result in results:
        player_data = {
            "full_name": result.full_name,
            "player_id": result.player_id,
            "G": result.G,
            "GS": result.GS,
            "IP": result.IP,
            "K%": result["K%"],
            "BB%": result["BB%"],
            "HR/9": result["HR/9"],
            "BABIP": result["BABIP"],
            "LOB%": result["LOB%"],
            "ERA": result["ERA"],
            "FIP": result["FIP"],
            "WAR": result["WAR"],
        }
        pitching_data[result.player_id] = player_data

    # Render template with team and pitching data
    return render_template('roster.html', title="{}'s Roster".format(teamId), teamId=teamId, year=year, pitching_data=pitching_data)