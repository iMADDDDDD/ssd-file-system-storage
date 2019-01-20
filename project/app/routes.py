import os
import sys
from copy import deepcopy
from app.functions.path import returnPathOfFile, returnPathOfFolder
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
    return redirect(url_for("currentPath", path=1)) # Verify that "Files" has for id 1

@app.route('/a/profile/<id>')
@login_required
def profile(id):
    user = User.query.filter_by(id=id).first()
    files = user.files
    folders = user.folders
    role = user.role
    if role != Role.admin:
        return redirect(url_for("index"))
    return render_template('/a/profile.html', title="Administration control panel", user=user, files=files, folders=folders)


@app.route('/a/unlock_user/<id>')
@login_required
def unlock_user(id):
    user = User.query.filter_by(id=id).first()
    role = user.role
    if role != Role.admin:
        return redirect(url_for("index"))

    user.locked = False
    db.session.add(user)
    db.session.commit()
    flash('User has been unlocked')
    return redirect(url_for("profile", id=user.id))

@app.route('/a/activate_user/<id>')
@login_required
def activate_user(id):
    user = User.query.filter_by(id=id).first()
    role = user.role
    if role != Role.admin:
        return redirect(url_for("index"))

    user.activated = True
    db.session.add(user)
    db.session.commit()
    flash('User account has been activated')
    return redirect(url_for("profile", id=user.id))

@app.route('/a/deactivate_user/<id>')
@login_required
def deactivate_user(id):
    user = User.query.filter_by(id=id).first()
    role = user.role
    if role != Role.admin:
        return redirect(url_for("index"))

    user.activated = False
    db.session.add(user)
    db.session.commit()
    flash('User account has been deactivated')
    return redirect(url_for("profile", id=user.id))


@app.route('/a/index')
@login_required
def admin():
    role = current_user.role
    if role != Role.admin:
        return redirect(url_for("index"))

    locked_users = User.query.filter_by(locked=True).all()
    non_activated_users = User.query.filter_by(activated=False).all()

    return render_template('/a/index.html', title="Administration control panel", admin=admin, locked_users=locked_users,
    non_activated_users=non_activated_users)

@app.route('/a/users')
@login_required
def users():
    role = current_user.role
    if role != Role.admin:
        return redirect(url_for("index"))
    users = User.query.order_by(User.id).all()
    files = File.query.all()
    folders = Folder.query.all()

    return render_template('/a/users.html', users=users, files=files, folders=folders)

@app.route('/index/<path>', methods=['POST', 'GET'])
@login_required
def currentPath(path):
    form = CreateFolder()
    user = User.query.get(current_user.id)
    indexToSuppress = []
    currentFolder = Folder.query.get(path)
    currentFiles = []
    for i in range(len(user.files)):
        f = user.files[i]
        currentFiles.append(f)
        if f.parent.name != currentFolder.name:
            indexToSuppress.append(i)
    for i in range(len(indexToSuppress)):
        currentFiles.pop(indexToSuppress[i] - i)
    indexToSuppress = []
    currentFolders = []
    for i in range(len(user.folders)):
        f = user.folders[i]
        currentFolders.append(f)
        if f.parent.name != currentFolder.name:
            indexToSuppress.append(i)
    for i in range(len(indexToSuppress)):
        currentFolders.pop(indexToSuppress[i] - i)
    if form.validate_on_submit():
        dirName = returnPathOfFolder(currentFolder.id) + "/" + form.folderName.data
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            flash("Directory " + form.folderName.data +  " Created ")
        else:
            flash("Directory " + form.folderName.data +  " already exists")
        newFolder = Folder(name=form.folderName.data, parent=currentFolder)
        newFolder.AccessFolder.append(user)
        db.session.add(newFolder)
        db.session.commit()
        return redirect(url_for("currentPath", title="Home", path=currentFolder.id))
    return render_template('home/home.html', title="Home", user=user, files=currentFiles, folders=currentFolders, form=form, parent=currentFolder.parent, path=path)
