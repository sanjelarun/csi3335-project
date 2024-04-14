from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from urllib.parse import urlsplit
from app import db
from app.forms import RegistrationForm

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
