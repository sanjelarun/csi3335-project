from flask import jsonify, render_template, request
from pages.stats import *

def ShowDepthChart(teamId, year):
    
    stat = request.args.get('stat', 'percentage')  # Default to 'percentage' if no stat is specified

    selected_stats = getSelectedStats(teamId,year,stat)
    
    pitching_stats = getPitchingStats(teamId,year)

    team=getTeam(teamId,year)

    return render_template('depthChart.html',title="Depth Chart - {} {}".format(year, team.team_name), positions_stats=selected_stats, pitching_stats = pitching_stats, stat=stat, team=team, teamId=teamId, year=year)
