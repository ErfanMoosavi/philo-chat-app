from fastapi import APIRouter, Depends, status

from ..dependencies import get_philo_chat
from ..schemas.user import UserUpdateReq
from ..services import PhiloChat

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_user(pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.delete_account()

    except Exception:
        pass


@router.patch("/me", status_code=status.HTTP_200_OK)
def update_user(request: UserUpdateReq, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        if request.name:
            pc.set_name(request.name)
        if request.age:
            pc.set_age(request.age)

    except Exception:
        pass
