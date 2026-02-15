import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .services import PhiloChat

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")
philo_chat = PhiloChat(api_key=api_key, base_url=base_url, model_name=model)


def get_philo_chat() -> PhiloChat:
    return philo_chat


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    decoded = jwt.decode(token, "test_key", algorithm="HS256")
    username = decoded.get("username")
    return username


def generate_access_token(username: str, expires_in: int = 1) -> str:
    now = datetime.now()
    payload = {
        "type": "access",
        "username": username,
        "iat": now,
        "exp": now + timedelta(hours=expires_in),
    }
    return jwt.encode(payload, "test_key", algorithm="HS256")


def generate_refresh_token(username: str, expires_in: int = 7) -> str:
    now = datetime.now()
    payload = {
        "type": "refresh",
        "username": username,
        "iat": now,
        "exp": now + timedelta(days=expires_in),
    }
    return jwt.encode(payload, "test_key", algorithm="HS256")
