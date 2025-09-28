# JWT Hybrid Auth for Flask

A modular authentication system for Flask APIs, supporting **hybrid JWT authentication** with both **basic email/password login** and **OAuth 2.0 logins** (Google, GitHub, Microsoft, Facebook).  

This project is designed to be **plug-and-play** across multiple Flask APIs.  
- Use `auth_basic` if you only need email/password accounts.  
- Use `auth_oauth` if you want OAuth provider logins as well.  

---

## ✨ Features

- **Hybrid JWT system**  
  - Access tokens via headers (`Authorization: Bearer <token>`)  
  - Refresh tokens via secure HTTP-only cookies  
  - Works seamlessly for both **browser-based apps** (cookies) and **mobile/external APIs** (headers).  

- **Two authentication modules**  
  - `auth_basic` → minimal JWT auth with email/password.  
  - `auth_oauth` → everything from `auth_basic` + OAuth logins with Google, GitHub, Microsoft, Facebook.  

- **Blueprint-based** → Drop into any Flask API project.  
- **Customizable decorators** (`@jwt_required`, `@admin_required`).  
- **Extensible utils** → Normalize email, validate password strength, etc.  

---

## 📂 Project Structure

```
JWT-hybrid-auth-flask/
├── auth_basic/
│   ├── __init__.py
│   ├── routes.py
│   ├── decorators.py
│   └── utils.py
│
├── auth_oauth/
│   ├── __init__.py
│   ├── routes.py
│   ├── decorators.py
│   └── utils.py
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install flask flask-jwt-extended authlib python-dotenv
```

### 2. Add to your Flask API
Example `app.py`:
```python
from flask import Flask
from auth_basic import auth_bp as basic_auth
from auth_oauth import auth_bp as oauth_auth
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

# Choose one module:
app.register_blueprint(basic_auth, url_prefix="/auth")
# or:
# app.register_blueprint(oauth_auth, url_prefix="/auth")
```

### 3. Environment variables

- For `auth_basic`, you only need:
```env
JWT_SECRET_KEY=your_secret_key
```

- For `auth_oauth`, you’ll also need provider keys:  
```env
GOOGLE_CLIENT_ID=xxxx
GOOGLE_CLIENT_SECRET=xxxx
GITHUB_CLIENT_ID=xxxx
GITHUB_CLIENT_SECRET=xxxx
MICROSOFT_CLIENT_ID=xxxx
MICROSOFT_CLIENT_SECRET=xxxx
MICROSOFT_TENANT_ID=common
FACEBOOK_CLIENT_ID=xxxx
FACEBOOK_CLIENT_SECRET=xxxx
```

> ⚠️ You must register your app with each provider to obtain these.  
Links: [Google](https://console.cloud.google.com/), [GitHub](https://github.com/settings/developers), [Microsoft](https://portal.azure.com/), [Facebook](https://developers.facebook.com/).  

---

## 🔑 Example Routes

### `auth_basic`
- `POST /auth/login` → email/password login  
- `POST /auth/refresh` → refresh JWT  
- `GET /auth/protected` → JWT-protected route  
- `GET /auth/admin-only` → admin-only route  

### `auth_oauth`
- `GET /auth/login/<provider>` → redirect to OAuth provider (google, github, microsoft, facebook)  
- `GET /auth/callback/<provider>` → handle OAuth callback  
- Same JWT issue/refresh logic as `auth_basic`  

---

## 🛠️ Utils
Both modules share helpers in `utils.py`, such as:
- Normalize emails  
- Validate password strength  
- (Extensible for custom claims, role management, etc.)  

---

## 📜 License
MIT License — free to use, modify, and distribute.  

---

👉 With this repo, you can quickly **drop authentication into any Flask API** — from a personal blog to a full SaaS app.  
