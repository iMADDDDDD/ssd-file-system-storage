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
pip install ftp

To update database
flask db migrate -m "Nom de ta migration"
flask db upgrade
