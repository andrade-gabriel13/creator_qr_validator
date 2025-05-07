from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User, db_users
from auth import verify_password, create_access_token, create_mfa_secret, verify_mfa_code
from utils import generate_qr_code_base64
from jose import JWTError, jwt
from datetime import timedelta
from baseModel import RegisterRequest, LoginRequest

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

@app.post("/register")
def register(data: RegisterRequest):
    if data.username in db_users:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    user = User.create(data.username, data.password)
    db_users[data.username] = user
    return {"msg": "Usuário registrado com sucesso"}

@app.get("/mfa/setup")
def mfa_setup(username: str):
    user = db_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.mfa_enabled = True
    user.mfa_secret = create_mfa_secret()
    uri = f"otpauth://totp/MinhaApp:{username}?secret={user.mfa_secret}&issuer=MinhaApp"
    qr = generate_qr_code_base64(uri)
    return {"otpauth_url": uri, "qr_code": qr}

@app.post("/login")
def login(data: LoginRequest):
    user = db_users.get(data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if user.mfa_enabled:
        if not data.scopes or not verify_mfa_code(user.mfa_secret, data.scopes[0]):
            raise HTTPException(status_code=401, detail="Código MFA inválido")

    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}

@app.get("/usuario/perfil")
def read_profile(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")
    user = db_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"username": user.username, "mfa_enabled": user.mfa_enabled}
