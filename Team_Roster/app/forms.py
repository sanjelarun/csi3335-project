from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class FindTeam(FlaskForm):
    year = SelectField('Year',choices=[], validators=[DataRequired()],id="year-dropdown")
    team = SelectField('Team Name', choices=[],validators=[DataRequired()],validate_choice=False,id="team-dropdown")

    submit = SubmitField('Find Team Roster')

class ImmaculateGridInput(FlaskForm):
    url = StringField('Immaculate Grid URL',validators=[DataRequired()])
    submit = SubmitField('Calculate Solution')
