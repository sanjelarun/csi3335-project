from flask import render_template

def ShowRoster(teamName, year):
    return render_template('roster.html', title="{}'s Roster".format(teamName), teamName=teamName, year=year)