from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired
import datetime


class JobsForm(FlaskForm):
    description = TextAreaField('Job title')
    team_leader_id = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Work_size', validators=[DataRequired()])
    start_date = DateField('Дата начала работы', validators=[DataRequired()], default=datetime.datetime.now())
    collaborators = StringField('Collaborators',validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')
