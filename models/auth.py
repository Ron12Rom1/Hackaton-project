from typing import Optional
from pydantic import BaseModel

class TokenData(BaseModel):
    username: Optional[str] = None
    user_type: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    user_type: str 