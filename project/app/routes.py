from app import app, db
import os
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, File
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, DeletionForm

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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['POST'])
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
    form = DeletionForm()
    form.filename.choices = [(int(f.id), f.filename) for f in User.query.filter_by(username='admin').first().files]
    return render_template('delete.html', title='Delete', form=form)

@app.route('/deleter', methods=['POST', 'GET'])
def deleter():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
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