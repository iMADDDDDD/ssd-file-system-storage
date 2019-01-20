import os
import pysftp
import socket

from app import app, db
from app.models import User, File, Folder
from app.email import send_password_reset_email
from app.fileModification.forms import UploadForm
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from datetime import timedelta
from uuid import uuid4
from app.routes import currentPath

@app.route('/download/file/<itemID>', methods = ['GET', 'POST'])
@login_required
def downloadFile(itemId):
   path = returnPathOfFile(itemId)
   return send_from_directory(directory=path, filename=fileD.name)
		
	
