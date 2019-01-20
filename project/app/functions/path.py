import os
from app import app
from app.models import User, File, Folder

from flask import send_from_directory

def returnPathOfFile(fileId):
	fileD = File.query.get(itemId)
	parentFolder = Folder.queryget(fileD.folderId)
	path = "/"+parentFolder.name
	while(parentFolder.parent):
		parentFolder = Folder.query.get(parentFolder.parent)
		path = "/" + parentFolder.name + path
	print(app.config['UPLOAD_PATH']+path, fileD.name)
	return path
