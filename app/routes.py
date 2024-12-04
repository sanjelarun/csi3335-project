from flask import Blueprint, redirect, url_for
from flask_login import login_required

from pages.account import getLogin, getRegister, getLogout, getEnsureAdmin, getUsers, getToggleUser
from pages.immaculateGrid import getImmaculateGrid
from pages.playerCharts import getDepthChart, getRoster, getTeams, getShowFindTeam


bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return redirect(url_for('main.ShowFindTeam'))

@bp.route('/findTeam', methods=['GET', 'POST'])
@login_required
def ShowFindTeam():
    return getShowFindTeam()

@bp.route('/get_teams/<int:year_id>', methods=['GET'])
@login_required
def get_teams(year_id):
    return getTeams(year_id)

@bp.route('/<teamId>/roster', methods=['GET'])
@login_required
def roster(teamId):
    return getRoster(teamId)

@bp.route('/<teamId>/depthChart', methods=['GET'])
@login_required
def depthChart(teamId):
    return getDepthChart(teamId)

@bp.route('/immaculateGrid', methods=['GET', 'POST'])
@login_required
def immaculateGrid():
    return getImmaculateGrid()

@bp.route('/users', methods=['GET'])
@login_required
def users():
    return getUsers()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return getLogin()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    return getRegister()

@bp.route('/logout')
def logout():
    return getLogout()

@bp.route('/toggle_user/<int:user_id>', methods=['POST'])
@login_required
def toggle_user(user_id):
    return getToggleUser(user_id)

@bp.before_request
def ensure_admin():
    getEnsureAdmin()