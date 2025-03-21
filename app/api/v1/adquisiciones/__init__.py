from flask import Blueprint
from flask_restx import Namespace


adquisiciones_bp = Blueprint('adquisiciones', __name__)
adquisiciones_ns = Namespace('adquisiciones', description='Adquisiciones API operation')
from . import adquisiciones_api