from datetime import datetime, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, InvalidSignatureError

from .database import SessionLocal
from .services import PhiloChat
from .config import settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


philo_chat = PhiloChat()


def get_philo_chat() -> PhiloChat:
    return philo_chat


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = decoded.get("user_id")

        if token in blacklisted_tokens:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authentication failed: token has been revoked",
            )
        if not user_id:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authetication failed, user_id not in payload",
            )
        if decoded.get("type") != "access":
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authetication failed, token type not valid",
            )
        exp_time = datetime.fromtimestamp(decoded.get("exp"), tz=timezone.utc)
        if exp_time < datetime.now(timezone.utc):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Authetication failed, token expired"
            )
        return user_id

    except InvalidSignatureError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Authetication failed, invalid signature"
        )
    except DecodeError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Authetication failed, decoder error"
        )
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))


# Set of blacklisted tokens
blacklisted_tokens: set[str] = set()


# Logout receives the token from this function to add it to the black list
def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return credentials.credentials
