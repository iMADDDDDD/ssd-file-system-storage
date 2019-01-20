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
from pytransmit import FTPClient


@app.route('/download/<fileId>')
@login_required
def download(itemType, itemId):
	if not current_user.is_authenticated:
        	return redirect(url_for('index'))
	verification = 
	if 
	
