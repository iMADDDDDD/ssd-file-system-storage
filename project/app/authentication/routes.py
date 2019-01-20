import pyqrcode
import os

from app import app, db
from app.models import User, File, JwtToken, Role
from app.authentication.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email, send_confirmation_email
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from datetime import timedelta
from uuid import uuid4
from io import BytesIO


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('Who are you ?')
        if not user.confirmed:
            flash('Confirm your account before logging in')
            return redirect(url_for('login'))
        if user.locked:
            flash("Your account has been locked.\n Please wait for the asministrator to unlock your account")
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            user.failedLogin += 1
            if user.failedLogin >= 3:
                user.locked = True
            db.session.add(user)
            db.session.commit()
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if not user.verify_totp(form.token.data):
            user.failedLogin += 1
            if user.failedLogin >= 3:
                user.locked = True
            db.session.add(user)
            db.session.commit()
            flash('Invalid token')
            return redirect(url_for('login'))
        user.failedLogin = 0
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        session['logged_in'] = True
        session['number'] = str(uuid4())
        session.permanent = True
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('authentication/login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, confirmed=False)
        user.set_password(form.password.data)
        user.activated = False
        user.locked = False
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        return redirect(url_for('two_factor_setup'))
    return render_template('authentication/register.html', title='Register', form=form)


@app.route('/registered/<token>', methods=['GET'])
def registered(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    user.confirmed = True
    db.session.commit()
    flash('Your registration has been confirmed')
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('authentication/reset_password_request.html', title='Reset Password', form=form)


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
        tk = JwtToken.query.filter(JwtToken.token == token).first()
        db.session.delete(tk)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('authentication/reset_password.html', form=form)


@app.route('/twofactor')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return redirect(url_for('index'))

    return render_template('authentication/two_factor_setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()

    if user is None:
        abort(404)

    del session['username']

    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=5)

    send_confirmation_email(user)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}
