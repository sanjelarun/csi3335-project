from wtforms import SelectField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import Users

class FindTeam(FlaskForm):
    year = SelectField('Year',choices=[], validators=[DataRequired()],id="year-dropdown")
    team = SelectField('Team Name', choices=[],validators=[DataRequired()],validate_choice=False,id="team-dropdown")
    submit = SubmitField('Find Team Roster')

class ImmaculateGridInput(FlaskForm):
    url = StringField('Immaculate Grid URL',validators=[DataRequired()])
    submit = SubmitField('Calculate Solution')
    solveCheckbox = BooleanField('Optimal Solution')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(Users).where(
            Users.u_USER == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(Users).where(
            Users.u_EMAIL == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')