from flask import Blueprint
from flask_jwt_extended import JWTManager

auth_bp = Blueprint("auth", __name__)
jwt = JWTManager()