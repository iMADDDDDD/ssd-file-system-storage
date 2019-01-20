import os

from app import app, db
from app.models import User, File, Folder
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
    return redirect(url_for("currentPath", path="Files"))


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
        dirName = form.folderName.data
        # TODO use the function to get the absolute path
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            flash("Directory " + form.folderName.data + " Created ")
        else:
            flash("Directory " + form.folderName.data + " already exists")
            return redirect(url_for("currentPath", title="Home", path=currentFolder.name))
        newFolder = Folder(name=form.folderName.data, parent=currentFolder)
        newFolder.AccessFolder.append(user)
        db.session.add(newFolder)
        db.session.commit()
        return redirect(url_for("currentPath", title="Home", path=currentFolder.name))
    return render_template('home/home.html', title="Home", user=user, files=files, folders=folders, form=form, parent=currentFolder.parent, path=path)
