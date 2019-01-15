from flask import Blueprint

bp = Blueprint('fileModification', __name__)

from app.fileModification import forms, routes