import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RECAPTCHA_PUBLIC_KEY = '6LdFYYkUAAAAAIVJudj34uZDRWrcf5-1ZnYuxQ0M'
    RECAPTCHA_PRIVATE_KEY = '6LdFYYkUAAAAAAZ5TOPD49ahyw-r3NfAZVeS5U73'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'autosecuremail@gmail.com'
    MAIL_PASSWORD = 'project2019secure'
    ADMINS = 'autosecuremail@gmail.com'
    UPLOAD_PATH = os.getcwd() #to change off debug
