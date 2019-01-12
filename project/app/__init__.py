from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome


app = Flask(__name__)
Bootstrap(app)

fa = FontAwesome(app)

app.config.from_object(Config)
app.debug = True
db = SQLAlchemy(app)
app.debug = True

migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
from app import routes, models