from app import app, db
from app.models import User, File, Folder
from app.email import send_password_reset_email
from app.fileModification.forms import UploadForm
import os
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from datetime import timedelta
from uuid import uuid4
from app.routes import currentPath
import pysftp
from pytransmit import FTPClient
import socket

    
@app.route('/connectFTP')
@login_required
def connectFTP():
	ftp_obj = FTPClient()

	if request.headers.getlist("X-Forwarded-For"):
	       ip_client = request.headers.getlist("X-Forwarded-For")[0]
	    else:
	       ip_client = request.remote_addr

	# FTP Details
	FTP_HOST = socket.gethostbyname(socket.gethostname())
	FTP_USER = ip_client
	FTP_PASS = ""
	FTP_PORT = 21

	ftp_obj.connect(FTP_HOST, FTP_USER, FTP_PASS, FTP_PORT)
	print(ftp_obj.get_message())

@app.route('/upload_normal')
@login_required
def upload_normal():
        srv = pysftp.Connection(host="your_FTP_server", username="your_username",
	password="your_password")

	# Get the directory and file listing
	data = srv.listdir()

	# Closes the connection
	srv.close()

	# Prints out the directories and files, line by line
	for i in data:
	    print i
