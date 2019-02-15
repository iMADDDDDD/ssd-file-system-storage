The flask project will be here

You have to import several packages to be able to run the project
cd project/
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install flask_sqlalchemy
pip install flask_migrate
pip install flask_login
pip install flask_wtf
pip install flask_bootstrap
pip install flask_fontawesome
pip install flask_mail
pip install pyjwt
pip install onetimepass
pip install pyqrcode
pip install pysftp
pip install pytransmit
pip install flask_uploads

To delete the existing database
rm -rf app.db migrations/

To create the database
flask db init
flask db migrate -m "Nom de la migration"
flask db upgrade


To set up the database correctly
export FLASK_APP=microblog.py
flask shell 
This will open a python console copy/paste the rest of the lines to add a first repository that will contain all the files
db.session.add(Folder(name="Files"))
db.session.commit()
exit()

To execute the application
flask run --cert app/cert.pem --key app/key.pem

To change the role of the user you have just created to administrator
flash shell
user = User.query.get(1)
user.role = Role.admin
db.session.commit()
exit()
