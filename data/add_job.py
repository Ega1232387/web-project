from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, StringField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название', validators=[DataRequired()])
    work_size = StringField('Объём Работы', validators=[DataRequired()])
    department = SelectField('Раздел', choices=[(2, 'Текст'), (3, 'Текстуры')])
    category = SelectField('Сложность', choices=[(1, 'Лёгкая'), (2, 'Средняя'), (3, 'Сложная')])
    file = FileField('Файл', validators=[FileRequired()])
    is_finished = BooleanField('Работа Завершена?')

    submit = SubmitField('Принять')
