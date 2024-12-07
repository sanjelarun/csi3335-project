from flask import redirect, url_for
from flask_login import logout_user

def ShowLogout():
    logout_user()
    return redirect(url_for('main.login'))