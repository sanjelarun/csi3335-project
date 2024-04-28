from sqlalchemy.exc import NoResultFound

from sqlalchemy.dialects.mysql import pymysql
from datetime import datetime, timezone
from urllib.parse import urlsplit

from app import app
from app.dbInteract import getPlayerBattingInfo, getPlayerFieldingInfo, getPlayerPitchingInfo, getTeamInfo
from app.forms import LoginForm
import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user
from flask_login import login_required
from flask_login import logout_user

from app import app
from app import db
from app.dbInteract import *
from app.forms import EditProfileForm
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import RequestLog
from sqlalchemy.engine import Engine
from sqlalchemy import event
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/roster/<teamid>/<yearid>')
@login_required
def roster(teamid, yearid):
    team_info = getTeamInfo(teamid, yearid)
    battingRoster = getBattingInfoByTeamIDandYearID(teamid, yearid)
    return render_template('roster.html', title='Roster', user=user, team=team_info, battingRoster=battingRoster, yearid=yearid)

@app.route('/player/<player_id>')
@login_required
def player_stats(player_id):
    # player_id="aardsda01"
    player_name = getName(player_id)
    batting_info = getPlayerBattingInfo(player_id)
    pitching_info = getPlayerPitchingInfo(player_id)
    fielding_info = getPlayerFieldingInfo(player_id)
    return render_template('player.html', player_id=player_id, batting=batting_info, pitching=pitching_info,
                           fielding=fielding_info, player=player_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))

    return render_template('user.html', user=user)


# @app.before_request
# def before_request():
#     # Check if the current request is for logging SQL queries
#     if request.endpoint == 'log_sql_queries':
#         return
#
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.now(timezone.utc)
#         db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    teams = [('Team A', 'Team A'), ('Team B', 'Team B'), ('Team C', 'Team C')]

    form.favorite_team.choices = teams

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.favorite_team = form.favorite_team.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.favorite_team.data = current_user.favorite_team
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/admin/request_logs')
@login_required
def admin_request_logs():
    if not current_user.is_admin:
        # Optionally, you can handle non-admin access here
        return "Access denied. Only admins are allowed to view this page."

    user_id = request.args.get('user_id')
    show_all = request.args.get('show_all')  # Check if "Show All Requests" button is clicked

    username = None  # Initialize username variable

    if user_id:
        try:
            # Check if the user_id exists in the database
            user = User.query.filter_by(id=user_id).one()
            user_id_exists = True

            # Get the username associated with the user_id
            username = user.username

            # Log the query
            log_sql_queries(str(User.query.filter_by(id=user_id).statement), current_user)

        except NoResultFound:
            # If user_id does not exist, set user_id_exists to False
            user_id_exists = False

        if user_id_exists:
            # Fetch request logs for the specific user_id
            select_query = sa.select(RequestLog).where(RequestLog.user_id == user_id)
        else:
            # Fetch all request logs from the database if user_id does not exist
            select_query = sa.select(RequestLog)
    elif show_all == 'true':  # Handle the case when "Show All Requests" button is clicked
        # Fetch all request logs from the database
        select_query = sa.select(RequestLog)
        user_id_exists = False
    else:
        # Fetch all request logs from the database if user_id is not provided
        select_query = sa.select(RequestLog)
        user_id_exists = False



    # # Handle sorting based on the provided sort order
    # if sort_order == 'timestamp_asc':
    #     select_query = select_query.order_by(RequestLog.timestamp.asc())
    # elif sort_order == 'timestamp_desc':
    #     select_query = select_query.order_by(RequestLog.timestamp.desc())

    # Log the query
    log_sql_queries(select_query, current_user)

    result = db.session.execute(select_query)
    request_logs = []

    for row in result:
        # Extract the first element of the tuple (which is a RequestLog instance)
        request_log = row[0]
        request_logs.append(request_log)

    # Retrieve usernames based on request_log IDs
    user_ids = [log.user_id for log in request_logs]
    user_id_to_username = {user.id: user.username for user in User.query.filter(User.id.in_(user_ids)).all()}

    # Map usernames to request_logs
    for log in request_logs:
        log.username = user_id_to_username.get(log.user_id)

    # Render the template with the request logs and user_id_exists flag
    return render_template('admin_request_logs.html', request_logs=request_logs, user_id=user_id,
                           user_id_exists=user_id_exists, show_all=show_all, username=username)

@app.before_request
def log_request():
    # Check if the current request is for logging SQL queries or during logout
    if request.endpoint == 'log_sql_queries' or request.endpoint == 'logout' or request.endpoint == 'login' or request.endpoint == 'index' or request.endpoint == 'register':
        return

    # Retrieve user_id if the user is authenticated
    user_id = current_user.id if current_user.is_authenticated else None

    current_user.last_seen = datetime.now(timezone.utc)

    # Construct the request data string
    request_data = (
        f"Method: {request.method}\n"
        f"Path: {request.path}\n"
        f"Args: {request.args}\n"
        # f"Form: {request.form}\n"
        f"Headers: {dict(request.headers)}\n"
        f"Remote Addr: {request.remote_addr}\n"
    )
    # Log the request
    log_entry = RequestLog(user_id=user_id,
                           timestamp=datetime.now(timezone.utc),
                           request_data=request_data)
    # Add the log entry to the database session
    db.session.add(log_entry)
    # Commit the transaction to save the log entry
    db.session.commit()






# Define a function to log SQL queries
def log_sql_queries(sql, current_user):
    # List of endpoints where user_id should not be extracted
    excluded_endpoints = ['log_sql_queries'] #, 'logout', 'login', 'index', 'register']

    # Check if the current request is for logging SQL queries or excluded endpoints
    if request.endpoint in excluded_endpoints:
        return

    # Set user_id to None by default
    user_id = None

    # Set user_id for authenticated users
    if current_user.is_authenticated:
        user_id = current_user.id


    # Construct the request data string
    request_data = (
        f"Method: {request.method}\n"
        f"Path: {request.path}\n"
        f"Args: {request.args}\n"
        # f"Form: {request.form}\n"
        # f"Headers: {dict(request.headers)}\n"
        # f"Remote Addr: {request.remote_addr}\n"
        f"SQL Query: {sql}\n"
    )

    # Log the request
    log_entry = RequestLog(user_id=user_id,
                           timestamp=datetime.now(timezone.utc),
                           request_data=request_data)

    # Add the log entry to the database session
    db.session.add(log_entry)
    # Commit the transaction to save the log entry
    db.session.commit()



# Register the event listener to log SQL queries
@event.listens_for(Engine, "before_cursor_execute", once=True)
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if request.method == 'GET':
        log_sql_queries(statement, current_user)

@event.listens_for(Engine, "after_cursor_execute", once=True)
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if request.method == 'POST':
        log_sql_queries(statement, current_user)