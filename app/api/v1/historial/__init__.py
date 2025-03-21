from flask import Blueprint
from flask_restx import Namespace


historial_bp = Blueprint('historial', __name__)
historial_ns = Namespace('historial', description='historial API operation')
from . import historial_api