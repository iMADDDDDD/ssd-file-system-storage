from app import app, db
from app.functions.path import returnPathOfFile, returnDirectoryOfFile, returnPathOfFolder
from app.models import User, File, Folder
from flask import render_template, redirect, url_for, flash, send_from_directory, send_file
from flask_login import current_user, login_required
from cryptography.fernet import Fernet

import zipfile
import io
import os


@app.route('/download/<itemID>', methods = ['GET', 'POST'])
@login_required
def downloadFile(itemID):
   fileD = File.query.get(itemID)
   path = returnDirectoryOfFile(fileD)
   if current_user.id in [user.id for user in fileD.AccessFile]:
      flash(fileD.name + " has been succesfuly downloaded")
      print(path, fileD.name)
      
      with open(os.path.join(path,fileD.name), 'rb') as f:
         data = f.read()

      fernet = Fernet(fileD.encryptionKey)

      decrypted = fernet.decrypt(data)
      
      return send_file(io.BytesIO(decrypted), as_attachment = True, attachment_filename=fileD.name)
   else:
      flash("Access denied!")
      return redirect(url_for('index'))

@app.route('/download/folder/<itemID>', methods = ['GET', 'POST'])
@login_required
def downloadFolder(itemID):
   folder = Folder.query.get(itemID)
   if current_user.id in [user.id for user in folder.AccessFolder] and folder.AccessFolder.count() == 1:
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as z:
           z = zipfile.ZipFile(folder.name + '.zip', mode='w')
           recAddToZip(z, itemID)	
           z.close()
           return send_from_directory(directory=app.config['UPLOAD_PATH'], filename=folder.name + '.zip', mimetype='application/zip', as_attachment=True)
   else:
        flash("Access denied!")
        return redirect(url_for('index'))

def recAddToZip(zipFile, itemId):
   files = File.query.filter_by(folderId=itemId)
   for f in files:
      if current_user in f.AccessFile and f.AccessFile.count() == 1:
         path = returnPathOfFolder(itemId)
         with open(os.path.join(path,f.name), 'rb') as f:
            data = f.read()
         fernet = Fernet(app.config["EKEY"])
         decrypted = fernet.decrypt(data)
         
         zipFile.writestr(f.name, decrypted, compress_type=zipFile.compression)
   folder = Folder.query.get(itemId)
   for f in folder.subFolders:
      recAddToZip(zipFile, f.id) 
