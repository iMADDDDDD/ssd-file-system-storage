from flask import Blueprint

bp = Blueprint('fileDownload', __name__)

from app.fileDownload import forms, routes
