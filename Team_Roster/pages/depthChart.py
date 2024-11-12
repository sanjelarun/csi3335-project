from flask import jsonify, render_template, request
from app import db
from app.models import People, Fielding, Batting
from sqlalchemy import func

def ShowDepthChart(teamId):
    year = request.args.get("year", type=int)
    stat = request.args.get('stat', 'percentage')  # Default to 'percentage' if no stat is specified

    positions_stats = {}

    positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C', 'P', 'OF']

    for position in positions:
        if stat == 'percentage':
            position_query = (
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

        elif stat == 'PA':
            # Query for Plate Appearances (PA)
            position_query = (
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
        else:
            return jsonify({'error': 'Invalid statistic selected'}), 400

        
        positions_stats[position] = position_query.all()

    # Render the template and return the updated HTML
    return render_template('depthChart.html', positions_stats=positions_stats, stat=stat, teamID=teamId, year=year)
