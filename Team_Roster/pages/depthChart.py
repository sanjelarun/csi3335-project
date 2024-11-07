from flask import render_template

def ShowDepthChart(teamId,year):
    return render_template('depthChart.html', title="{}'s Depth Chart".format(teamId), teamId=teamId, year=year)