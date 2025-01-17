from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
import os
import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail


app = Flask(__name__)
app.secret_key = os.urandom(24)
Bootstrap(app)
FontAwesome(app)

app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)
from app.authentication import bp as authentication_bp
app.register_blueprint(authentication_bp)
from app.fileModification import bp as fileModification_bp
app.register_blueprint(fileModification_bp)
from app.fileDownload import bp as fileDownload_bp
app.register_blueprint(fileDownload_bp)

from app import routes, models
from app.models import Folder

app.debug = False

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
