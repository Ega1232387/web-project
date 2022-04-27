from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, StringField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('Логин/Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторить Пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    department = SelectField('Раздел', choices=[(2, 'Текст'), (2, 'Текстуры'), (3, 'Текст и Текстуры')])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Принять')
