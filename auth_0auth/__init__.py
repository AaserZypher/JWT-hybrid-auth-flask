import os
from flask import Blueprint
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager

# ---------------- Blueprint & Extensions ----------------
auth_bp = Blueprint("auth", __name__)
jwt = JWTManager()
oauth = OAuth()

# ---------------- OAuth Providers ----------------

# Google OAuth
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v3/",
    client_kwargs={"scope": "openid email profile"},
)

# GitHub OAuth
oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

# Microsoft OAuth
# Tenant ID can be: "common", "organizations", or "consumers"
MS_TENANT = os.getenv("MICROSOFT_TENANT_ID", "common")
oauth.register(
    name="microsoft",
    client_id=os.getenv("MICROSOFT_CLIENT_ID"),
    client_secret=os.getenv("MICROSOFT_CLIENT_SECRET"),
    access_token_url=f"https://login.microsoftonline.com/{MS_TENANT}/oauth2/v2.0/token",
    authorize_url=f"https://login.microsoftonline.com/{MS_TENANT}/oauth2/v2.0/authorize",
    api_base_url="https://graph.microsoft.com/",
    client_kwargs={"scope": "openid email profile User.Read"},
)

# Facebook OAuth
oauth.register(
    name="facebook",
    client_id=os.getenv("FACEBOOK_CLIENT_ID"),
    client_secret=os.getenv("FACEBOOK_CLIENT_SECRET"),
    access_token_url="https://graph.facebook.com/oauth/access_token",
    authorize_url="https://www.facebook.com/dialog/oauth",
    api_base_url="https://graph.facebook.com/",
    client_kwargs={"scope": "email"},
)