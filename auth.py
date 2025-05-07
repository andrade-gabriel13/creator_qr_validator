import pyotp
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

def verify_password(plain, hashed):
    return bcrypt.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_mfa_secret():
    return pyotp.random_base32()

def verify_mfa_code(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
