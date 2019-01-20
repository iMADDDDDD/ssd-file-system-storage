from app import app, db
from app.functions.path import returnPathOfFile
from app.models import User, File, Folder
from flask import render_template, redirect, url_for, flash, send_from_directory
from flask_login import current_user, login_required


@app.route('/download/file/<itemID>', methods = ['GET', 'POST'])
@login_required
def downloadFile(itemID):
   fileD = File.query.get(itemID)
   path = app.config['UPLOAD_PATH'] + returnPathOfFile(itemID)
   flash(path)
   return send_from_directory(directory=path, filename=fileD.name)

