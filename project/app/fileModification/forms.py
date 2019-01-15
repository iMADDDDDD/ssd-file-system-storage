from app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class DeletionForm(FlaskForm):
    filename = SelectField('filename', coerce=int, choices=[(1,"no files")])
    submit = SubmitField('Delete')
