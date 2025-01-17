import os
from app import app
from app.models import User, File, Folder

from flask import send_from_directory

def returnDirectoryOfFile(fileD):
	parentFolder = fileD.parent
	path = "/"+ parentFolder.name
	while(parentFolder.parent):
		parentFolder = parentFolder.parent
		path = "/" + parentFolder.name + path
	return app.config['UPLOAD_PATH'] + path
	
def returnPathOfFile(fileId):
	fileD = File.query.get(fileId)
	directory = returnDirectoryOfFile(fileD)
	return directory + "/" + fileD.name

def returnPathOfFolder(folderId):
	folder = Folder.query.get(folderId)
	parentFolder = folder.parent
	path= ""
	if parentFolder:
		path = "/" + parentFolder.name
		while(parentFolder.parent):
			parentFolder = parentFolder.parent
			path = "/" + parentFolder.name + path
	return app.config['UPLOAD_PATH'] + path + "/" + folder.name
