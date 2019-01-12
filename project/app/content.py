from app import app, db
import os
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, File


@app.route('/content')
@login_required
def content():
    user = current_user
    files = File.query.all()
    return render_template('content.html', title="Content", user=user, files=files)

