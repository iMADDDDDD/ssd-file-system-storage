from flask_mail import Message
from flask import render_template
from app import app, mail
from threading import Thread


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    tk = user.get_reset_password_token()
    t = JwtToken(token = tk)
    db.session.add(t)
    db.session.commit()
    send_email('[secure Upload] Reset Your Password',
               sender=app.config['ADMINS'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=tk),
               html_body=render_template('email/reset_password.html', user=user, token=tk)
               )

def send_confirmation_email(user):
    tk = user.get_reset_password_token()
    t = JwtToken(token = tk)
    db.session.add(t)
    db.session.commit()
    send_email('[secure Upload] Confirm your account',
               sender=app.config['ADMINS'],
               recipients=[user.email],
               text_body=render_template('email/confirm.txt', user=user, token=tk),
               html_body=render_template('email/confirm.html', user=user, token=tk)
               )

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
