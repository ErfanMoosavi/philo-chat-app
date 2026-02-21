from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError
from ..dependencies import get_current_user, get_db, get_philo_chat
from ..schemas.user import UserUpdateReq
from ..services import PhiloChat

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.delete_account(db, user_id)
        return {"message": "User deleted successfully"}

    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.patch("/me", status_code=status.HTTP_200_OK)
def update_user(
    request: UserUpdateReq,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.update_profile(db, user_id, request.first_name, request.age)

        return {"message": "Updated user successfully"}

    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
