from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.exceptions import BadRequestError, NotFoundError
from ..dependencies import get_current_user, get_db, get_philo_chat
from ..schemas.chat import ChatCreateReq, MessageCreateReq
from ..services import PhiloChat

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_chat(
    chat: ChatCreateReq,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.new_chat(db, user_id, chat.chat_name, chat.philosopher_id)
        return {"message": "Created chat successfully"}

    except BadRequestError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/", status_code=status.HTTP_200_OK)
def get_chats(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        chat_list = pc.get_chats(db, user_id)
        return chat_list

    except NotFoundError:
        return []
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.delete("/{chat_id}", status_code=status.HTTP_200_OK)
def delete_chat(
    chat_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.delete_chat(db, user_id, chat_id)
        return {"message": "Deleted chat successfully"}

    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.post("/{chat_id}/messages", status_code=status.HTTP_201_CREATED)
def create_message(
    chat_id: int,
    data: MessageCreateReq,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.complete_chat(db, user_id, chat_id, data.input_text)

    except BadRequestError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
