from flask import render_template, flash, redirect, request

from app import app

from pages.index import ShowIndexPage
from pages.findTeam import ShowFindTeam
from pages.roster import ShowRoster
from pages.depthChart import ShowDepthChart

@app.route('/')
@app.route('/index')
@app.route('/findTeam', methods=['GET', 'POST'])
def findTeam():
    return ShowFindTeam()

@app.route('/<teamName>/roster',methods=['GET'])
def roster(teamName):
    year =request.args.get("year")
    return ShowRoster(teamName,year)

@app.route('/<teamName>/depthChart',methods=['GET'])
def depthChart(teamName):
    year =request.args.get("year")
    return ShowDepthChart(teamName,year)