import os
from datetime import datetime, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, InvalidSignatureError

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
        decoded = jwt.decode(token, "test_key", algorithms=["HS256"])
        username = decoded.get("username")

        if token in blacklisted_tokens:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authentication failed: token has been revoked",
            )
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


# Set of blacklisted tokens
blacklisted_tokens: set[str] = set()


# Logout receives the token from this function to add it to the black list
def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return credentials.credentials
