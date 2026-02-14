from fastapi import APIRouter, Depends

from ..dependencies import get_philo_chat
from ..schemas.user import UserUpdateReq
from ..services import PhiloChat

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/me")
def delete_user(pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.delete_account()

    except Exception:
        pass


@router.patch("/me")
def update_user(request: UserUpdateReq, pc: PhiloChat = Depends(get_philo_chat)):
    if request.name:
        pc.set_name(request.name)
    if request.age:
        pc.set_age(request.age)
    return {"message": "Profile updated"}
