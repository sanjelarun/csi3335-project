from flask import render_template, flash, redirect, request

from app import app

from pages.findTeam import ShowFindTeam
from pages.roster import ShowRoster
from pages.depthChart import ShowDepthChart

@app.route('/')
@app.route('/index')
@app.route('/findTeam', methods=['GET', 'POST'])
def findTeam():
    return ShowFindTeam()

@app.route('/<teamId>/roster',methods=['GET'])
def roster(teamId):
    year =request.args.get("year")
    return ShowRoster(teamId,year)

@app.route('/<teamId>/depthChart',methods=['GET'])
def depthChart(teamId):
    year =request.args.get("year")
    return ShowDepthChart(teamId,year)