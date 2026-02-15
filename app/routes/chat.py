from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_philo_chat, get_username_from_header
from ..schemas.chat import ChatCreateReq, MessageCreateReq
from ..services import PhiloChat

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_chat(
    chat: ChatCreateReq,
    username: str = Depends(get_username_from_header),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.new_chat(username, chat.chat_name, chat.philosopher_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK)
def get_chats(
    username: str = Depends(get_username_from_header),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        chat_list = pc.list_chats(username)
        return chat_list

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{chat_name}", status_code=status.HTTP_200_OK)
def delete_chat(
    chat_name: str,
    username: str = Depends(get_username_from_header),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.delete_chat(username, chat_name)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{chat_name}/messages", status_code=status.HTTP_201_CREATED)
def create_message(
    chat_name: str,
    data: MessageCreateReq,
    username: str = Depends(get_username_from_header),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        ai_msg, user_msg = pc.complete_chat(username, chat_name, data.input_text)
        return ai_msg, user_msg

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
