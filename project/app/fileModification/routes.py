import os

from app import app, db
from app.models import User, File, Folder
from app.email import send_password_reset_email
from app.functions.path import returnPathOfFile
from app.fileModification.forms import UploadForm, UploadDirectoryForm
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from datetime import timedelta
from uuid import uuid4
from app.routes import currentPath
from app.functions.path import returnPathOfFile, returnPathOfFolder
import os, random, struct
import cryptography
from cryptography.fernet import Fernet

import shutil

app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/upload/<path>')
@login_required
def upload(path):
    return render_template('fileModification/upload.html', title='Upload file', path=path)

@app.route('/upload_normal_file/<path>', methods=['POST','GET'])
@login_required
def upload_normal_file(path):
    form = UploadForm()
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        f = request.files['upload']
        currentFolder = Folder.query.filter_by(id=path).one()
        fileDb = File(name=f.filename, parent=currentFolder, AccessFile=[user])
        db.session.add(fileDb)
        path = returnPathOfFolder(currentFolder.id)
        name = f.filename
        files = f.read()
        fernet = Fernet(app.config["EKEY"])
        print(app.config["EKEY"])
        encrypted = fernet.encrypt(files)
        with open(os.path.join(path,name), 'wb') as fa:
            fa.write(encrypted)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('fileModification/upload_normal/upload_normal_file.html', title='Upload Normal file', form=form, path=path)

@app.route('/upload_group_file/<path>',methods=['POST','GET'])
@login_required
def upload_group_file(path):
    form = UploadForm()
    return render_template('fileModification/upload_group/upload_group_file.html', title='Upload Group File', form=form, path=path)

@app.route('/upload_normal_directory/<path>', methods=['POST','GET'])
@login_required
def upload_normal_directory(path):
    form = UploadDirectoryForm()
    if form.validate_on_submit():
        uploaded_files = request.files.getlist("files")
        for f in uploaded_files:
            currentFolder = Folder.query.filter_by(id=path).one()
            f.save(os.path.join(returnPathOfFolder(currentFolder.id), currentFolder.name, secure_filename(f.filename)))
        return redirect(url_for('index'))
    return render_template('fileModification/upload_normal/upload_normal_directory.html', title='Upload Normal file', form=form, path=path)


@app.route('/upload_group_directory/<path>', methods=['POST','GET'])
@login_required
def upload_group_directory(path):
    form = UploadForm()
    return render_template('fileModification/upload_group/upload_group_directory.html', title='Upload Group Directory', form=form, path=path)

@app.route('/deleter/file/<id>', methods=['POST', 'GET'])
@login_required
def deleteFile(id):
    f = File.query.filter_by(id=id).one()
    print(f.parent.name)
    filePath = returnPathOfFile(id)
    db.session.delete(f)
    os.remove(filePath)
    db.session.commit()
    flash(f.name + " has been deleted correctly")
    return redirect(url_for("currentPath", path=f.parent.id))


@app.route('/deleter/folder/<id>', methods=['POST', 'GET'])
@login_required
def deleteFolder(id):
    f = Folder.query.filter_by(id=id).one()
    for subf in f.subFolders:
        deleteFolder(subf.id)
    for subf in f.subFiles:
        deleteFile(subf.id)
    folderPath = returnPathOfFolder(id)
    print(folderPath)
    os.rmdir(folderPath)
    db.session.delete(f)
    db.session.commit()
    flash(f.name + " has been deleted correctly")
    return redirect(url_for("currentPath", path=f.parent.id))
