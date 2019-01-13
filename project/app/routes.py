from app import app, db
from app.models import User, File
from app.forms import LoginForm, RegistrationForm, DeletionForm, ResetPasswordRequestForm, ResetPasswordForm
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
    return render_template('index.html', title="Home", user=user, files=files)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        session['logged_in'] = True
        session['number'] = str(uuid4())
        session.permanent = True
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        return render_template('login.html')
    logout_user()
    return redirect(url_for('index'))


@app.route('/upload')
def upload():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('upload.html')


@app.route('/uploader', methods = ['POST'])
def uploader():
    if not session.get('logged_in'):
        return render_template('login.html')
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        user = User.query.filter_by(username="admin").first()
        newfile = File(filename=f.filename, author=user)
        db.session.add(newfile)
        db.session.commit()
        flash('File uploaded successfully')
        return render_template('upload.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if not session.get('logged_in'):
        return render_template('login.html')
    form = DeletionForm()
    form.filename.choices = [(int(f.id), f.filename) for f in User.query.filter_by(username='admin').first().files]
    return render_template('delete.html', title='Delete', form=form)


@app.route('/deleter', methods=['POST', 'GET'])
def deleter():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
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


@app.route('/content')
@login_required
def content():
    if not session.get('logged_in'):
        return render_template('login.html')
    user = current_user
    files = File.query.all()
    return render_template('content.html', title="Content", user=user, files=files)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
