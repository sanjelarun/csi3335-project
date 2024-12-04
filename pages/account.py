from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import Users
from app.forms import FindTeam, LoginForm, RegistrationForm
from app import db

def getUsers():
    if not current_user.u_ADMIN:
        return redirect(url_for('main.index'))

    users = Users.query.filter(Users.u_USER != 'admin').all()
    return render_template('users.html', users=users)

def getLogin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(u_USER=form.username.data).first()
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

def getRegister():
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

def getLogout():
    logout_user()
    return redirect(url_for('main.login'))

def getEnsureAdmin():
    def ensure_admin():
        print(f"Ensuring admin... Current app: {current_app}")

        if not hasattr(current_app, 'admin_checked') or not current_app.admin_checked:
            print("Checking for admin user...")
            current_app.admin_checked = True

            # Check if admin exists
            admin_user = Users.query.filter_by(u_ADMIN=True).first()
            if admin_user:
                print("Admin user already exists.")
            else:
                print("No admin user found. Creating one...")
                admin = Users(
                    u_USER="admin",
                    u_EMAIL="admin@email.com",
                    u_PASSHASH=generate_password_hash("password"),
                    u_ADMIN=True,
                    u_ACTIVE=True
                )
                db.session.add(admin)
                try:
                    db.session.commit()
                    print("Admin user successfully created.")
                except Exception as e:
                    print(f"Error while committing admin user: {e}")
                    db.session.rollback()

def getToggleUser(user_id):
    if not current_user.u_ADMIN:
        return redirect(url_for('main.index'))

    user = Users.query.get_or_404(user_id)
    user.u_ACTIVE = not user.u_ACTIVE
    db.session.commit()
    status = "activated" if user.u_ACTIVE else "deactivated"
    flash(f"User {user.u_USER} has been {status}.")
    return redirect(url_for('main.users'))