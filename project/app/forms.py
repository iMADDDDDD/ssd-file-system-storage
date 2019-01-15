from app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class CreateFolder(FlaskForm):
    folderName = StringField('Folder name', validators=[DataRequired()])
    submit = SubmitField('New Folder')