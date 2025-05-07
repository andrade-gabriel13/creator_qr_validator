from pydantic import BaseModel
from typing import List


class RegisterRequest(BaseModel):
    username: str
    password: str



class LoginRequest(BaseModel):
    username: str
    password: str
    scopes: List[str]