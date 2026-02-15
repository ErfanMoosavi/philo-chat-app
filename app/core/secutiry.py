from datetime import datetime, timedelta, timezone

import jwt


def generate_access_token(username: str, expires_in: int = 1) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": "access",
        "username": username,
        "iat": now,
        "exp": now + timedelta(hours=expires_in),
    }
    return jwt.encode(payload, "test_key")


def generate_refresh_token(username: str, expires_in: int = 7 * 24) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": "refresh",
        "username": username,
        "iat": now,
        "exp": now + timedelta(days=expires_in),
    }
    return jwt.encode(payload, "test_key")
