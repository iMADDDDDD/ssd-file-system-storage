import os
from app import app
from app.models import User, File, Folder

from flask import send_from_directory

def returnPathOfFile(fileId):
	fileD = File.query.get(fileId)
	parentFolder = fileD.parent
	path = "/"+parentFolder.name
	while(parentFolder.parent):
		parentFolder = parentFolder.parent
		path = "/" + parentFolder.name + path
	print(app.config['UPLOAD_PATH']+path, fileD.name)
	return path
