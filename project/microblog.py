from app import app, db
from app.models import User, File, Folder

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'File': File, 'Folder': Folder}