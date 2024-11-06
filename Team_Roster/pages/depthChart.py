from flask import render_template

def ShowDepthChart(teamName,year):
    return render_template('depthChart.html', title="{}'s Depth Chart".format(teamName), teamName=teamName, year=year)