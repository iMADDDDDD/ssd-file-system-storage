from app import app, db
from app.models import User, File
from app.fileModification.forms import DeletionForm
from app.email import send_password_reset_email
import os
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from datetime import timedelta
from uuid import uuid4

app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['POST'])
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
        return render_template('upload.html')

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeletionForm()
    form.filename.choices = [(int(f.id), f.filename) for f in User.query.filter_by(username='admin').first().files]
    return render_template('delete.html', title='Delete', form=form)

@app.route('/deleter', methods=['POST', 'GET'])
@login_required
def deleter():
    form = DeletionForm()
    if form.validate_on_submit():
        f = File.query.filter_by(id=form.filename.data).first()
        if os.path.exists(f.filename):
            os.remove(f.filename)
            db.session.delete(f)
            db.session.commit()
            return f.filename + " has been deleted correctly"
        else:
            return 'Error'
    return str(form.errors)