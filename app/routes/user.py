from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_philo_chat, get_current_user
from ..schemas.user import UserUpdateReq
from ..services import PhiloChat

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_user(
    username: str = Depends(get_current_user),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.delete_account(username)
        return {"message": "User deleted seccessfully"}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/me", status_code=status.HTTP_200_OK)
def update_user(
    request: UserUpdateReq,
    username: str = Depends(get_current_user),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        if request.name:
            pc.set_name(username, request.name)
        if request.age:
            pc.set_age(username, request.age)

        return {"message": "Updated user seccessfully"}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
