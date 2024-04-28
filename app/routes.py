from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
import sqlalchemy as sa
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from urllib.parse import urlsplit
from app import db
from app.forms import RegistrationForm
from datetime import datetime, timezone
from app.forms import EditProfileForm
from app.models import RequestLog
from sqlalchemy.engine import Engine
from sqlalchemy import event

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/roster')
@login_required
def roster():
    user = {'username': 'Spencer'}
    players = [
        {'Name': 'John Doe', 'Position': 'Catcher', 'GamesPlayed': 50, 'BattingAverage': 0.300, 'OnBasePercentage': 0.400, 'SluggingPercentage': 0.500},
        {'Name': 'Jane Smith', 'Position': 'Shortstop', 'GamesPlayed': 45, 'BattingAverage': 0.280, 'OnBasePercentage': 0.350, 'SluggingPercentage': 0.450},
        {'Name': 'Mike Johnson', 'Position': 'Outfielder', 'GamesPlayed': 55, 'BattingAverage': 0.320, 'OnBasePercentage': 0.420, 'SluggingPercentage': 0.550}
    ]
    pitchers = [
        {'Name': 'Jake Anderson', 'GamesPitched': 30, 'GamesStarted': 25, 'InningsPitched': 150, 'WHIP': 1.20, 'StrikeoutsPer9': 8.5},
        {'Name': 'Sarah Brown', 'GamesPitched': 35, 'GamesStarted': 30, 'InningsPitched': 170, 'WHIP': 1.15, 'StrikeoutsPer9': 9.0}
    ]
    team ={
            'team': 'New York Yankees',
            'record': '72-9',
            'year': '2020'
        }
    return render_template('roster.html', title='Roster', user=user, players=players, pitchers=pitchers, team=team)

@app.route('/player/<int:player_id>')
@login_required
def player_stats(player_id):
    user = {'username': 'Spencer'}
    players = [
        {'player_id': 1, 'Name': 'John', 'Position': 'Catcher', 'GamesPlayed': 50, 'BattingAverage': 0.300, 'OnBasePercentage': 0.400, 'SluggingPercentage': 0.500},
        {'player_id': 2, 'Name': 'Jane Smith', 'Position': 'Shortstop', 'GamesPlayed': 45, 'BattingAverage': 0.280, 'OnBasePercentage': 0.350, 'SluggingPercentage': 0.450},
        {'player_id': 3, 'Name': 'Mike Johnson', 'Position': 'Outfielder', 'GamesPlayed': 55, 'BattingAverage': 0.320, 'OnBasePercentage': 0.420, 'SluggingPercentage': 0.550}
    ]
    pitchers = [
        {'player_id': 4, 'Name': 'Jake Anderson', 'GamesPitched': 30, 'GamesStarted': 25, 'InningsPitched': 150, 'WHIP': 1.20, 'StrikeoutsPer9': 8.5},
        {'player_id': 5, 'Name': 'Sarah Brown', 'GamesPitched': 35, 'GamesStarted': 30, 'InningsPitched': 170, 'WHIP': 1.15, 'StrikeoutsPer9': 9.0}
    ]
    team = {
        'team': 'New York Yankees',
        'record': '72-9',
        'year': '2020'
    }
    # Find the player in the list based on the player_id parameter
    selected_player = next((player for player in players if player['player_id'] == player_id), None)

    if selected_player:
        return render_template('player.html', title=f"Player ID {player_id}'s Stats", user=user, player=selected_player, team=team)
    else:
        return "Player not found", 404

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


@app.before_request
def before_request():
    # Check if the current request is for logging SQL queries
    if request.endpoint == 'log_sql_queries':
        return

    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

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

    if user_id:
        # Fetch request logs for a specific user_id
        select_query = sa.select(RequestLog).where(RequestLog.user_id == user_id)
        user_id_exists = True
    else:
        # Fetch all request logs from the database if user_id is not provided
        select_query = sa.select(RequestLog)
        user_id_exists = False

    result = db.session.execute(select_query)
    request_logs = []

    for row in result:
        # Extract the first element of the tuple (which is a RequestLog instance)
        request_log = row[0]
        request_logs.append(request_log)

    # Render the template with the request logs and user_id_exists flag
    return render_template('admin_request_logs.html', request_logs=request_logs, user_id=user_id,
                           user_id_exists=user_id_exists)

    # # Render the template with the request logs
    # return render_template('admin_request_logs.html', request_logs=request_logs, user_id=user_id)


# def log_request(user_id, request_data):
#     # Create a new log entry
#     log_entry = RequestLog(user_id=user_id,
#                            timestamp=datetime.datetime.utcnow(),
#                            request_data=str(request_data))
#     # Add the log entry to the database session
#     db.session.add(log_entry)
#     # Commit the transaction to save the log entry
#     db.session.commit()

@app.before_request
def log_request():
    # Check if the current request is for logging SQL queries
    if request.endpoint == 'log_sql_queries':
        return

    # Retrieve user_id if the user is authenticated
    user_id = current_user.id if current_user.is_authenticated else None

    # Construct the request data string
    request_data = (
        f"Method: {request.method}\n"
        f"Path: {request.path}\n"
        f"Args: {request.args}\n"
        f"Form: {request.form}\n"
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
    # Retrieve user_id if the user is authenticated
    user_id = current_user.id if current_user.is_authenticated else None

    # Construct the request data string
    request_data = (
        f"Method: {request.method}\n"
        f"Path: {request.path}\n"
        # f"Args: {request.args}\n"
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
    log_sql_queries(statement, current_user)