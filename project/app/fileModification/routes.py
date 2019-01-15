from app import app, db
from app.models import User, File, Folder
from app.email import send_password_reset_email
import os
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from datetime import timedelta
from uuid import uuid4
from app.routes import currentPath

app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/upload')
@login_required
def upload():
    return render_template('authenticated/upload.html')

@app.route('/uploader', methods = ['POST', 'GET'])
@login_required
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        user = User.query.filter_by(username="admin").first()
        newfile = File(filename=f.filename, author=user)
        db.session.add(newfile)
        db.session.commit()
        flash('File uploaded successfully')
        return render_template('authenticated/upload.html')

@app.route('/deleter/file/<id>', methods=['POST', 'GET'])
@login_required
def deleteFile(id):
	f = File.query.filter_by(id=id).one()
	print(f.parent.name)
	db.session.delete(f)
	db.session.commit()
	flash(f.name + " has been delete correctly")
	return redirect("index") + f.parent.name

@app.route('/deleter/folder/<id>', methods=['POST', 'GET'])
@login_required
def deleteFolder(id):
	f = Folder.query.filter_by(id=id).one()
	db.session.delete(f)
	db.session.commit()
	flash(f.name + " has been delete correctly")
	return redirect("index") + f.parent.name
