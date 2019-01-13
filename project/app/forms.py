from app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

app.config['RECAPTCHA_PUBLIC_KEY'] ='6LdFYYkUAAAAAIVJudj34uZDRWrcf5-1ZnYuxQ0M'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdFYYkUAAAAAAZ5TOPD49ahyw-r3NfAZVeS5U73'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class DeletionForm(FlaskForm):
    filename = SelectField('filename', coerce=int, choices=[(1,"no files")])
    submit = SubmitField('Delete')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')