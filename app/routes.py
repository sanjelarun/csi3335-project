from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Spencer'},
            'body': 'I really like to think that was a good day!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/roster')
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)