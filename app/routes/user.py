from fastapi import APIRouter, Depends, HTTPException, status

from ..core.exceptions import NotFoundError
from ..dependencies import get_current_user, get_philo_chat
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
        return {"message": "User deleted successfully"}

    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.patch("/me", status_code=status.HTTP_200_OK)
def update_user(
    request: UserUpdateReq,
    username: str = Depends(get_current_user),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        if request.name is not None:
            pc.set_first_name(username, request.first_name)
        if request.age is not None:
            pc.set_age(username, request.age)

        return {"message": "Updated user successfully"}

    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
