from flask import jsonify, render_template, request
from app import db
from app.models import People, Fielding, Team
from sqlalchemy import func

def ShowDepthChart(teamId):
    year = request.args.get("year", type=int)
    stat = request.args.get('stat', 'percentage')  # Default to 'percentage' if no stat is specified

    positions_stats = {}

    positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C', 'P', 'OF']

    for position in positions:
        if stat == 'percentage':
            # Query for time percentage (percentage of innings played at a position)
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
                    func.sum(Fielding.f_A).label('stat_value')
                )
                .join(Fielding, People.playerID == Fielding.playerID)
                .filter(
                    Fielding.teamID == teamId,
                    Fielding.yearID == year,
                    Fielding.position == position
                )
                .group_by(Fielding.playerID, Fielding.position)
                .order_by(func.sum(Fielding.f_A).desc())  # Correct ordering for PA
                .limit(6)
            )
        else:
            # If an invalid stat is selected, return an error response
            return jsonify({'error': 'Invalid statistic selected'}), 400

        # Execute the query and store the results for the position
        position_data = position_query.all()

        positions_stats[position] = position_query.all()
        print(f"Position: {position}, Data: {position_data}")  # Debugging line

    # Render the template and return the updated HTML
    return render_template('depthChart.html', positions_stats=positions_stats, stat=stat, teamID=teamId, year=year)
