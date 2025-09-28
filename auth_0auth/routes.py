from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from . import auth_bp, oauth  # <-- oauth is the Authlib OAuth() instance with providers registered
from .models import User
from extensions import db
from .decorators import admin_required

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


# ---------------- OAuth Login ----------------
@auth_bp.route("/login/<provider>")
def login_oauth(provider):
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"error": f"Provider {provider} not configured"}), 404
    redirect_uri = url_for("auth.oauth_callback", provider=provider, _external=True)
    return client.authorize_redirect(redirect_uri)


@auth_bp.route("/authorize/<provider>")
def oauth_callback(provider):
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"error": f"Provider {provider} not configured"}), 404

    token = client.authorize_access_token()

    # Fetch user info depending on provider
    if provider == "google":
        user_info = client.get("userinfo").json()
    elif provider == "github":
        user_info = client.get("user").json()
    elif provider == "microsoft":
        user_info = client.get("v1.0/me").json()
    elif provider == "facebook":
        user_info = client.get("me?fields=id,name,email,picture").json()
    else:
        return jsonify({"error": "Unsupported provider"}), 400

    if not user_info:
        return jsonify({"error": "Failed to fetch user info"}), 400

    # Normalize email and name
    email = (
        user_info.get("email")
        or user_info.get("userPrincipalName")  # Microsoft
        or None
    )
    name = (
        user_info.get("name")
        or user_info.get("displayName")  # Microsoft
        or user_info.get("login")  # GitHub
    )

    if not email:
        return jsonify({"error": "No email available from provider"}), 400

    # Lookup or create user
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.commit()

    # Issue JWTs
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    resp = jsonify(access=access_token, provider=provider, user={"email": user.email, "name": user.name})
    resp.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Lax")
    return resp


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