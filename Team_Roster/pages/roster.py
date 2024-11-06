from flask import render_template

def ShowRoster(teamId, year):
    return render_template('roster.html', title="{}'s Roster".format(teamId), teamId=teamId, year=year)