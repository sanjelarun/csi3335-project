from flask import redirect, url_for, request, jsonify
from flask_login import login_required, current_user

from app.pages.immaculateGrid import ShowImmaculateGrid
from app.pages.depthChart import ShowDepthChart
from app.pages.login import ShowLogin
from app.pages.register import ShowRegister
from app.pages.logout import ShowLogout
from app.pages.admin import getEnsureAdmin, ShowToggleUser, getUsers
from app.pages.roster import ShowRoster
from app.pages.findTeam import ShowFindTeam, getTeams
from app.pages.queries import ShowQueries, DeleteRosterQueries, DeleteImmaculateGridQueries

from flask import Blueprint

# Define the blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return redirect(url_for('main.findTeam'))

@bp.route('/findTeam', methods=['GET', 'POST'])
@login_required
def findTeam():
    return ShowFindTeam()

@bp.route('/get_teams/<int:year_id>', methods=['GET'])
@login_required
def get_teams(year_id):
    return getTeams(year_id)

@bp.route('/<teamId>/roster', methods=['GET'])
@login_required
def roster(teamId):
    return ShowRoster(teamId, request.args.get('year'))

@bp.route('/<teamId>/depthChart', methods=['GET'])
@login_required
def depthChart(teamId):
    return ShowDepthChart(teamId, request.args.get('year'))

@bp.route('/immaculateGrid', methods=['GET', 'POST'])
@login_required
def immaculateGrid():
    return ShowImmaculateGrid()

@bp.route('/users', methods=['GET'])
@login_required
def users():
    return getUsers()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return ShowLogin()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    return ShowRegister()

@bp.route('/logout')
def logout():
    return ShowLogout()

@bp.route('/toggle_user/<int:user_id>', methods=['POST'])
@login_required
def toggle_user(user_id):
    return ShowToggleUser(user_id)

@bp.before_request
def ensure_admin():
    getEnsureAdmin()

@bp.route('/queries', methods=['GET'])
@login_required
def queries():
    return ShowQueries(current_user.get_id())

@bp.route('/clearRosterQueries', methods=['POST'])
@login_required
def clearRosterQueries():
    if request.form.get('_method') == 'DELETE':
        return DeleteRosterQueries(current_user.get_id())

@bp.route('/clearImmaculateGridQueries', methods=['POST'])
@login_required
def clearImmaculateGridQueries():
    if request.form.get('_method') == 'DELETE':
        return DeleteImmaculateGridQueries(current_user.get_id())