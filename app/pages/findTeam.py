from app.forms import FindTeam
from app.models import Team
from flask import jsonify, render_template, redirect
import sqlalchemy as sa
from app import db

def ShowFindTeam():
    form = FindTeam()
    form.year.choices = [("", "Select Year...")]
    form.team.choices = [("", "First select a year...")]

    years = db.session.scalars(
        sa.select(Team.yearID).distinct().order_by(Team.yearID.desc()))

    for year in years:
        form.year.choices.append((year, year))

    if form.validate_on_submit():
        return redirect('/{}/roster?year={}'.format(form.team.data, form.year.data))

    return render_template('findTeam.html', title='Find Team', form=form)

def getTeams(year_id):
    teams = db.session.scalars(
        sa.select(Team).where(Team.yearID == year_id)
    )
    team_list = [(team.teamID, team.team_name) for team in teams]
    return jsonify(team_list)