from pages.findTeam import ShowFindTeam
from pages.roster import ShowRoster
from pages.depthChart import ShowDepthChart
from flask import flash, redirect, url_for, render_template, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for('users'))
    return ShowFindTeam()

@app.route('/users', methods=['GET'])
@login_required
def users():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    users = User.query.filter(User.username != 'admin').all()
    return render_template('users.html', users=users)

@app.route('/toggle_user/<int:user_id>', methods=['POST'])
@login_required
def toggle_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))

    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    status = "activated" if user.is_active else "deactivated"
    flash(f"User {user.username} has been {status}.")
    return redirect(url_for('users'))

@app.route('/findTeam', methods=['GET', 'POST'])
@login_required
def findTeam():
    return ShowFindTeam()

@app.route('/<teamId>/roster', methods=['GET'])
@login_required
def roster(teamId):
    year = request.args.get("year")
    return ShowRoster(teamId, year)

@app.route('/<teamId>/depthChart', methods=['GET'])
@login_required
def depthChart(teamId):
    year = request.args.get("year")
    return ShowDepthChart(teamId, year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        # Check if user exists and if the password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        if not user.is_active:
            flash('Your account has been deactivated. Please contact support.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        # Redirect to the next page if specified, otherwise to index
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.before_request
def ensure_admin():
    if not hasattr(app, 'admin_checked'):  # Ensure this logic runs only once
        app.admin_checked = True
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user:
            admin = User(
                username="admin",
                email="admin@email.com",
                password_hash=generate_password_hash("password"),
                is_admin=True,
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()