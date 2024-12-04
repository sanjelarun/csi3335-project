from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from app.models import Users
from app.forms import RegistrationForm
from app import db

def ShowRegister():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(u_USER=form.username.data, u_EMAIL=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)