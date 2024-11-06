from flask import render_template, flash, redirect, request

from app import app
from app.forms import FindTeam

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Immaculate Party Time'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/findTeam', methods=['GET', 'POST'])
def login():
    form = FindTeam()
    if form.validate_on_submit():
        flash('Trying to find team {} at year {}'.format(
            form.teamName.data, form.year.data))
        return redirect('/{}/roster?year={}'.format(form.teamName.data,form.year.data))
    return render_template('findTeam.html', title='Find Team', form=form)

@app.route('/<team>/roster',methods=['GET'])
def roster(team):
    print(request.data)
    year =request.args.get("year")
    return render_template('roster.html', title="{}'s Roster".format(team), team=team, year=year)