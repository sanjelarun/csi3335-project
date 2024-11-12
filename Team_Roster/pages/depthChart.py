from flask import jsonify, render_template, request
from app import db
from app.models import People, Fielding, Batting
from sqlalchemy import func

def ShowDepthChart(teamId):
    year = request.args.get("year", type=int)
    stat = request.args.get('stat', 'percentage')  # Default to 'percentage' if no stat is specified

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
        all_stats['wOBA'][position] = woba_query.all()

        
    selected_stats = all_stats.get(stat, {})

    # Render the template and return the updated HTML
    return render_template('depthChart.html', positions_stats=selected_stats, stat=stat, teamID=teamId, year=year)
