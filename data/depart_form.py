from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, StringField
from wtforms.validators import DataRequired


class AddDepartForm(FlaskForm):
    title = StringField('Department Title', validators=[DataRequired()])
    chief = IntegerField('Chief ID', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = StringField('Department Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
