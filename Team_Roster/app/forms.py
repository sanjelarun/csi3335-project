from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class FindTeam(FlaskForm):
    team = SelectField('Team Name', choices=[],validators=[DataRequired()]) #Choices set dynamically
    year = IntegerField('Year', validators=[DataRequired()])
    submit = SubmitField('Find Team Roster')