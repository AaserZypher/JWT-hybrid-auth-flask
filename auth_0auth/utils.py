import re

def normalize_email(email: str) -> str:
    if not email:
        return None
    return email.strip().lower()

def validate_password_strength(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    return True