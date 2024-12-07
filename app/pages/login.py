from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

from app.models import Users
from app.forms import LoginForm
from app import db

def ShowLogin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(Users).filter_by(u_USER=form.username.data).first()
        if user is None or not check_password_hash(user.u_PASSHASH, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))

        if not user.is_active:
            flash('Your account has been deactivated.')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))

    return render_template('login.html', form=form, title='Login')