import enum
from datetime import datetime
from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt


class Role(enum.Enum):
    user = 1
    admin = 2

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashPassword = db.Column(db.String(128))
    role = db.Column(db.Enum(Role))
    creationDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    locked = db.Column(db.Boolean)
    failedLogin = db.Column(db.Integer, default=0)
    logs = db.relationship('Log', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.hashPassword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashPassword, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Log(db.Model):
    __tablename__ = 'Log'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return '<Log {}>'.format(self.date)


AccessFolder = db.Table('AccessFolder',
    db.Column('userId', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('folderId', db.Integer, db.ForeignKey('Folder.id'), primary_key=True)
)


class Folder(db.Model):
    __tablename__ = 'Folder'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    creationDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    folderId = db.Column(db.Integer, db.ForeignKey('Folder.id'), nullable=False)
    subFiles = db.relationship('File', backref='parent', lazy='dynamic')
    subFolders = db.relationship("Folder", remote_side=[id], backref='parent')
    AccessFolder = db.relationship('User', secondary=AccessFolder, lazy='dynamic',
        backref=db.backref('folders', lazy=True))

    def __repr__(self):
        return '<Folder {}>'.format(self.name)


AccessFile = db.Table('AccessFile',
    db.Column('userId', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('fileId', db.Integer, db.ForeignKey('File.id'), primary_key=True)
)


class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    path = db.Column(db.String(128))
    size = db.Column(db.Integer)
    folderId = db.Column(db.Integer, db.ForeignKey('Folder.id'), nullable=False)
    creationDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    AccessFile = db.relationship('User', secondary=AccessFile, lazy='dynamic',
        backref=db.backref('files', lazy=True))

    def __repr__(self):
        return '<File {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))