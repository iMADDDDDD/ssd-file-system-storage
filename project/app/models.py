import enum
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Role(enum.Enum):
    user = 1
    admin = 2

class User(UserMixin, db.Model):
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

class Log(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    creationDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    subFiles = db.relationship('File', backref='parent', lazy='dynamic')
    subFolders = db.relationship("Folder", backref='parent', lazy='dynamic')
    AccessFolder = db.relationship('User', secondary=AccessFolder, lazy='dynamic',
        backref=db.backref('folders', lazy=True))

    def __repr__(self):
        return '<Folder {}>'.format(self.name)

AccessFile = db.Table('AccessFile',
    db.Column('userId', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('fileId', db.Integer, db.ForeignKey('File.id'), primary_key=True)
)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    path = db.Column(db.String(128))
    size = db.Column(db.Integer)
    creationDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    AccessFile = db.relationship('User', secondary=AccessFile, lazy='dynamic',
        backref=db.backref('files', lazy=True))

    def __repr__(self):
        return '<File {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))