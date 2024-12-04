from flask import render_template, redirect, url_for, flash, current_app
from flask_login import current_user
from werkzeug.security import generate_password_hash

from app.models import Users
from app import db

def getUsers():
    if not current_user.u_ADMIN:
        return redirect(url_for('main.index'))

    users = Users.query.filter(Users.u_USER != 'admin').all()
    return render_template('users.html', users=users)

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

def ShowToggleUser(user_id):
    if not current_user.u_ADMIN:
        return redirect(url_for('main.index'))

    user = Users.query.get_or_404(user_id)
    user.u_ACTIVE = not user.u_ACTIVE
    db.session.commit()
    status = "activated" if user.u_ACTIVE else "deactivated"
    flash(f"User {user.u_USER} has been {status}.")
    return redirect(url_for('main.users'))