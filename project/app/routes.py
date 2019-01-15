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

app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user
    files = File.query.all()
    files.append(Folder.query.all())
    return render_template('index.html', title="Home", user=user, files=files)

@app.route('/content')
@login_required
def content():
    user = current_user
    files = File.query.all()
    return render_template('content.html', title="Content", user=user, files=files)