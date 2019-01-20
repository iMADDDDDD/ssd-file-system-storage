from app import app, db
from app.functions.path import returnPathOfFile
from app.models import User, File, Folder
from flask import render_template, redirect, url_for, flash, send_from_directory
from flask_login import current_user, login_required
import zipfile



@app.route('/download/<itemID>', methods = ['GET', 'POST'])
@login_required
def downloadFile(itemID):
   fileD = File.query.get(itemID)
   path = returnPathOfFile(itemID)
   if current_user.id in [user.id for user in fileD.AccessFile]:
        flash(fileD.name + " has been succesfuly downloaded")
        return send_from_directory(directory=path, filename=fileD.name, as_attachment = True)
   else:
        flash("Access denied!")
        return redirect(url_for('index'))

@app.route('/download/folder/<itemID>', methods = ['GET', 'POST'])
@login_required
def downloadFolder(itemID):

   if current_user.id in [user.id for user in fileD.AccessFile]:
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as z:
           z = zipfile.ZipFile('zipfile_write_compression.zip', mode='w')
           recAddToZip(z, itemId)	
           z.close()
           return fl.send_file(data, mimetype='application/zip', as_attachment=True, attachment_filename='data.zip')
   else:
        flash("Access denied!")
        return redirect(url_for('index'))


def recAddToZip(zipFile, itemId):
   files = File.query.filter_by(folderId=itemId)
   for f in files:
      if current_user in f.AccessFile and len(f.AccessFile) == 1:
         path = returnPathOfFile(itemID)
         zipFile.write(path+'/'+f.name, compress_type=compression)
   folder = Folder.query.get(itemId)
   folders = [ f.id for f in folder.subFolders]
   for fId in folders:
      recAddToZip(zipFile, fId) 











