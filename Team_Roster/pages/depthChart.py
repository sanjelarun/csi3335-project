from flask import render_template
from app import db
import sqlalchemy as sa
from app.models import People, Fielding, Team
from sqlalchemy import func, and_

def getTeam(teamId,year):
    team = db.session.scalar(
        sa.select(Team).where(and_(Team.teamID==teamId, Team.yearID == year))
    )
    return team

def ShowDepthChart(teamId, year):
    #Query to get player fielding time in each position for the specified team and year
    subquery = (
        db.session.query(
            Fielding.position,
            Fielding.playerID,
            func.sum(Fielding.f_InnOuts).label("total_innouts"),
        )
        .filter(Fielding.yearID == year, Fielding.teamID == teamId)
        .group_by(Fielding.position, Fielding.playerID)
        .subquery()
    )

    #Main query to calculate time percentage and retrieve player names
    results = (
        db.session.query(
            subquery.c.position,
            People.playerID,
            People.nameFirst,
            People.nameLast,
            (subquery.c.total_innouts / func.sum(subquery.c.total_innouts).over(partition_by=subquery.c.position) * 100).label("time_percentage"),
        )
        .join(People, People.playerID == subquery.c.playerID)
        .order_by(subquery.c.position, subquery.c.total_innouts.desc())
        .all()
    )

    #Seperate by position
    position_data = {}
    for result in results:
        pos = result.position
        if pos not in position_data:
            position_data[pos] = []
        position_data[pos].append({
            "name": f"{result.nameFirst} {result.nameLast}",
            "time_percentage": f"{result.time_percentage:.2f}%"
        })

    team=getTeam(teamId,year)

    return render_template('depthChart.html',title="Depth Chart - {} {}".format(year, team.team_name), position_data=position_data, team=team, teamId=teamId, year=year)
