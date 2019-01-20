import os
import sys

from app import app, db
from app.models import User, File, Folder, Role
from app.email import send_password_reset_email
from app.forms import CreateFolder
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from datetime import timedelta
from uuid import uuid4

app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    user = User.query.get(current_user.id)
    role = user.role

    if role == Role.admin:
        return redirect(url_for("admin"))
    return redirect(url_for("currentPath", path="Files"))

@app.route('/a/profile/<id>')
@login_required
def profile(id):
    user = User.query.filter_by(id=id).first()
    files = user.files
    folders = user.folders
    return render_template('/a/profile.html', title="Administration control panel", user=user, files=files, folders=folders)


@app.route('/a/unlock_user/<id>')
@login_required
def unlock_user(id):
    user = User.query.filter_by(id=id).first()
    user.locked = False
    db.session.add(user)
    db.session.commit()
    flash('User has been unlocked')
    return redirect(url_for("profile", id=user.id))

@app.route('/a/activate_user/<id>')
@login_required
def activate_user(id):
    user = User.query.filter_by(id=id).first()
    user.activated = True
    db.session.add(user)
    db.session.commit()
    flash('User account has been activated')
    return redirect(url_for("profile", id=user.id))

@app.route('/a/deactivate_user/<id>')
@login_required
def deactivate_user(id):
    user = User.query.filter_by(id=id).first()
    user.activated = False
    db.session.add(user)
    db.session.commit()
    flash('User account has been deactivated')
    return redirect(url_for("profile", id=user.id))


@app.route('/a/index')
@login_required
def admin():
    admin = current_user
    locked_users = User.query.filter_by(locked=True).all()
    non_activated_users = User.query.filter_by(activated=False).all()

    return render_template('/a/index.html', title="Administration control panel", admin=admin, locked_users=locked_users,
    non_activated_users=non_activated_users)

@app.route('/a/users')
@login_required
def users():
    users = User.query.order_by(User.id).all()
    files = File.query.all()
    folders = Folder.query.all()

    return render_template('/a/users.html', users=users, files=files, folders=folders)

@app.route('/index/<path>', methods=['POST', 'GET'])
@login_required
def currentPath(path):
    form = CreateFolder()
    user = User.query.get(current_user.id)
    files = user.files
    indexToSuppress = []
    currentFolder = Folder.query.filter_by(name=path).first()
    for i in range(len(files)):
        f = files[i]
        if f.parent.name != path:
            indexToSuppress.append(i)
    for i in range(len(indexToSuppress)):
        files.pop(indexToSuppress[i] - i)
    folders = user.folders
    indexToSuppress = []
    for i in range(len(folders)):
        f = folders[i]
        if f.parent.name != path:
            indexToSuppress.append(i)
    for i in range(len(indexToSuppress)):
        folders.pop(indexToSuppress[i] - i)
    if form.validate_on_submit():
        # Create target Directory if don't exist

        dirName = os.path.abspath(currentFolder.name) + "/" + form.folderName.name
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            flash("Directory " , dirName ,  " Created ")
        else:
            flash("Directory " , dirName ,  " already exists")
        newFolder = Folder(name=form.folderName.data, parent=currentFolder)
        newFolder.AccessFolder.append(user)
        db.session.add(newFolder)
        db.session.commit()
        return redirect(url_for("currentPath", title="Home", path=currentFolder.name))
    return render_template('home/home.html', title="Home", user=user, files=files, folders=folders, form=form, parent=currentFolder.parent, path=path)
