from flask import render_template
from pages.get_pitching_data import get_pitching_data

def ShowRoster(teamId, year):
    pitching_data = get_pitching_data(teamId, year)
    return render_template(
        'roster.html',
        title="{}'s Roster".format(teamId),
        teamId=teamId,
        year=year,
        pitching_data=pitching_data
    )