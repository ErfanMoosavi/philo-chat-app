from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.exceptions import BadRequestError, NotFoundError, PermissionDeniedError
from ..core.models import User
from ..core.secutiry import (
    decode_refresh_token,
    generate_access_token,
    generate_refresh_token,
)
from ..dependencies import get_db, get_philo_chat, get_token
from ..schemas.auth import LoginReq, RefreshTokenReq, SignupReq
from ..services import PhiloChat

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(
    request: SignupReq,
    db: Session = Depends(get_db),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.signup(db, request.username, request.password)
        return {"message": "Signed up successfully"}

    except BadRequestError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    request: LoginReq,
    db: Session = Depends(get_db),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.login(db, request.username, request.password)

        user = db.query(User).filter(User.username == request.username).first()

        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)

        return {
            "message": "Logged in successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    except NotFoundError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except PermissionDeniedError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(get_token)):
    try:
        from ..dependencies import blacklisted_tokens

        blacklisted_tokens.add(token)
        return {"message": "Logged out successfully"}

    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
def refresh_token(request: RefreshTokenReq):
    try:
        username = decode_refresh_token(request.refresh_token)
        access_token = generate_access_token(username)
        return {
            "message": "Generated access token successfully",
            "access_token": access_token,
        }

    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
