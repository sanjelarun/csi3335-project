from app import app
from app.dbInteract import getPlayerBattingInfo
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

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

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

    players = [
        {'player_id': 1, 'Name': 'John', 'Position': 'Catcher', 'GamesPlayed': 50, 'BattingAverage': 0.300, 'OnBasePercentage': 0.400, 'SluggingPercentage': 0.500},
        {'player_id': 2, 'Name': 'Jane Smith', 'Position': 'Shortstop', 'GamesPlayed': 45, 'BattingAverage': 0.280, 'OnBasePercentage': 0.350, 'SluggingPercentage': 0.450},
        {'player_id': 3, 'Name': 'Mike Johnson', 'Position': 'Outfielder', 'GamesPlayed': 55, 'BattingAverage': 0.320, 'OnBasePercentage': 0.420, 'SluggingPercentage': 0.550}
    ]
    
    # Fetch player info based on player_id
    selected_player = next((player for player in players if player['player_id'] == player_id), None)

    if selected_player:
        # Call getPlayerBattingInfo to get batting data
        batting_info = getPlayerBattingInfo(str(player_id))

        # Render the template with player and batting info
        return render_template('player.html', title=f"Player ID {player_id}'s Stats", user=user, player=selected_player, team=team, batting=batting_info)
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
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    form = EditProfileForm(current_user.username)

    teams = [('0', 'Team A'), ('1', 'Team B'), ('2', 'Team C')]

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



def log_request(user_id, request_data):
    # Create a new log entry
    log_entry = RequestLog(user_id=user_id,
                           timestamp=datetime.datetime.utcnow(),
                           request_data=str(request_data))
    # Add the log entry to the database session
    db.session.add(log_entry)
    # Commit the transaction to save the log entry
    db.session.commit()