from flask import render_template
from pages.stats import *

def ShowRoster(teamId, year):
    team = getTeam(teamId, year)
    return render_template(
        'roster.html',
        title="Roster - {} {}".format(year, team.team_name),
        teamId=teamId,
        team=team,
        year=year,
        pitching_data=getPitchingStats(teamId, year),
        batting_data=getBattingStats(teamId, year)
    )