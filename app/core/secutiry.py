from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from jwt import DecodeError, InvalidSignatureError

from ..config import settings


def generate_access_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": "access",
        "username": username,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.secret_key)


def generate_refresh_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": "refresh",
        "username": username,
        "iat": now,
        "exp": now + timedelta(days=settings.refresh_token_expire_days),
    }
    return jwt.encode(payload, settings.secret_key)


def decode_refresh_token(refresh_token: str):
    try:
        decoded = jwt.decode(
            refresh_token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = decoded.get("username")

        if not username:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authetication failed, username not in payload",
            )
        if decoded.get("type") != "refresh":
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authetication failed, token type not valid",
            )
        exp_time = datetime.fromtimestamp(decoded.get("exp"), tz=timezone.utc)
        if exp_time < datetime.now(timezone.utc):
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
            status.HTTP_401_UNAUTHORIZED, "Authetication failed, decoder error"
        )
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))
