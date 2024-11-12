from sqlalchemy import func
from app import db
from app.models import Pitching, People

def get_pitching_data(teamId, year):
    league_fip = 4.20
    fip_constant = 10.5

    subquery = (
        db.session.query(
            Pitching.playerID.label("player_id"),
            func.sum(Pitching.p_G).label("G"),
            func.sum(Pitching.p_GS).label("GS"),
            (func.sum(Pitching.p_IPOuts) / 3).label("IP"),
            ((func.sum(Pitching.p_SO) * 100.0) / func.sum(Pitching.p_BFP)).label("K%"),
            ((func.sum(Pitching.p_BB) * 100.0) / func.sum(Pitching.p_BFP)).label("BB%"),
            ((func.sum(Pitching.p_HR) * 9.0) / (func.sum(Pitching.p_IPOuts) / 3.0)).label("HR/9"),
            ((func.sum(Pitching.p_H) - func.sum(Pitching.p_HR)) /
             ((func.sum(Pitching.p_BFP) - func.sum(Pitching.p_SO) -
               func.sum(Pitching.p_BB) - func.sum(Pitching.p_HR) - func.sum(Pitching.p_HBP)))
             ).label("BABIP"),
            ((func.sum(Pitching.p_H) + func.sum(Pitching.p_BB) +
              func.sum(Pitching.p_HBP) - func.sum(Pitching.p_ER)) /
             (func.sum(Pitching.p_H) + func.sum(Pitching.p_BB) +
              func.sum(Pitching.p_HBP) - (1.4 * func.sum(Pitching.p_HR)))
             ).label("LOB%"),
            ((func.sum(Pitching.p_ER) * 9.0) / (func.sum(Pitching.p_IPOuts) / 3.0)).label("ERA"),
            (((13 * func.sum(Pitching.p_HR)) +
              (3 * func.sum(Pitching.p_BB)) -
              (2 * func.sum(Pitching.p_SO)) +
              (3 * func.sum(Pitching.p_HBP)) /
              (func.sum(Pitching.p_IPOuts) / 3.0)) + 3.1
             ).label("FIP")
        )
        .filter(Pitching.yearID == year, Pitching.teamID == teamId)
        .group_by(Pitching.playerID)
        .subquery()
    )

    results = (
        db.session.query(
            subquery.c.player_id,
            func.concat(People.nameFirst,' ', People.nameLast).label("full_name"),
            subquery.c.G,
            subquery.c.GS,
            subquery.c.IP,
            subquery.c["K%"].label("K_percent"),
            subquery.c["BB%"].label("BB_percent"),
            subquery.c["HR/9"].label("HR_per_9"),
            subquery.c.BABIP,
            subquery.c["LOB%"].label("LOB_percent"),
            subquery.c.ERA,
            subquery.c.FIP,
            ((league_fip - subquery.c.FIP) * subquery.c.IP / fip_constant).label("WAR"),
        )
        .join(People, People.playerID == subquery.c.player_id)
        .all()
    )

    pitching_data = {}
    for result in results:
        pitching_data[result.player_id] = {
            "full_name": result.full_name,
            "G": result.G,
            "GS": result.GS,
            "IP": result.IP,
            "K%": result.K_percent,
            "BB%": result.BB_percent,
            "HR/9": result.HR_per_9,
            "BABIP": result.BABIP,
            "LOB%": result.LOB_percent,
            "ERA": result.ERA,
            "FIP": result.FIP,
            "WAR": result.WAR,
        }

    return pitching_data