from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_philo_chat, get_username_from_header
from ..schemas.auth import LoginReq, SignupReq
from ..services import PhiloChat

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def user_signup(request: SignupReq, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.signup(request.username, request.password)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/login", status_code=status.HTTP_200_OK)
def user_login(request: LoginReq, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.login(request.username, request.password)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/logout", status_code=status.HTTP_200_OK)
def user_logout(
    username: str = Depends(get_username_from_header),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.logout(username)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
