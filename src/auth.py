import requests
import json
from configuration import conf
from pydantic import BaseModel
from datetime import datetime

class Session(BaseModel):
    expiresAt: datetime
    token: str
    createdAt: datetime
    updatedAt: datetime
    ipAddress: str
    userAgent: str
    userId: str
    id: str

class User(BaseModel):
    name: str
    email: str
    emailVerified: bool
    image: str
    createdAt: datetime
    updatedAt: datetime
    id: str

class AuthResponse(BaseModel):
    session: Session
    user: User


def get_auth_session(better_auth_session_token: str):
    response = requests.get(
        f"{conf.auth_server_uri}/api/auth/get-session",
        cookies={
            "better-auth.session_token": better_auth_session_token
        }
    )

    jsonRes = json.loads(response.text)
    return AuthResponse(**jsonRes)
