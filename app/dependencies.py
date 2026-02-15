import os
from datetime import datetime, timedelta

import jwt
from jwt import InvalidSignatureError, DecodeError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .services import PhiloChat

# Create a global instance of PhiloChat
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")
philo_chat = PhiloChat(api_key=api_key, base_url=base_url, model_name=model)


def get_philo_chat() -> PhiloChat:
    return philo_chat


# Security setup
security = HTTPBearer()


# Every private action receives username from this function
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, "test_key", algorithm="HS256")
        username = decoded.get("username")

        if not username:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authetication failed, username not in payload",
            )
        if decoded.get("type") != "access":
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authetication failed, token type not valid",
            )
        if datetime.fromtimestamp(decoded.get("exp")) < datetime.now:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Authetication failed, token expired"
            )
        return username

    except InvalidSignatureError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Authetication failed, invalid signature"
        )
    except DecodeError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Authetication failed, error in decoder"
        )
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))


def generate_access_token(username: str, expires_in: int = 1) -> str:
    now = datetime.now()
    payload = {
        "type": "access",
        "username": username,
        "iat": now,
        "exp": now + timedelta(hours=expires_in),
    }
    return jwt.encode(payload, "test_key", algorithm="HS256")


def generate_refresh_token(username: str, expires_in: int = 7 * 24) -> str:
    now = datetime.now()
    payload = {
        "type": "refresh",
        "username": username,
        "iat": now,
        "exp": now + timedelta(days=expires_in),
    }
    return jwt.encode(payload, "test_key", algorithm="HS256")
