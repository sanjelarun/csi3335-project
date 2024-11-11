from Team_Roster.app.forms import FindTeam
from Team_Roster.app.models import Team
from flask import flash, jsonify, render_template, redirect
from Team_Roster.app import app, db
import sqlalchemy as sa

def ShowFindTeam():
    form = FindTeam()
    form.year.choices = [("","")]
    form.team.choices = [("","First select a year...")]

    years = db.session.scalars(
        sa.select(Team.yearID).distinct().order_by(Team.yearID.desc()))
    
    for year in years:
        form.year.choices.append((year,year))

    if form.validate_on_submit():
        return redirect('/{}/roster?year={}'.format(form.team.data,form.year.data))
    
    return render_template('findTeam.html', title='Find Team', form=form)

# AJAX request to fetch teams by year
@app.route('/get_teams/<int:year_id>', methods=['GET'])
def get_teams(year_id):
    teams = db.session.scalars(
        sa.select(Team).where(Team.yearID == year_id)
    )
    team_list = [(team.teamID, team.team_name) for team in teams]
    return jsonify(team_list)