from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_philo_chat, get_username_from_header
from ..schemas.user import UserUpdateReq
from ..services import PhiloChat

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_user(
    username: str = Depends(get_username_from_header),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.delete_account(username)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/me", status_code=status.HTTP_200_OK)
def update_user(
    request: UserUpdateReq,
    username: str = Depends(get_username_from_header),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        if request.name:
            pc.set_name(username, request.name)
        if request.age:
            pc.set_age(username, request.age)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
