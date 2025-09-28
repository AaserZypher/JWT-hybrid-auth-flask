from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from . import auth_bp
from .decorators import admin_required
from extensions import db
from models import User  # Each API can have its own User model

# ---------------- Email/Password Login ----------------
@auth_bp.post("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad credentials"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    resp = jsonify(access=access_token)
    resp.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Lax")
    return resp

# ---------------- Refresh Token ----------------
@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access=access_token)

# ---------------- Protected Test Route ----------------
@auth_bp.get("/protected")
@jwt_required()
def protected():
    return jsonify(msg=f"Hello user {get_jwt_identity()}")

# ---------------- Admin Test Route ----------------
@auth_bp.get("/admin-only")
@admin_required
def admin_route():
    return jsonify(msg="You are an admin!")