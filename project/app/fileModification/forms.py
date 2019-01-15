from app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField

from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class DeletionForm(FlaskForm):
    filename = SelectField('filename', coerce=int, choices=[(1,"no files")])
    submit = SubmitField('Delete')

class UploadForm(FlaskForm):
    email = StringField('Email', validators=[Email()],render_kw={"placeholder": "example@example.com, ... "})
    submit = SubmitField('Upload')
    upload = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png','txt'], 'Valid file types only!')
    ])
