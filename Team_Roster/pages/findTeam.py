from app.forms import FindTeam
from flask import render_template, redirect


def ShowFindTeam():
    form = FindTeam()
    if form.validate_on_submit():
        return redirect('/{}/roster?year={}'.format(form.teamName.data,form.year.data))
    return render_template('findTeam.html', title='Find Team', form=form)