@app.route('/upload')
@login_required
def upload():
        form = UploadForm()
        return render_template('fileModification/upload.html', title='Upload Normal file', form=form)

@app.route('/upload_normal')
@login_required
def upload_normal():
        form = UploadForm()
        return render_template('fileModification/upload_normal_file.html', title='Upload Normal file', form=form)

@app.route('/upload_group')
@login_required
def upload_group():
        form = UploadForm()
        return render_template('fileModification/upload_group_file.html', title='Upload Group File', form=form)

@app.route('/uploader', methods = ['POST'])
@login_required
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        user = User.query.filter_by(username="admin").first()
        newfile = File(filename=f.filename, author=user)
        db.session.add(newfile)
        db.session.commit()
        flash('File uploaded successfully')
        return render_template('index.html')

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeletionForm()
    form.filename.choices = [(int(f.id), f.filename) for f in User.query.filter_by(username='admin').first().files]
    return render_template('fileModification/delete.html', title='Delete', form=form)

@app.route('/deleter', methods=['POST', 'GET'])
@login_required
def deleter():
    form = DeletionForm()
    if form.validate_on_submit():
        f = File.query.filter_by(id=form.filename.data).first()
        if os.path.exists(f.filename):
            os.remove(f.filename)
            db.session.delete(f)
            db.session.commit()
            return f.filename + " has been deleted correctly"
        else:
            return 'Error'
    return str(form.errors)